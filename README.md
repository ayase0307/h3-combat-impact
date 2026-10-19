<p align="center">
  <img src="assets/hero.jpg" alt="Two wuxia swordfighters at the instant of contact: white-hot spark bloom, teal and amber shockwave, robes whipped by air pressure" width="100%">
</p>

<h1 align="center">h3-combat-impact</h1>

<p align="center">
  <b>Agent Skill that makes MiniMax H3 / Hailuo fights <i>hit</i>: impact beats, named moves, force fields, impact frames, screen shake.</b>
</p>

<p align="center">
  <b>English</b> · <a href="README.zh-TW.md">繁體中文</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/agent-skill-8A2BE2">
  <img alt="MiniMax H3" src="https://img.shields.io/badge/MiniMax-H3%20%2F%20Hailuo-ff5a36">
  <img alt="Zero dependencies" src="https://img.shields.io/badge/scripts-stdlib%20%2B%20ffmpeg-0a7">
  <img alt="Measured" src="https://img.shields.io/badge/7%20runs-measured-2ea44f">
</p>

---

## Why this skill

AI fight clips usually fail in the same ways: the action is soft, the VFX is a glowing sticker, two characters pose like wooden dolls, the camera jitters, and the last two seconds just stand there. "Epic explosion" does not fix any of that.

This skill turns "make it hit harder" into a structure you can write, copy and **measure**:

- **Six-beat impact.** Every hit is anticipation → contact → hit stop → release → reaction → recovery, with a time budget per beat.
- **Force field, not glow.** Four channels (light / air / matter / particles). The cheapest proof of power is a robe or a strand of hair being pushed.
- **Named moves.** 16 moves with four layers each (displacement, body mechanics, physical result, tactical purpose) so the model stops averaging into "swing, block, retreat".
- **Exchange · compression · consequence.** Three design rules that matter more than any prompt wording.
- **Output you can paste.** The final answer is one code block in the official H3 three-field format, checked by a validator script.
- **Measured, not felt.** `measure_motion.py` scores the generated mp4 for dead openings, stalled endings and motion lulls.

## The six beats

<p align="center">
  <img src="assets/six-beat.jpg" alt="One sword strike split into six panels: anticipation 35%, contact 5%, hit stop 15%, release 25%, reaction 15%, recovery 5%" width="92%"><br>
  <sub>One strike, six beats, and the share of time each one gets. No wind-up, no weight.</sub>
</p>

| Beat | Share | What the frame needs | Prompt key phrase |
|---|---:|---|---|
| 1 Anticipation | 35% | counter-motion, weight sinks, cloth tightens | `weight sinks into the rear leg` |
| 2 Contact | 5% | **impact frame**: 1–2 frames of white-out / black-out | `for two frames the entire frame blows out to pure white` |
| 3 Hit stop | 15% | time almost freezes, dust and sparks hang | `decelerates to a near-freeze for two frames` |
| 4 Release | 25% | shockwave, debris, dust ring, light shift | `a ring of shockwave dust bursts outward` |
| 5 Reaction | 15% | defender hurled back, delayed cloth and hair, **decaying shake** | `the shake decays within a third of a second` |
| 6 Recovery | 5% | back to guard, embers fall, camera steadies | `settles into a low guard` |

Rules of thumb: anticipation ≥ 5× contact; hit stop is the *only* source of weight; one visual climax per hit. For non-stop brawls there is a separate four-beat mode with no freeze ([`continuous-brawl.md`](references/continuous-brawl.md)).

## Force field: glow is just colour

<p align="center">
  <img src="assets/force-field.jpg" alt="Explosion core with four radiating channels: light, air, matter, particles" width="92%"><br>
  <sub>Open at most three channels per hit. Priority: air &gt; matter &gt; light &gt; particles.</sub>
</p>

```text
✗  epic explosion, glowing shockwave
✓  wind pressure flattens the silk against her body, the air ripples in a heat-haze ring,
   roof tiles rattle loose
```

## Seen on real generations

Both clips below are my own H3 test runs, scored with the bundled script.

<table>
  <tr>
    <td align="center" width="55%"><img src="assets/demo-before-v01.gif" alt="V01: static opening"><br><sub><b>V01 · first draft</b> · opening 3.24 · flag: <code>opening too static</code></sub></td>
    <td align="center" width="45%"><img src="assets/demo-after-v06.gif" alt="V06: rules applied"><br><sub><b>V06 · rules applied</b> · opening 20.44 · zero flags</sub></td>
  </tr>
</table>

<p align="center"><img src="assets/strip-v06.jpg" alt="Frame strip of V06 at 2 fps" width="90%"><br><sub>V06 at 2 fps. Different subject and aspect ratio from V01; the point is the motion curve, not a like-for-like swap.</sub></p>

### Same subject, before vs after the skill

<p align="center"><img src="assets/demo-ab-skill.gif" alt="Side-by-side animated comparison: before the skill rules versus after" width="88%"><br>
<sub><b>Same subject, same first frame, same 9:16, same 8 s.</b> Left: written without the skill. Right: written with it.<br>
End-of-clip motion 57% → 93%; the tail-stall and static-symmetry flags are gone.</sub></p>

| | Before | After |
|---|---:|---:|
| Whole-clip motion | 18.43 | **21.89** |
| End 2 s ÷ middle | 57% | **93%** |
| Longest lull | 0.33 s | 0.29 s |
| Flags | tail stall, static symmetry | **none** |

