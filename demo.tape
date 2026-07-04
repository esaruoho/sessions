# demo.tape — a "recorded-terminal GIF" of the picker for the README banner.
#
# charmbracelet/vhs spins up a headless terminal, TYPES these commands, and records a
# deterministic GIF (no live screen-capture of a real session — the data is synthetic).
#
# Regenerate (run from the repo root):
#   brew install vhs                 # https://github.com/charmbracelet/vhs
#   vhs demo.tape                    # → demo.gif
#
# demo/make-fixture.py builds a fake $HOME with a handful of FAKE sessions across all three
# agents (Claude / Copilot / Codex) so the picker has something realistic — but private-data
# free — to show. It runs inside the Hidden block so the ages ("12m", "3h", …) are fresh.

Output demo.gif

Set Shell bash
Set FontSize 20
Set Width 1320
Set Height 560
Set Padding 20
Set Theme "Builtin Solarized Dark"

Hide
Type "python3 demo/make-fixture.py >/dev/null && export HOME=$PWD/demo/home && clear"
Enter
Sleep 500ms
Show

Type "python3 sessions.py /tmp/acme-api"
Sleep 500ms
Enter
Sleep 2500ms

Down@600ms 3
Sleep 1200ms
Up@600ms 1
Sleep 1500ms

Type "q"
Sleep 900ms
