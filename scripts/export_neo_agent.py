#!/usr/bin/env python3
"""Export one Neo agent/workflow to JSON for GitHub backup."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import requests

DEFAULT_BASE_URL = os.getenv("NEO_BASE_URL", "https://api.neoagent.io/public-api")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-") or "agent"


def api_get(
    session: requests.Session,
    base_url: str,
    path: str,
    params: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    response = session.get(f"{base_url.rstrip('/')}{path}", params=params, timeout=60)
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise SystemExit(f"GET {path} failed: {response.status_code} {response.text[:1000]}") from exc
    return response.json()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a single Neo agent/workflow")
    parser.add_argument("--agent-id", required=True, help="Neo agent/workflow ID, e.g. 23782")
    parser.add_argument("--agent-name", default="", help="Optional friendly name for filenames")
    parser.add_argument("--out", default="neo-backup", help="Output folder")
    parser.add_argument("--include-versions", action="store_true", help="Also export version history")
    args = parser.parse_args()

    api_key = os.getenv("NEO_API_KEY")
    if not api_key:
        print("NEO_API_KEY is required", file=sys.stderr)
        return 2

    base_url = DEFAULT_BASE_URL
    agent_id = str(args.agent_id)
    safe_name = slugify(args.agent_name) if args.agent_name.strip() else f"agent-{agent_id}"
    out_dir = Path(args.out)

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
    )

    print(f"Fetching agent {agent_id}...")
    agent_payload = api_get(session, base_url, f"/agents/{agent_id}")
    write_json(
        out_dir / "agents" / f"{agent_id}-{safe_name}.json",
        agent_payload.get("data", agent_payload),
    )

    snapshot_timestamp = datetime.now(timezone.utc).isoformat()
    print(f"Fetching resolved snapshot for {agent_id} at {snapshot_timestamp}...")
    snapshot_payload = api_get(
        session,
        base_url,
        f"/agents/{agent_id}/version-at",
        params={"timestamp": snapshot_timestamp},
    )
    write_json(
        out_dir / "agent_snapshots" / f"{agent_id}-{safe_name}.json",
        snapshot_payload.get("data", snapshot_payload),
    )

    version_count = 0
    if args.include_versions:
        print(f"Fetching versions for {agent_id}...")
        versions_payload = api_get(session, base_url, f"/agents/{agent_id}/versions")
        versions_data = versions_payload.get("data", versions_payload)
        if isinstance(versions_data, list):
            version_count = len(versions_data)
        write_json(out_dir / "agent_versions" / f"{agent_id}-{safe_name}.json", versions_data)

    write_json(
        out_dir / "manifest.json",
        {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "base_url": base_url,
            "agent_id": agent_id,
            "agent_name": args.agent_name.strip(),
            "include_versions": args.include_versions,
            "version_count": version_count,
        },
    )

    print(f"Done. Wrote export to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
