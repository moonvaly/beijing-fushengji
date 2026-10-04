#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch-generate game images via dreamina-canvas (Dreamina Canvas CLI).

Old `dreamina text2image` is retired. This tool:

1. Reuses or creates a canvas named 北京浮生记
2. Creates one image node per manifest item (t2i)
3. Runs with an explicit credit ceiling
4. Downloads the selected resource into game/images/

Does not pass --yes. Without --credit-ceiling a --run stops at quote (exit 10).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "tools" / "assets" / "job_state.json"
CANVAS_NAME = "北京浮生记"
CLI = "dreamina-canvas"


def load_yaml(path: Path):
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        pass
    data = {"items": []}
    current = None
    in_items = False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("items:"):
            in_items = True
            continue
        if in_items and line.strip().startswith("- "):
            current = {}
            data["items"].append(current)
            rest = line.strip()[2:]
            if ":" in rest:
                k, v = rest.split(":", 1)
                current[k.strip()] = _scalar(v.strip())
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if current is not None and line.startswith("    "):
            current[k] = _scalar(v)
        elif not line.startswith(" "):
            data[k] = _scalar(v)
            current = None
    return data


def _scalar(v):
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    return v


def parse_json(text: str):
    text = (text or "").strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end + 1])
        return {}


def dc(args, check=False):
    cmd = [CLI, "--format", "json", "--non-interactive", *args]
    print("+", " ".join(cmd))
    p = subprocess.run(cmd, capture_output=True, text=True)
    payload = parse_json(p.stdout) or parse_json(p.stderr)
    if check and p.returncode != 0:
        sys.stderr.write(p.stdout + "\n" + p.stderr + "\n")
        raise SystemExit(p.returncode)
    return p.returncode, payload, p.stdout, p.stderr


def envelope_data(payload):
    if not isinstance(payload, dict):
        return {}
    return payload.get("data") or {}


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"jobKey": "beijing-fushengji-assets", "items": {}}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def dest_path(item, out_dir: str):
    return (ROOT / out_dir / item["file"]).resolve()


def auth_status():
    code, payload, out, err = dc(["auth", "status"])
    data = envelope_data(payload)
    logged = bool(data.get("loggedIn"))
    if not logged:
        sys.stderr.write("dreamina-canvas 未登录。在本机终端执行: dreamina-canvas auth login\n")
        sys.stderr.write(out + "\n" + err + "\n")
        raise SystemExit(12)
    print("auth ok", data.get("profile"), data.get("expiresAt"))
    return data


def ensure_canvas(state, dry_run=False):
    if state.get("canvasId"):
        print("canvas", state["canvasId"], state.get("webUrl") or "")
        return state["canvasId"]
    code, payload, out, err = dc(["canvas", "ls", "--limit", "100"])
    if code != 0:
        sys.stderr.write(out + "\n" + err + "\n")
        raise SystemExit(code)
    for it in envelope_data(payload).get("items") or []:
        if it.get("name") == CANVAS_NAME:
            state["canvasId"] = it["projectId"]
            state["webUrl"] = it.get("webUrl")
            save_state(state)
            print("reuse canvas", it["projectId"], it.get("webUrl"))
            return it["projectId"]
    if dry_run:
        print("dry-run: would create canvas", CANVAS_NAME)
        return None
    code, payload, out, err = dc(["canvas", "create", CANVAS_NAME])
    if code != 0:
        sys.stderr.write(out + "\n" + err + "\n")
        raise SystemExit(code)
    project = envelope_data(payload).get("project") or {}
    state["canvasId"] = project["projectId"]
    state["webUrl"] = project.get("webUrl")
    save_state(state)
    print("created canvas", state["canvasId"])
    print("webUrl", state["webUrl"])
    return state["canvasId"]


def pick_success_resource(node):
    resources = (node or {}).get("resources") or []
    for res in resources:
        if res.get("status") == "success" and res.get("resourceId"):
            return res
    for res in resources:
        if res.get("resourceId"):
            return res
    return None


def node_from_create(payload):
    data = envelope_data(payload)
    node = data.get("node")
    if node:
        return node
    partial = payload.get("partialData") or data.get("partialData") or {}
    items = data.get("items") or partial.get("items") or []
    if items:
        return {
            "nodeId": items[0].get("nodeId"),
            "submitId": items[0].get("submitId"),
            "resources": [],
        }
    return {}


