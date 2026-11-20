# Patchwork Bastion: source backup

This branch holds the editable source for Patchwork Bastion. The playable game is on the `main` branch and is served at https://riftreapersgame.github.io/Patchwork-Bastion/

Backed up on 2026-11-20.

## What is here

| Folder | Contents |
| --- | --- |
| `build/` | `index.src.html` (the whole game: markup, styles and code), `make.sh`, `build.py` and the art-processing scripts |
| `art/` | The original painted art, as supplied (towers, flyers, goblins, scenery, projectiles, effects, coins, die, castle collapse, Red Canyon) |
| `sound/` | Scripts that trim, level and loop the sounds, plus the list of which pack file each sound came from (`P.json`) |
| `tests/` | Playwright scripts used to check the game, and the balance simulator (`sim.js`) |
| `tools/` | One-off scripts: the "art still needed" sheet and the patches that added cloud saves and sounds |

The finished sound files and WebP art are not duplicated here. They are in `audio/` and `assets/` on `main`.

## How the game is built

1. Edit `build/index.src.html`.
2. For a code-only change, run `sh make.sh`. It injects `manifest.json` into the page, writes `index.html`, and converts any changed PNG to WebP.
3. When art changes, run `build.py` first. It runs each art script (`paint2`, `paint3`, `flyers`, `sp`, `gob`, `terrain`, `proj`, `glaive_blade`, `fx`, `coin`, `collapse`, `canyon`) and merges their output into the manifest.

`build.py` also reads a few third-party asset folders that are not stored here: the Tiny Swords pack (via the tinywar and Clashlings repositories) and monster sprites from Stendhal. The paths inside the scripts point at the original workspace and would need updating on a new machine.

The game loads `assets/<name>.webp`. Six PNGs are still used directly by CSS: the five ribbons and the scroll.

## Things worth knowing

- **Speed:** 1× runs the update step twice per frame. The die timer and the between-wave countdown are halved so they keep their real-time pace.
- **Balance:** `TUNE` has `hpLin .3` and `hpExp 1.11`. Twin Keeps and Red Canyon each have a 1.15 health multiplier. Easy is health ×.55 with 40 castle health. Hard is 30% more health and 10% faster. The simulator's median runs were wave 30 on Greenwood normal, and 28 normal, 21 hard, 37 easy on Red Canyon.
- **Keeps:** keep 0 is the hero's. `S.k2` and `S.k3` are the extra keeps. A fallen keep redirects its goblins to the nearest standing one, and the run ends when all keeps fall.
- **Crowns and Armory:** stored on the device under `pb_crowns`, `pb_arm` and `pb_bank`. Payouts are 1 per wave, 5 per warlord, 20 per victory and 50 for a first win, multiplied by 1 on easy, 1.5 on normal and 2 on hard.
- **Cloud saves:** optional Google sign-in through Firebase (project `patchwork-bastion`, Realtime Database, saves at `saves/{uid}`). The device save stays the main save. The game checks the account before each upload and asks which progress to keep if both changed. Sign-in is hidden where Firebase can't be reached, such as the claude.ai artifact page, and on CrazyGames.
- **Sound:** the `REC` table in the source maps each event to a file, volume, pitch and minimum gap. A list of files means one is picked at random. Music volumes are in `TRACKS`. Players set music and effects volume in the pause menu.
- **Credits:** every third-party sound, music track and sprite is listed in the in-game Credits screen. Keep that list in step with any new asset. Most audio is CC0. The sea waves, "Settlement of the Frontier" and "Dark Quest" are CC BY and must stay credited.

## Still to do

- Hands-on playtest of Red Canyon, then a balance pass on Easy and Hard across all three levels
- Add a contact email to the privacy policy
- Painted phoenix rebirth (still the old pixel sprite) and a painted logo
- Publishing prep for itch.io and CrazyGames