> **Honest caveat:** the two runs use different random seeds, so this is a matched-composition comparison, not a single-variable controlled test. The new A/B workflow below fixes the seed, so future comparisons are strictly controlled.

| Run | Words | Shots | Opening 0.8 s | End 2 s ÷ middle | Longest lull | Flags |
|---|---:|---:|---:|---:|---:|---|
| V01 | 525 | 4 | 3.24 | 80% | 0.17 s | opening too static |
| V02 | 667 | 4 | 23.59 | 32% | 1.17 s | stalled ending, lull |
| V04 | 885 | 5 | 18.12 | 27% | 0.17 s | stalled ending (generated 10.1 s, prompt said 8 s) |
| **V06** | **1022** | **5** | **20.44** | **108%** | **0.04 s** | **none** |

What the data changed: a wrong duration setting causes stalled endings more than wording does, and one sentence, `First contact occurs within the opening half-second.`, took the opening from 3.24 to 20.44. The score measures *frame change*, so VFX can inflate it; always check by eye that the subject moves.

## After a skill update, prove it

**Every rule change ships with a before/after pair.** Same subject, same seed, same everything — only the prompt differs — then the two clips are scored and rendered as one animated comparison on this page.

```bash
# 1. run both prompt versions through the local H3
python analysis/submit_ab.py --before before.txt --after after.txt \
    --label-before "A · before skill" --label-after "B · after skill" \
    --width 960 --height 544 --seconds 8 --quality light --seed 20261019

# 2. score + render the side-by-side animated comparison
python scripts/compare_clips.py --before before.mp4 --after after.mp4 \
    --out compare.gif --label-before "A · before skill" --label-after "B · after skill" \
    --width 240 --fps 8 --colors 64 --dither-scale 3
```

`compare_clips.py` prints the motion-metric table for both clips, so the numbers on this page are reproducible rather than asserted.

## Install

```bash
git clone https://github.com/ayase0307/h3-combat-impact ~/.claude/skills/h3-combat-impact
```

Works with any agent that reads `SKILL.md` skills (Claude Code, Codex, …). Windows: clone into `%USERPROFILE%\.claude\skills\`.

Then ask in plain language:

> *"Write an H3 prompt for a 8-second rooftop duel, it feels floaty, make it hit."*
> *"Break this fight clip down and recreate it in H3 format."*

## Tools

```bash
# format check before you paste into the model (FAIL must be fixed)
python scripts/validate_prompt.py prompt.txt --duration 8

# motion curve of generated clips (needs ffmpeg on PATH)
python scripts/measure_motion.py --dir ./outputs
python scripts/measure_motion.py --dir ./outputs --symmetry   # flags "static symmetric" hero poses
```

| Metric | Pass |
|---|---|
| Opening 0.8 s | ≥ 50% of middle |
| End 2 s ÷ middle | ≥ 60% |
| Longest lull | ≤ 0.8 s |
| Peaks | ≥ 4 |

## What's inside

| File | Covers |
|---|---|
| [`SKILL.md`](SKILL.md) | Schema, six-beat method, force field, design rules, measurable rules, workflow |
| [`references/output-format.md`](references/output-format.md) | Official 3-field / 6-field contract, alignment line, dialogue tags, common mistakes |
| [`references/impact-design.md`](references/impact-design.md) | Beat detail, power tiers, material reactions, timing budgets |
| [`references/move-library.md`](references/move-library.md) | 16 named moves, 4 three-move chains, EN/ZH translation rules |
| [`references/continuous-brawl.md`](references/continuous-brawl.md) | Non-stop four-beat mode |
| [`references/blade-light-cinema.md`](references/blade-light-cinema.md) | 21:9 high-speed blade cinematography: 1.57 cuts/s, manga impact panels, single-hue night |
| [`references/force-field.md`](references/force-field.md) | Four channels, three field types, phrase bank |
| [`references/impact-frame-and-shake.md`](references/impact-frame-and-shake.md) | Impact-frame forms and frame counts, shake decay, hit-stop numbers |
| [`references/camera-grammar.md`](references/camera-grammar.md) | Official camera vocabulary, fight camera patterns, frame-rate traps |
| [`references/vfx-vocabulary.md`](references/vfx-vocabulary.md) | Bilingual VFX word bank, colour scripts, night-scene colour logic |
| [`references/prompt-templates.md`](references/prompt-templates.md) | Fill-in T2VA / FL2VA / Ref2VA templates |
| [`references/qa-checklist.md`](references/qa-checklist.md) | Pre- and post-generation checks, failure → fix |
| [`references/guided-mode.md`](references/guided-mode.md) | Guided mode: three entry paths, six scenario options |
| [`references/case-wuxia-duel.md`](references/case-wuxia-duel.md) | A 27.5 s duel broken down and rebuilt in four segments |
| [`scripts/validate_prompt.py`](scripts/validate_prompt.py) | Format validator |
| [`scripts/measure_motion.py`](scripts/measure_motion.py) | Motion-curve scorer |
| [`scripts/compare_clips.py`](scripts/compare_clips.py) | Side-by-side animated comparison + metric table |

## Honest limits

- Numbers come from my own runs on one rig. They are evidence, not a benchmark.
- The motion score measures picture change, not subject motion.
- The case study analyses a third-party reference clip; the clip itself is not included.
- H3 has no negative-prompt field; every "don't" is rewritten as a positive constraint.
- Reference-clip frame rates are not always what the container claims. Verify before converting.

## License

MIT
