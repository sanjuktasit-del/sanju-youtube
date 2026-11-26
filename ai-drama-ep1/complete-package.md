# Asha Kaun Hai? — Episode 1, complete package

Everything for Episode 1 in one place. Nothing here posts without Sanju's approval. She sees the cut before it goes up.

## What is in this folder

- `script.md` — the 60-second story, 5 beats, Hinglish.
- `direction.md` — look, sound, camera, the rules (original story, no child characters, no violence on screen, no kidnapping).
- `dreamina-prompts.md` — the 5 scene prompts for Dreamina image-to-video.
- `voice-script.md` — all 10 dialogue lines, 4 voices, ElevenLabs file names.
- `seedance-prompts.md` — per-beat Seedance prompts for true lip sync.
- `posting.md` — title, description, hashtags, pinned comment for The Swinging Star.
- `complete-package.md` — this file, the runbook.

## Rendered locally (not in the repo — binary files cannot be pushed here)

In `workspace/your_files/sanju-youtube/ai-drama-ep1/`:

- `frames/` — the 5 preview stills (beats 1, 2, 3, 4, 5).
- `animatic-ep1-60s.mp4` — silent 60-second animatic, stills cut to beat timing.
- `audio/line01` to `line10` — the 10 dialogue lines as MP3, 4 voices, Hindi.
- `episode1-with-dialogue.mp4` — the with-dialogue cut: stills with a slow zoom, dialogue mixed in at the beat times. Honest label: the voices speak, the pictures move gently, but the lips do not move. A timing and voice preview, not the final episode.

## How the final movie-like video gets made

There are two paths. Only one gives real lip sync.

### Path A — free, GitHub + Kaggle pipeline

The repo holds `video-pipeline/` (Kaggle free GPU + Stable Video Diffusion + MMS TTS, adapted from open-source mytho-verse-video-gen). What it makes: moving scenes from stills plus Hindi narration. It does NOT do lip-synced dialogue.

Current state, checked 2026-11-26: the workflow file is NOT live. `.github/workflows/generate-taxi-reel.yml` does not exist in the repo. Two steps are still open, both need Sanju:

1. Add the workflow file via the GitHub web UI (copy `video-pipeline/generate-taxi-reel.yml` to `.github/workflows/`). The Muse GitHub App cannot write there.
2. Create a free Kaggle account and token, add `KAGGLE_USERNAME` and `KAGGLE_KEY` as repo secrets.

### Path B — paid, ElevenLabs + Seedance (the lip-sync path)

1. Generate the 10 voice lines in ElevenLabs from `voice-script.md`.
2. Generate each beat in Seedance from `seedance-prompts.md`: reference still plus that beat's audio, so the lips follow the dialogue.
3. Assemble in CapCut in beat order, hard cuts. Low drone under beats 1 to 4, one sting at "Main Asha hoon", silence on the cut to black. On-screen text from `script.md`.

Seedance is paid, via Higgsfield. There is no free audio-driven lip sync in this stack, and no Seedance connector here.

## Limits, stated plainly

- Video generation is blocked for this account in its region, so no moving scenes can be generated from here.
- Faces may drift between beats in any AI render. If a beat's face is wrong, regenerate that beat only, same reference still, same audio.
- Keep each shot 5 to 10 seconds and one speaker visible at a time. Multi-speaker wide shots are where lip sync breaks.
