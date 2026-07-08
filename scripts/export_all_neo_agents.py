#!/usr/bin/env python3
"""Export every enabled Neo agent/workflow."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import requests

DEFAULT_BASE_URL = os.getenv("NEO_BASE_URL", "https://api.neoagent.io/public-api")

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

TEXT_FIELD_KEYS = {"custom_instructions", "additional_instructions"}
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
    response = session.get(f"{base_url.rstrip('/')}{path}", params=params, timeout=90)
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise SystemExit(
            f"GET {path} failed: {response.status_code} {response.text[:1000]}"
        ) from exc
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
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key in sorted(value.keys()):
            if key in NOISY_KEYS:
                continue
            out[key] = normalize(value[key])
        return out

    if isinstance(value, list):
        normalized = [normalize(item) for item in value]

        if not normalized:
            return normalized

        if all(isinstance(item, dict) for item in normalized):
            return sorted(normalized, key=dict_sort_key)

        if all(isinstance(item, (str, int, float, bool)) or item is None for item in normalized):
            return sorted(normalized, key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))

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


def list_all_agents(
    session: requests.Session,
    base_url: str,
    state: str = "ENABLED",
) -> list[dict[str, Any]]:
    agents: list[dict[str, Any]] = []
    cursor: str | None = None

    while True:
        params: dict[str, str] = {"page_size": "100", "state": state}
        if cursor:
            params["cursor"] = cursor

        payload = api_get(session, base_url, "/agents", params=params)
        page_agents = payload.get("data", [])
        if not isinstance(page_agents, list):
            raise SystemExit("Unexpected /agents response shape")

        agents.extend(page_agents)

        pagination = payload.get("meta", {}).get("pagination", {})
        if not pagination.get("has_more"):
            break

        cursor = pagination.get("next_cursor")
        if not cursor:
            break

    return agents


def path_slug(path_parts: tuple[str, ...]) -> str:
    return slugify(".".join(path_parts))


def extract_text_fields(
    node: Any,
    out_dir: Path,
    agent_id: str,
    safe_name: str,
    path: tuple[str, ...] = (),
) -> tuple[Any, list[str]]:
    extracted_paths: list[str] = []

    if isinstance(node, dict):
        out: dict[str, Any] = {}
        for key in sorted(node.keys()):
            value = node[key]

            if key in TEXT_FIELD_KEYS and isinstance(value, str) and value.strip():
                rel_file = (
                    Path("agent_text")
                    / "custom-instructions"
                    / f"{agent_id}-{safe_name}"
                    / f"{path_slug(path + (key,))}.md"
                )
                abs_file = out_dir / rel_file
                write_text(abs_file, value)
                out[key] = "[see separate markdown file]"
                out[f"{key}_file"] = str(rel_file)
                extracted_paths.append(str(rel_file))
                continue

            new_value, child_paths = extract_text_fields(
                value,
                out_dir,
                agent_id,
                safe_name,
                path + (key,),
            )
            out[key] = new_value
            extracted_paths.extend(child_paths)

        return out, extracted_paths

    if isinstance(node, list):
        out_list: list[Any] = []
        for idx, item in enumerate(node):
            new_value, child_paths = extract_text_fields(
                item,
                out_dir,
                agent_id,
                safe_name,
                path + (str(idx),),
            )
            out_list.append(new_value)
            extracted_paths.extend(child_paths)
        return out_list, extracted_paths

    return node, []


def first_items_text(items: Any, limit: int = 5) -> str:
    if not isinstance(items, list) or not items:
        return ""

    out: list[str] = []
    for item in items[:limit]:
        if isinstance(item, dict):
            label = item.get("name") or item.get("title") or item.get("key") or item.get("slug") or item.get("id")
            out.append(str(label))
        else:
            out.append(str(item))

    suffix = "" if len(items) <= limit else f" … (+{len(items) - limit} more)"
    return ", ".join(out) + suffix


def summarize_agent(
    agent_id: str,
    agent_name: str,
    agent: dict[str, Any],
    snapshot: dict[str, Any],
    extracted_text_files: list[str],
    versions_count: int,
) -> str:
    lines: list[str] = []
    title = agent_name or str(snapshot.get("name") or agent.get("name") or f"Agent {agent_id}")

    lines.append(f"# Neo agent export: {title}")
    lines.append("")
    lines.append(f"- Agent ID: `{agent_id}`")
    if agent_name:
        lines.append(f"- Export label: `{agent_name}`")

    status = snapshot.get("state") or agent.get("state")
    if status is not None:
        lines.append(f"- State: `{status}`")

    autonomy_type = snapshot.get("autonomy_type") or agent.get("autonomy_type")
    if autonomy_type is not None:
        lines.append(f"- Type: `{autonomy_type}`")

    trigger_type = snapshot.get("trigger_type") or agent.get("trigger_type")
    if trigger_type is not None:
        lines.append(f"- Trigger: `{trigger_type}`")

    entity_type = snapshot.get("entity_type") or agent.get("entity_type")
    if entity_type is not None:
        lines.append(f"- Entity: `{entity_type}`")

    if versions_count:
        lines.append(f"- Version records exported: `{versions_count}`")

    integrations = snapshot.get("integrations") or agent.get("integrations") or []
    if isinstance(integrations, list):
        lines.append(f"- Integrations: {len(integrations)}")
        sample = first_items_text(integrations)
        if sample:
            lines.append(f"- Integration sample: {sample}")

    toolbox = snapshot.get("toolbox") or agent.get("toolbox") or {}
    if isinstance(toolbox, dict):
        tool_settings = toolbox.get("tool_settings_by_type")
        if isinstance(tool_settings, dict):
            lines.append(f"- Tools configured: {len(tool_settings)}")
            lines.append(f"- Tool sample: {first_items_text([{'name': k} for k in tool_settings.keys()])}")

    if extracted_text_files:
        lines.append(f"- Extracted text files: {len(extracted_text_files)}")
        for file_path in extracted_text_files[:8]:
            lines.append(f"- `{file_path}`")
        if len(extracted_text_files) > 8:
            lines.append(f"- … (+{len(extracted_text_files) - 8} more)")

    lines.append("")
    lines.append("## Export contents")
    lines.append("")
    lines.append("- `agents/` = normalized agent records")
    lines.append("- `agent_snapshots/` = normalized resolved snapshots")
    lines.append("- `agent_versions/` = normalized version history")
    lines.append("- `agent_text/custom-instructions/` = extracted multiline instructions for clean diffs")
    lines.append("- `summaries/` = short human-readable summaries")
    lines.append("")
    lines.append(f"_Exported at {datetime.now(timezone.utc).isoformat()}_")
    return "\n".join(lines)


def export_one_agent(
    session: requests.Session,
    base_url: str,
    agent_stub: dict[str, Any],
    out_dir: Path,
    include_versions: bool,
) -> dict[str, Any]:
    agent_id = str(agent_stub["id"])
    safe_name = slugify(str(agent_stub.get("name") or f"agent-{agent_id}"))

    raw_agent = api_get(session, base_url, f"/agents/{agent_id}")
    agent_data = normalize(raw_agent.get("data", raw_agent))

    snapshot_timestamp = datetime.now(timezone.utc).isoformat()
    raw_snapshot = api_get(
        session,
        base_url,
        f"/agents/{agent_id}/version-at",
        params={"timestamp": snapshot_timestamp},
    )
    snapshot_data = normalize(raw_snapshot.get("data", raw_snapshot))

    agent_data, agent_text_files = extract_text_fields(agent_data, out_dir, agent_id, safe_name)
    snapshot_data, snapshot_text_files = extract_text_fields(snapshot_data, out_dir, agent_id, safe_name)

    versions_count = 0
    if include_versions:
        raw_versions = api_get(session, base_url, f"/agents/{agent_id}/versions")
        versions_data = normalize(raw_versions.get("data", raw_versions))
        versions_data, version_text_files = extract_text_fields(versions_data, out_dir, agent_id, safe_name)
        if isinstance(versions_data, list):
            versions_count = len(versions_data)
        write_json(out_dir / "agent_versions" / f"{agent_id}-{safe_name}.json", versions_data)
    else:
        version_text_files = []

    write_json(out_dir / "agents" / f"{agent_id}-{safe_name}.json", agent_data)
    write_json(out_dir / "agent_snapshots" / f"{agent_id}-{safe_name}.json", snapshot_data)

    summary = summarize_agent(
        agent_id=agent_id,
        agent_name=str(agent_stub.get("name") or ""),
        agent=agent_data,
        snapshot=snapshot_data,
        extracted_text_files=sorted(set(agent_text_files + snapshot_text_files + version_text_files)),
        versions_count=versions_count,
    )
    write_text(out_dir / "summaries" / f"{agent_id}-{safe_name}.md", summary)

    return {
        "id": agent_id,
        "name": agent_stub.get("name", ""),
        "state": agent_stub.get("state", ""),
        "autonomy_type": agent_stub.get("autonomy_type", ""),
        "entity_type": agent_stub.get("entity_type", ""),
        "trigger_type": agent_stub.get("trigger_type", ""),
        "agent_file": str(Path("agents") / f"{agent_id}-{safe_name}.json"),
        "snapshot_file": str(Path("agent_snapshots") / f"{agent_id}-{safe_name}.json"),
        "summary_file": str(Path("summaries") / f"{agent_id}-{safe_name}.md"),
        "versions_file": str(Path("agent_versions") / f"{agent_id}-{safe_name}.json") if include_versions else "",
        "versions_count": versions_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export every enabled Neo agent/workflow")
    parser.add_argument("--out", default="neo-backup", help="Output folder")
    parser.add_argument("--include-versions", action="store_true", help="Also export version history")
    parser.add_argument("--state", default="ENABLED", help="Agent state filter (default: ENABLED)")
    args = parser.parse_args()

    api_key = os.getenv("NEO_API_KEY")
    if not api_key:
        print("NEO_API_KEY is required", file=sys.stderr)
        return 2

    base_url = DEFAULT_BASE_URL
    out_dir = Path(args.out)

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
    )

    print(f"Fetching all agents with state={args.state}...")
    agent_stubs = list_all_agents(session, base_url, state=args.state)

    results: list[dict[str, Any]] = []
    state_counts = Counter()
    trigger_counts = Counter()
    type_counts = Counter()

    for stub in agent_stubs:
        print(f"Exporting {stub.get('id')} - {stub.get('name')}")
        result = export_one_agent(
            session=session,
            base_url=base_url,
            agent_stub=stub,
            out_dir=out_dir,
            include_versions=args.include_versions,
        )
        results.append(result)
        state_counts[result["state"]] += 1
        trigger_counts[result["trigger_type"]] += 1
        type_counts[result["autonomy_type"]] += 1

    manifest = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "base_url": base_url,
        "state_filter": args.state,
        "include_versions": args.include_versions,
        "agent_count": len(results),
        "counts_by_state": dict(state_counts),
        "counts_by_trigger_type": dict(trigger_counts),
        "counts_by_type": dict(type_counts),
        "agents": results,
    }
    write_json(out_dir / "manifest.json", manifest)

    print(f"Done. Exported {len(results)} enabled agents to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
