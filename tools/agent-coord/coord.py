# -*- coding: utf-8 -*-
"""agent-coord: a small coordination CLI for several AI agents sharing one workspace.

Reference implementation for .claude/rules/multi-agent-coordination.md.
Pure standard library, Python 3.8+, works on Windows, macOS and Linux.

Subcommands
  init                         create the coordination directory and a default config
  status                       baseline, lease, recent registry entries, on-disk artifacts
  claim   --agent A --task T   acquire the write lease (exclusive create); exit 1 on conflict
  release --agent A            release your lease
  next-rev --agent A           allocate the next revision number (scan deliverables + archive, locked)
  log     --agent A --action X [--artifact P ...] [--baseline rNN]
                               append to REGISTRY.jsonl; with --baseline also update STATE.json
  doctor                       consistency checks; exit 1 when anything needs attention

Design
  - REGISTRY.jsonl is append-only, so concurrent sessions never overwrite each other's entries.
  - The lease is created with O_CREAT|O_EXCL, a filesystem-level mutex. Takeovers are logged.
  - Every check trusts the disk, not text that an agent remembers.

Exit codes: 0 ok, 1 conflict or doctor findings, 2 usage or configuration error.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import time

CONFIG_NAME = "coord.config.json"
DEFAULT_CONFIG = {
    "coord_dir": ".coord",
    "deliverables_dir": "deliverables",
    "archive_dirs": ["archive"],
    "revision_pattern": r"[-_]r(\d+)",
    "artifact_extensions": [".docx", ".pdf", ".md", ".tex", ".pptx", ".xlsx"],
    "agents": [],
    "lease_ttl_minutes": 90,
    "mirror_pairs": [["AGENTS.md", "CLAUDE.md"]],
    "allowed_top_level": [],
}
STALE_LOCK_SECONDS = 600

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


class Workspace:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        cfg_path = os.path.join(self.root, CONFIG_NAME)
        self.cfg = dict(DEFAULT_CONFIG)
        self.has_config = os.path.exists(cfg_path)
        if self.has_config:
            with open(cfg_path, "r", encoding="utf-8") as f:
                self.cfg.update(json.load(f))
        self.coord = os.path.join(self.root, self.cfg["coord_dir"])
        self.state = os.path.join(self.coord, "STATE.json")
        self.registry = os.path.join(self.coord, "REGISTRY.jsonl")
        self.lease = os.path.join(self.coord, "LEASE.json")
        self.revlock = os.path.join(self.coord, ".revalloc.lock")
        self.front = os.path.join(self.root, self.cfg["deliverables_dir"])
        self.rev_re = re.compile(self.cfg["revision_pattern"])

    # ---------------------------------------------------------------- storage
    def read_registry(self, limit=None):
        rows = []
        if os.path.exists(self.registry):
            with open(self.registry, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rows.append(json.loads(line))
                    except ValueError:
                        rows.append({"ts": "?", "agent": "?", "action": "unparseable: " + line[:80]})
        return rows[-limit:] if limit else rows

    def append(self, entry):
        os.makedirs(self.coord, exist_ok=True)
        entry = dict({"ts": now()}, **entry)
        with open(self.registry, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def load_json(self, path):
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except ValueError:
            return {"_error": "unparseable " + os.path.basename(path)}

    def load_lease(self):
        lease = self.load_json(self.lease)
        if lease and "_error" in lease:
            return {"agent": "?", "task": lease["_error"], "expires": "1970-01-01 00:00:00"}
        return lease

    @staticmethod
    def expired(lease):
        try:
            return datetime.datetime.now() > datetime.datetime.strptime(lease["expires"], "%Y-%m-%d %H:%M:%S")
        except (KeyError, ValueError):
            return True

    # ---------------------------------------------------------------- disk scan
    def front_artifacts(self):
        out = []
        if not os.path.isdir(self.front):
            return out
        exts = tuple(e.lower() for e in self.cfg["artifact_extensions"])
        for name in sorted(os.listdir(self.front)):
            p = os.path.join(self.front, name)
            if os.path.isfile(p) and name.lower().endswith(exts) and not name.startswith("~$"):
                m = self.rev_re.search(name)
                out.append((name, int(m.group(1)) if m else None, sha256(p)))
        return out

    def max_revision(self):
        best = max([r for _, r, _ in self.front_artifacts() if r] or [0])
        for d in self.cfg["archive_dirs"]:
            base = os.path.join(self.root, d)
            if not os.path.isdir(base):
                continue
            for dirpath, dirnames, filenames in os.walk(base):
                for name in dirnames + filenames:
                    for m in self.rev_re.finditer(name):
                        best = max(best, int(m.group(1)))
        return best


def check_agent(ws, agent):
    allowed = ws.cfg.get("agents") or []
    if allowed and agent not in allowed:
        print("Unknown agent %r. Allowed: %s" % (agent, ", ".join(allowed)))
        sys.exit(2)


# -------------------------------------------------------------------- commands
def cmd_init(ws, args):
    os.makedirs(ws.coord, exist_ok=True)
    cfg_path = os.path.join(ws.root, CONFIG_NAME)
    if not os.path.exists(cfg_path):
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        print("Created %s" % CONFIG_NAME)
    if not os.path.exists(ws.state):
        with open(ws.state, "w", encoding="utf-8") as f:
            json.dump({"baseline": None, "sha256": None, "updated": now(), "by": "init"}, f, indent=2)
    ws.append({"agent": "init", "action": "coordination layer initialised", "kind": "init"})
    print("Coordination directory: %s" % ws.coord)
    return 0


def cmd_status(ws, args):
    print("=== agent-coord status | %s ===" % now())
    lease = ws.load_lease()
    if lease is None:
        print("Lease: free")
    else:
        tag = "EXPIRED, can be taken over" if ws.expired(lease) else "active"
        print("Lease: held by %s [%s] - %s (until %s)" % (lease.get("agent"), tag, lease.get("task"), lease.get("expires")))
    state = ws.load_json(ws.state) or {}
    print("Baseline: %s  sha256=%s  updated=%s by %s" % (
        state.get("baseline"), (state.get("sha256") or "-")[:16], state.get("updated"), state.get("by")))
    print("Deliverables on disk:")
    arts = ws.front_artifacts()
    for name, rev, digest in arts:
        print("  %-50s r%-4s %s" % (name, rev if rev is not None else "-", digest[:16]))
    if not arts:
        print("  (none)")
    print("Recent registry entries:")
    for r in ws.read_registry(5):
        print("  [%s] %-12s %s" % (r.get("ts"), r.get("agent"), r.get("action")))
    return 0


def cmd_claim(ws, args):
    check_agent(ws, args.agent)
    os.makedirs(ws.coord, exist_ok=True)
    lease = ws.load_lease()
    if lease is not None:
        if not ws.expired(lease) and not args.force:
            print("CONFLICT: lease held by %s until %s - %s" % (lease.get("agent"), lease.get("expires"), lease.get("task")))
            print("Stop here. Use --force only after confirming the holder has stopped; takeovers are logged.")
            return 1
        reason = "expired-takeover" if ws.expired(lease) else "forced-takeover"
        ws.append({"agent": args.agent, "action": "%s of lease from %s" % (reason, lease.get("agent")),
                   "kind": reason, "task": args.task})
        os.remove(ws.lease)
    ttl = args.ttl or ws.cfg["lease_ttl_minutes"]
    expires = (datetime.datetime.now() + datetime.timedelta(minutes=ttl)).strftime("%Y-%m-%d %H:%M:%S")
    payload = {"agent": args.agent, "task": args.task, "since": now(), "expires": expires, "pid": os.getpid()}
    try:
        fd = os.open(ws.lease, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        print("CONFLICT: another session acquired the lease a moment ago. Run status.")
        return 1
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    ws.append({"agent": args.agent, "action": "claim: " + args.task, "kind": "claim", "expires": expires})
    print("Claimed until %s." % expires)
    return 0


def cmd_release(ws, args):
    check_agent(ws, args.agent)
    lease = ws.load_lease()
    if lease is None:
        print("No lease to release.")
        return 0
    if lease.get("agent") != args.agent and not args.force:
        print("Lease belongs to %s, not %s. Use --force to release anyway." % (lease.get("agent"), args.agent))
        return 1
    os.remove(ws.lease)
    ws.append({"agent": args.agent, "action": "release: " + str(lease.get("task")), "kind": "release"})
    print("Released.")
    return 0


def cmd_next_rev(ws, args):
    check_agent(ws, args.agent)
    os.makedirs(ws.coord, exist_ok=True)
    if os.path.exists(ws.revlock) and time.time() - os.path.getmtime(ws.revlock) > STALE_LOCK_SECONDS:
        os.remove(ws.revlock)
        ws.append({"agent": args.agent, "action": "removed stale revision lock", "kind": "lock-heal"})
    try:
        fd = os.open(ws.revlock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        print("Revision allocator is busy (another session is allocating). Retry shortly.")
        return 1
    try:
        allocated = [e.get("rev") for e in ws.read_registry() if e.get("kind") == "rev-alloc"]
        nxt = max([ws.max_revision()] + [r for r in allocated if isinstance(r, int)]) + 1
        ws.append({"agent": args.agent, "action": "allocated r%d" % nxt, "kind": "rev-alloc", "rev": nxt})
    finally:
        os.close(fd)
        os.remove(ws.revlock)
    print("r%d" % nxt)
    return 0


def cmd_log(ws, args):
    check_agent(ws, args.agent)
    entry = {"agent": args.agent, "action": args.action, "kind": "log"}
    arts = []
    for p in args.artifact or []:
        full = p if os.path.isabs(p) else os.path.join(ws.root, p)
        exists = os.path.isfile(full)
        arts.append({"path": p, "exists": exists, "sha256": sha256(full) if exists else None})
    if arts:
        entry["artifacts"] = arts
    if args.baseline:
        entry["baseline"] = args.baseline
    ws.append(entry)
    if args.baseline:
        first = next((a for a in arts if a["exists"]), None)
        with open(ws.state, "w", encoding="utf-8") as f:
            json.dump({"baseline": args.baseline, "sha256": first["sha256"] if first else None,
                       "artifact": first["path"] if first else None,
                       "updated": now(), "by": args.agent, "action": args.action}, f, ensure_ascii=False, indent=2)
        print("Logged; baseline set to %s." % args.baseline)
    else:
        print("Logged.")
    missing = [a["path"] for a in arts if not a["exists"]]
    if missing:
        print("WARNING: artifact not found on disk: %s" % ", ".join(missing))
        return 1
    return 0


def cmd_doctor(ws, args):
    problems, notes = [], []
    if not ws.has_config:
        notes.append("no %s found; defaults in use (run init)" % CONFIG_NAME)
    if not os.path.isdir(ws.coord):
        problems.append("coordination directory is missing: %s" % ws.cfg["coord_dir"])

    allowed = ws.cfg.get("allowed_top_level") or []
    if allowed:
        for name in sorted(os.listdir(ws.root)):
            if name not in allowed and name not in (CONFIG_NAME, ws.cfg["coord_dir"]):
                problems.append("top-level item not in allowed_top_level: %s" % name)

    for pair in ws.cfg.get("mirror_pairs") or []:
        paths = [os.path.join(ws.root, p) for p in pair]
        present = [p for p in paths if os.path.isfile(p)]
        if len(present) == len(paths) and len({sha256(p) for p in paths}) > 1:
            problems.append("mirrored entry files have diverged: %s" % " vs ".join(pair))

    state = ws.load_json(ws.state) or {}
    arts = ws.front_artifacts()
    if state.get("sha256") and arts and all(state["sha256"] != d for _, _, d in arts):
        problems.append("STATE sha256 matches no deliverable on disk: someone changed a file without logging")
    m = re.match(r"r(\d+)$", str(state.get("baseline") or ""))
    front_max = max([r for _, r, _ in arts if r] or [0])
    if m and front_max > int(m.group(1)):
        problems.append("deliverables contain r%d but STATE baseline is %s: log it with --baseline r%d"
                        % (front_max, state.get("baseline"), front_max))
    if len(arts) > 1:
        notes.append("%d deliverables present; confirm they are intended parallel candidates" % len(arts))

    lease = ws.load_lease()
    if lease and ws.expired(lease):
        notes.append("lease held by %s expired at %s" % (lease.get("agent"), lease.get("expires")))
    if os.path.exists(ws.revlock):
        notes.append("revision lock present; it will self-heal after %d s" % STALE_LOCK_SECONDS)

    print("=== agent-coord doctor | %s ===" % now())
    for n in notes:
        print("  note: " + n)
    for p in problems:
        print("  PROBLEM: " + p)
    print("result: %s" % ("%d problem(s)" % len(problems) if problems else "all checks passed"))
    return 1 if problems else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Coordination CLI for multiple AI agents in one workspace.")
    ap.add_argument("--root", default=os.environ.get("AGENT_COORD_ROOT", "."), help="workspace root (default: .)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("init", cmd_init), ("status", cmd_status), ("doctor", cmd_doctor)):
        sub.add_parser(name).set_defaults(func=fn)
    p = sub.add_parser("claim")
    p.add_argument("--agent", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--ttl", type=int)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_claim)
    p = sub.add_parser("release")
    p.add_argument("--agent", required=True)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_release)
    p = sub.add_parser("next-rev")
    p.add_argument("--agent", required=True)
    p.set_defaults(func=cmd_next_rev)
    p = sub.add_parser("log")
    p.add_argument("--agent", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--artifact", action="append")
    p.add_argument("--baseline")
    p.set_defaults(func=cmd_log)
    args = ap.parse_args(argv)
    return args.func(Workspace(args.root), args)


if __name__ == "__main__":
    sys.exit(main())