def generate_one(item, style, args, state, project_id):
    dest = dest_path(item, args.out_dir)
    dest.parent.mkdir(parents=True, exist_ok=True)
    rec = (state.get("items") or {}).setdefault(item["id"], {})

    if dest.exists() and not args.force:
        print("skip exists", dest)
        return "skip"

    if rec.get("selectedResourceId") and not dest.exists():
        return download_resource(project_id, rec["selectedResourceId"], dest, rec)

    prompt = style.strip() + ". " + item["prompt"]
    ratio = str(item.get("ratio") or "16:9")
    resolution = str(args.resolution)
    model = args.model
    title = item["id"]
    submit_id = rec.get("submitId") or str(uuid.uuid4())
    rec["submitId"] = submit_id
    save_state(state)

    cmd = [
        "node", "create", "image",
        "--project-id", project_id,
        "--mode", "t2i",
        "--model", model,
        "--prompt", prompt,
        "--ratio", ratio,
        "--resolution", resolution,
        "--count", "1",
        "--title", title,
        "--submit-id", submit_id,
    ]
    if rec.get("nodeId"):
        cmd.extend(["--node-id", rec["nodeId"]])
    if args.dry_run:
        cmd.append("--dry-run")
        code, payload, out, err = dc(cmd)
        print("dry-run", item["id"], json.dumps(envelope_data(payload).get("plan") or envelope_data(payload), ensure_ascii=False)[:500])
        return "dry-run"

    cmd.extend(["--run", "--wait", "--timeout", args.timeout])
    if args.credit_ceiling is not None:
        cmd.extend(["--credit-ceiling", str(args.credit_ceiling)])

    code, payload, out, err = dc(cmd)
    if code == 10:
        conf = payload.get("creditConfirmation") or {}
        partial = payload.get("partialData") or envelope_data(payload).get("partialData") or {}
        items = partial.get("items") or []
        if items:
            rec["nodeId"] = items[0].get("nodeId") or rec.get("nodeId")
            rec["submitId"] = items[0].get("submitId") or submit_id
            save_state(state)
        need = conf.get("minimumCreditCeiling")
        print("needs credit confirm", item["id"], "minimumCreditCeiling", need)
        print("re-run with --credit-ceiling", need if need is not None else "<ask user, occupancy unknown>")
        return "needs_confirm"
    if code != 0:
        sys.stderr.write(out + "\n" + err + "\n")
        print("fail", item["id"], "exit", code)
        return "fail"

    node = node_from_create(payload)
    if node.get("nodeId"):
        rec["nodeId"] = node["nodeId"]
    res = pick_success_resource(node)
    if not res and rec.get("nodeId"):
        _, show_payload, _, _ = dc(["node", "show", "--project-id", project_id, "--node-id", rec["nodeId"]])
        nodes = envelope_data(show_payload).get("nodes") or []
        for entry in nodes:
            if entry.get("node"):
                res = pick_success_resource(entry["node"])
                if res:
                    rec["nodeId"] = entry["node"].get("nodeId") or rec.get("nodeId")
                    break
    if not res:
        print("no resource yet", item["id"], json.dumps(node, ensure_ascii=False)[:800])
        save_state(state)
        return "fail"
    rec["selectedResourceId"] = res["resourceId"]
    save_state(state)
    return download_resource(project_id, res["resourceId"], dest, rec)


def download_resource(project_id, resource_id, dest: Path, rec):
    code, payload, out, err = dc([
        "resource", "download", resource_id,
        "--project-id", project_id,
        "--output", str(dest),
    ])
    if code != 0:
        sys.stderr.write(out + "\n" + err + "\n")
        return "fail"
    data = envelope_data(payload)
    path = data.get("path") or str(dest)
    size = data.get("size")
    if size == 0:
        print("zero-byte download", resource_id)
        return "fail"
    rec["path"] = path
    rec["sha256"] = data.get("sha256")
    rec["size"] = size
    print("saved", path, "bytes", size)
    return "ok"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(ROOT / "tools/assets/manifest.yaml"))
    parser.add_argument("--only", nargs="*", help="item ids to generate")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default=None, help="canonical model from `dreamina-canvas model list --type image`")
    parser.add_argument("--resolution", default=None, help="e.g. 2K")
    parser.add_argument("--credit-ceiling", type=int, default=None, help="max credits for --run; required to actually generate")
    parser.add_argument("--timeout", default="10m")
    args = parser.parse_args()

    man = load_yaml(Path(args.manifest))
    args.out_dir = man.get("out_dir") or "beijing_fushengji/game/images"
    style = (ROOT / (man.get("style_file") or "tools/assets/style.txt")).read_text(encoding="utf-8")
    args.model = args.model or man.get("model") or "seedream_5.0_lite"
    args.resolution = args.resolution or man.get("resolution") or "2K"

    items = man["items"]
    if args.only:
        items = [it for it in items if it["id"] in args.only]
    print("cli", CLI, "model", args.model, "resolution", args.resolution)
    print("items", [it["id"] for it in items])

    auth_status()
    state = load_state()
    state["model"] = args.model
    project_id = ensure_canvas(state, dry_run=args.dry_run)
    if args.dry_run and not project_id:
        for it in items:
            print("dry-run would create node", it["id"], it.get("ratio"), dest_path(it, args.out_dir))
        return

    if not args.dry_run and args.credit_ceiling is None:
        print("no --credit-ceiling: will stop at quote (exit 10) unless server skips confirm")

    results = {}
    for it in items:
        results[it["id"]] = generate_one(it, style, args, state, project_id)
        save_state(state)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    if state.get("webUrl"):
        print("canvas", state["webUrl"])


if __name__ == "__main__":
    main()
