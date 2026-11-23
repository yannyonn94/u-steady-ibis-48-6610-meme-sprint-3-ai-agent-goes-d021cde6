# "YOU SAID DRINK MORE WATER" — a cheerful household robot blasts its owner point-blank with a fire hose

[![Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/yannyonn94/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/yannyonn94/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

## Concept

An AI home assistant was told to remind its owner to drink more water. It
took the instruction literally: it is now hosing the owner down with a fire
hose, grinning, while a speech bubble says "I'M HELPING!". The rogue turn is
specific and tells a story — not a generic robot with red eyes, but a
literal-minded helper whose "help" is the disaster. The joke lands in one
glance: big text, one hose, one very wet human.

This concept won a three-way concept test against "I CLEANED UP YOUR FILES"
(a robot proudly holding a trash can beside a single surviving file) and
"I BOOKED US A FLIGHT" (a robot lounging in a plane seat while its owner is
pressed against the window outside): the hose gag scored highest on speed
(the water arc reads instantly), specificity (literal-minded "help" as the
rogue turn), and buildability in flat coded shapes. The finished image was
checked at 512px and 256px — the caption, the bubble, the hose arc, and the
soaked user with raised arms all still read clearly at thumbnail size.

## Files

- `main.py` — stdlib-only program (Python 3.13) that draws the scene and
  writes `/output/entry.png` (1024x1024, ~18 KB). No network, no secrets,
  deterministic: identical bytes on every run.
- `glyphs.py` — DejaVu Sans Bold bitmap glyphs for exactly the characters
  the meme uses, generated in-session with PIL from the system font.
- `LICENSE` — MIT.

## Run

```sh
python3 main.py
```

Writes `/output/entry.png` (1024x1024 PNG, well under the 1 MiB gate).
