#!/usr/bin/env python3
"""Build a synthetic $HOME under demo/home so the README demo GIF can show the picker
with realistic — but entirely fake — sessions. No real prompts or paths are ever recorded.

The tape does:  HOME=$PWD/demo/home  python3 sessions.py <DEMO_CWD>

Run from anywhere: it writes relative to this file, not the cwd.
"""
import json
import os
import shutil
import sqlite3
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.join(HERE, "home")
# The folder the picker is "opened on". It MUST exist (the picker guards with os.path.isdir),
# so the fixture creates it. /tmp keeps it generic — no username leaks into the GIF.
DEMO_CWD = "/tmp/acme-api"

DAY = 86400
NOW = time.time()


def encode_cwd(path):
    return "".join(ch if ch.isalnum() else "-" for ch in os.path.realpath(path))


def write(path, lines, mtime):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for obj in lines:
            f.write(json.dumps(obj) + "\n")
    os.utime(path, (mtime, mtime))


def claude(uuid, first, extra_turns, mtime, title=None):
    proj = os.path.join(HOME, ".claude", "projects", encode_cwd(DEMO_CWD))
    lines = []
    if title:
        lines.append({"type": "custom-title", "customTitle": title})
    lines.append({"type": "user", "message": {"content": first}})
    for i in range(extra_turns):
        lines.append({"type": "assistant", "message": {"content": "…"}})
        lines.append({"type": "user", "message": {"content": "…"}})
    write(os.path.join(proj, uuid + ".jsonl"), lines, mtime)


def codex(uuid, first, extra_turns, mtime, nickname=None):
    d = os.path.join(HOME, ".codex", "sessions", "2026", "07", "02")
    lines = [{"type": "session_meta",
              "payload": {"id": uuid, "cwd": DEMO_CWD, "agent_nickname": nickname}}]
    lines.append({"type": "response_item", "payload": {"role": "user", "content": first}})
    for i in range(extra_turns):
        lines.append({"type": "response_item", "payload": {"role": "user", "content": "…"}})
    write(os.path.join(d, f"rollout-2026-07-02T09-18-00-{uuid}.jsonl"), lines, mtime)


def copilot(sessions):
    db = os.path.join(HOME, ".copilot", "session-store.db")
    os.makedirs(os.path.dirname(db), exist_ok=True)
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE sessions (id TEXT, cwd TEXT, summary TEXT, updated_at TEXT)")
    con.execute("CREATE TABLE turns (session_id TEXT, turn_index INTEGER, user_message TEXT)")
    cwd = os.path.realpath(DEMO_CWD)   # list_copilot matches on realpath(folder)
    for sid, summary, updated, turns in sessions:
        con.execute("INSERT INTO sessions VALUES (?,?,?,?)", (sid, cwd, summary, updated))
        for i, msg in enumerate(turns):
            con.execute("INSERT INTO turns VALUES (?,?,?)", (sid, i, msg))
    con.commit()
    con.close()


def gemini(uuid, first, extra_turns, mtime):
    project = "acme-api"
    project_dir = os.path.join(HOME, ".gemini", "tmp", project)
    chats = os.path.join(project_dir, "chats")
    os.makedirs(chats, exist_ok=True)
    with open(os.path.join(project_dir, ".project_root"), "w", encoding="utf-8") as f:
        f.write(os.path.realpath(DEMO_CWD))
    short = uuid[:8]
    lines = [{
        "sessionId": uuid,
        "projectHash": "demo",
        "startTime": iso(mtime),
        "lastUpdated": iso(mtime),
        "kind": "main",
    }]
    lines.append({"type": "user", "content": [{"text": first}]})
    for i in range(extra_turns):
        lines.append({"type": "gemini", "content": "…"})
        lines.append({"type": "user", "content": [{"text": "…"}]})
    write(os.path.join(chats, f"session-2026-07-02T10-20-{short}.jsonl"), lines, mtime)


def iso(mtime):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(mtime))


def main():
    shutil.rmtree(HOME, ignore_errors=True)
    os.makedirs(DEMO_CWD, exist_ok=True)   # the picker requires the folder to exist

    claude("44a489e0-1111-2222-3333-444455556666",
           "boot up the apple skill and show me what's left in the queue", 35,
           NOW - 12 * 60, title="apple skill boot")
    claude("7b2c10de-aaaa-bbbb-cccc-ddddeeeeffff",
           "why does the curses layout wrap at 80 columns on the small terminal?", 8,
           NOW - 40 * 60)
    claude("019da930-2020-4040-6060-808080808080",
           "refactor the picker to add an incremental search mode", 20,
           NOW - 34 * DAY)

    codex("cf19aa22-7777-8888-9999-000011112222",
          "study this folder and explain how the build system is wired", 5,
          NOW - 2 * DAY, nickname="build-scout")

    gemini("66f681eb-7002-40f4-83f6-83db37b713fb",
           "check whether the API retry handling covers rate limits", 6,
           NOW - 90 * 60)

    copilot([
        ("e9ee0f44-3333-1111-5555-777799990000",
         "Renoise plugin pricing table",
         iso(NOW - 3 * 3600),
         ["check the Renoise plugin pricing table and summarise the tiers", "…", "…"]),
    ])

    print("wrote synthetic $HOME →", HOME)
    print("demo cwd →", DEMO_CWD)


if __name__ == "__main__":
    main()
