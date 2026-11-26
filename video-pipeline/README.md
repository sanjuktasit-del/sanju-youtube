# Free Video Pipeline - Hindi Taxi Reel

Makes the Episode 1 video for free, with no paid API and no local GPU.
All heavy compute runs on Kaggle's free GPU, started from GitHub Actions.

Credit: adapted from
[soumyabandi252/mytho-verse-video-gen](https://github.com/soumyabandi252/mytho-verse-video-gen)
(Krishna + baby video pipeline). Same idea, rebuilt for the taxi reel:
vertical 9:16, 5 story beats, Hindi narration.

## How it works

1. You press Run on the `Generate Taxi Reel` workflow in the Actions tab.
2. `video-pipeline/orchestrator.py` (GitHub Actions CPU runner) pushes
   `video-pipeline/kaggle_kernel_generate.py` to a Kaggle GPU kernel.
3. On Kaggle's free GPU (T4):
   - SDXL-Turbo draws two reference images: the woman in the beige coat
     and the man in the black puffer jacket.
   - Stable Video Diffusion animates them into 15 short clips, 3 per story
     beat (rain street, the steal, the chase, the twist, the laugh).
   - Hindi narration is generated with MMS TTS (`facebook/mms-tts-hin`).
   - ffmpeg stitches clips + narration into `output.mp4`.
4. The workflow uploads `output.mp4` as an artifact. Download it and post
   it manually.

## Setup (only you can do this part)

1. Create a free [Kaggle](https://www.kaggle.com/) account. Turn on phone
   verification, it is required for internet + GPU kernels.
2. In Kaggle, go to Account Settings, API, "Create New Token". It downloads
   a `kaggle.json` with your `username` and `key`.
3. In this repo, go to Settings, Secrets and variables, Actions, and add:
   - `KAGGLE_USERNAME`
   - `KAGGLE_KEY`
   Never commit these. They are secrets, not files.
4. Go to the Actions tab, select "Generate Taxi Reel", click "Run workflow".
5. Wait. First run can take 30 to 90+ minutes (model downloads + Kaggle
   GPU queue). Later runs are faster. Then download `output.mp4` from the
   run's Artifacts section.

## Cost

$0. Kaggle's free tier gives about 30 GPU-hours a week. One episode uses
roughly 1 to 2 hours, so about 15 to 20 episodes a week fit in the free
quota. GitHub Actions free tier covers the orchestrator (CPU only, minutes).

## Honest limits

- Character consistency is approximate. The woman and the man will look
  roughly the same across clips, not exactly the same.
- The clips are gentle motion (rain, drift, movement), not acted dialogue
  with lip-sync. The story is carried by the Hindi narration, the captions
  and the edit.
- Vertical 9:16 is adapted from the original pipeline's landscape format
  and is untested on the first run. If it fails on shape, the fallback is
  landscape + crop to 9:16 in CapCut.
- Uploading to YouTube, Instagram and Facebook is manual.
- Nothing posts without Sanju's approval. Watch the downloaded video
  first, check it against `hindi-taxi-reel/direction.md`, then post.
