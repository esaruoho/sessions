# sessions

A single-file Python TUI session picker for the three coding-agent CLIs:

- **Claude Code** (`claude`)
- **GitHub Copilot CLI** (`copilot`)
- **OpenAI Codex CLI** (`codex`)

Run it on any folder. It lists every session any of the three agents has
recorded for that folder — newest first, with calendar timestamp, age,
turn count, on-disk size, and the first user message. Pick one with the
arrow keys, hit Enter, and it resumes that session with the right CLI and
the right flags. The list auto-refreshes every 1.5 seconds.

## Install

Stdlib-only. No `pip`, no Homebrew, no Node.

```
git clone https://github.com/esaruoho/sessions ~/work/sessions
ln -s ~/work/sessions/sessions.py ~/.local/bin/sessions
chmod +x ~/work/sessions/sessions.py
```

Requires Python 3.11+ (uses `datetime.fromisoformat` with `Z` handling).

## Usage

```
sessions                 # picker for the current directory
sessions ~/work/paketti  # picker for that folder
```

Keys:

| key | action |
|---|---|
| `↑` / `↓` (or `j` / `k`) | move selection |
| `Enter` | resume the selected session |
| `n` | start a new Claude session in this folder |
| `c` | start a new Copilot session in this folder |
| `x` | start a new Codex session in this folder |
| `q` / `Esc` / `Ctrl-C` | quit |

Resume invocations:

- Claude → `claude --dangerously-skip-permissions --resume <uuid>`
- Copilot → `copilot --resume=<uuid>`
- Codex → `codex resume <uuid>`

## What each row looks like

```
 C  today 14:32   7m    36t   393K  boot up apple skill. see how the bbs-app…   44a489
 G  today 09:11   3h    45t      ·  Check Paketti Renoise Copilot Pricing       e9ee0f
 X  04-20 09:18   1mo    2t   356K  please study this folder and tell me why…  019da9
```

Columns: provider glyph (`C` = Claude, `G` = Copilot, `X` = Codex) ·
calendar timestamp · relative age · message turns · on-disk size ·
first user message · short uuid (dim).

## How it finds your sessions

| provider | store | match on folder |
|---|---|---|
| Claude | `~/.claude/projects/<encoded-cwd>/<uuid>.jsonl` | `realpath(folder)` then every non-alphanumeric char → `-`, matching Claude's own encoding (works for iCloud-symlinked projects) |
| Copilot | `~/.copilot/session-store.db` | SQL `WHERE cwd = realpath(folder)` |
| Codex | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | parse `session_meta` line 1, match `cwd`, skip subagent rollouts |

## Why a single file

If a tool needs more than one file you have to install it. This one you
read, copy, symlink — done. The whole thing is stdlib (curses, sqlite3,
json, os, time) so there's nothing to vendor and nothing to break when
Python or the agent CLIs update.

## Origin

Extracted from the [esaruoho/apple](https://github.com/esaruoho/apple)
skill collection, where it lives at `bin/sessions` alongside `~/work/apple`'s
65 other Apple-native CLI tools and its `/sessions [folder]` slash command
for Claude Code. That repo is the source of truth for personal Apple-native
automation; this repo carries `sessions` on its own so anyone juggling more
than one coding-agent CLI can use it without cloning the whole apple skill.

When the apple repo's copy diverges, this one is the version to follow.

## License

MIT.
