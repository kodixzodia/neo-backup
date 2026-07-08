#!/usr/bin/env python3
"""Export a Neo agent/workflow to normalized JSON plus a human-readable summary."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable

import requests

DEFAULT_BASE_URL = os.getenv("NEO_BASE_URL", "https://api.neoagent.io/public-api")

# Tune this list to your tenant. These are the usual "diff noise" fields.
NOISY_KEYS = {
    "exported_at",
    "fetched_at",
    "retrieved_at",
    "created_at",
    "updated_at",
    "last_updated_at",
    "last_modified_at",
    "request_id",
    "timings_ms",
}

SORT_KEY_CANDIDATES = ("id", "name", "title", "key", "slug", "order", "index")


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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def normalize(value: Any) -> Any:
    """Recursively remove noisy fields and sort nested lists."""
    if isinstance(value, dict):
        items = []
        for key in sorted(value.keys()):
            if key in NOISY_KEYS:
                continue
            items.append((key, normalize(value[key])))
        return {k: v for k, v in items}

    if isinstance(value, list):
        normalized = [normalize(item) for item in value]

        if not normalized:
            return normalized

        # Sort lists of dicts by the first stable-looking key we can find.
        if all(isinstance(item, dict) for item in normalized):
            return sorted(normalized, key=dict_sort_key)

        # Sort lists of scalars if possible.
        if all(isinstance(item, (str, int, float, bool)) or item is None for item in normalized):
            return sorted(normalized, key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))

        # Fallback: sort by serialized content.
        return sorted(
            normalized,
            key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False, default=str),
        )

    return value


def dict_sort_key(item: dict[str, Any]) -> tuple:
    for candidate in SORT_KEY_CANDIDATES:
        value = item.get(candidate)
        if value is not None:
            return (0, str(value).lower())
    return (1, json.dumps(item, sort_keys=True, ensure_ascii=False, default=str))


def get_any(data: Any, *paths: str, default: Any = None) -> Any:
    """
    Try a sequence of keys/paths against a nested dict.
    Example: get_any(obj, "name", "metadata.name", default="")
    """
    if isinstance(data, dict):
        for path in paths:
            cur: Any = data
            ok = True
            for part in path.split("."):
                if not isinstance(cur, dict) or part not in cur:
                    ok = False
                    break
                cur = cur[part]
            if ok and cur is not None:
                return cur
    return default


def first_items_text(items: Any, limit: int = 5) -> str:
    if not isinstance(items, list) or not items:
        return ""
    out: list[str] = []
    for item in items[:limit]:
        if isinstance(item, dict):
            label = (
                item.get("name")
                or item.get("title")
                or item.get("key")
                or item.get("slug")
                or item.get("id")
            )
            out.append(str(label))
        else:
            out.append(str(item))
    suffix = "" if len(items) <= limit else f" … (+{len(items) - limit} more)"
    return ", ".join(out) + suffix


def summarize_agent(agent_id: str, agent_name: str, agent: dict[str, Any], snapshot: dict[str, Any]) -> str:
    lines: list[str] = []
    title = agent_name or str(get_any(snapshot, "name", "title", default=f"Agent {agent_id}"))
    lines.append(f"# Neo agent export: {title}")
    lines.append("")
    lines.append(f"- Agent ID: `{agent_id}`")
    if agent_name:
        lines.append(f"- Export label: `{agent_name}`")

    status = get_any(snapshot, "status", "enabled", default=None)
    if status is not None:
        lines.append(f"- Status: `{status}`")

    autonomy_type = get_any(agent, "autonomy_type", "type", default=None)
    if autonomy_type is not None:
        lines.append(f"- Type: `{autonomy_type}`")

    trigger_type = get_any(snapshot, "trigger_type", "trigger.type", default=None)
    if trigger_type is not None:
        lines.append(f"- Trigger: `{trigger_type}`")

    schedule = get_any(snapshot, "schedule", default=None)
    if schedule is not None:
        if isinstance(schedule, dict):
            schedule_text = first_items_text([schedule], limit=1)
            lines.append(f"- Schedule: `{schedule_text}`")
        else:
            lines.append(f"- Schedule: `{schedule}`")

    integrations = get_any(snapshot, "integrations", default=[])
    if isinstance(integrations, list):
        lines.append(f"- Integrations: {len(integrations)}")
        sample = first_items_text(integrations)
        if sample:
            lines.append(f"- Integration sample: {sample}")

    toolbox = get_any(snapshot, "toolbox", default=None)
    if isinstance(toolbox, dict):
        tool_settings = toolbox.get("tool_settings_by_type")
        if isinstance(tool_settings, dict):
            lines.append(f"- Tools configured: {len(tool_settings)}")
            lines.append(f"- Tool sample: {first_items_text([{ 'name': k } for k in tool_settings.keys()])}")

    custom_instructions = get_any(snapshot, "agent_settings.custom_instructions", "custom_instructions", default=None)
    if custom_instructions:
        preview = str(custom_instructions).strip().splitlines()[0]
        lines.append(f"- Instructions preview: {preview[:160]}")

    lines.append("")
    lines.append("## Export contents")
    lines.append("")
    lines.append("- `agents/` = raw agent record")
    lines.append("- `agent_snapshots/` = normalized resolved snapshot")
    lines.append("- `agent_versions/` = normalized version history")
    lines.append("")
    lines.append(f"_Exported at {datetime.now(timezone.utc).isoformat()}_")
    return "\n".join(lines)


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
    agent_data = agent_payload.get("data", agent_payload)
    agent_data = normalize(agent_data)
    write_json(out_dir / "agents" / f"{agent_id}-{safe_name}.json", agent_data)

    snapshot_timestamp = datetime.now(timezone.utc).isoformat()
    print(f"Fetching resolved snapshot for {agent_id} at {snapshot_timestamp}...")
    snapshot_payload = api_get(
        session,
        base_url,
        f"/agents/{agent_id}/version-at",
        params={"timestamp": snapshot_timestamp},
    )
    snapshot_data = snapshot_payload.get("data", snapshot_payload)
    snapshot_data = normalize(snapshot_data)
    write_json(out_dir / "agent_snapshots" / f"{agent_id}-{safe_name}.json", snapshot_data)

    version_count = 0
    if args.include_versions:
        print(f"Fetching versions for {agent_id}...")
        versions_payload = api_get(session, base_url, f"/agents/{agent_id}/versions")
        versions_data = versions_payload.get("data", versions_payload)
        versions_data = normalize(versions_data)
        if isinstance(versions_data, list):
            version_count = len(versions_data)
        write_json(out_dir / "agent_versions" / f"{agent_id}-{safe_name}.json", versions_data)

    summary = summarize_agent(agent_id, args.agent_name.strip(), agent_data, snapshot_data)
    write_text(out_dir / "summaries" / f"{agent_id}-{safe_name}.md", summary)

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
