# Asha Kaun Hai? — Episode 1, Seedance lip-sync prompts

## How lip sync works here

Voices first, then video. Seedance generates each shot from a reference still plus that beat's voice audio, so the lips follow the dialogue. That is what makes it lip sync instead of narration over silent motion. The free routes (Dreamina motion, the Kaggle pipeline) do not do audio-driven lip sync. Seedance is paid, via Higgsfield.

## Order of work

1. Generate all 10 voice lines in ElevenLabs from `voice-script.md`. Save as `ai-drama-ep1/audio/` with the file names there.
2. For each beat below, open Seedance, upload the reference still, upload that beat's audio file or files, paste the prompt, generate 5 to 10 seconds.
3. Assemble in CapCut in beat order, hard cuts. Add the low drone under beats 1 to 4, one sting at "Main Asha hoon", silence on the cut to black. Add the on-screen text from `script.md`.

## Reference stills

The 5 preview stills are the image input for Seedance. They live in `workspace/your_files/sanju-youtube/ai-drama-ep1/frames/` and were shown in chat. (They are images, so they are not in the repo itself.)

- Beat 1: `media-generation-beat-1-gate-0-998395c2-97b1-4e0a-82c5-81a644f7b725.webp`
- Beat 2: `media-generation-beat-2-will-0-f9e8d7de-71bc-4cd1-adf2-f4dbee78d338.webp`
- Beat 3: `media-generation-beat-3-photo-0-0d798176-5e3d-42f3-80a7-2c7a8f466231.webp`
- Beat 4: `media-generation-beat-4-confrontation-0-49efdb07-595c-4b7b-a90f-d04a6cc504e3.webp`
- Beat 5: `media-generation-beat-5-doorbell-0-8dab36aa-4700-44c7-b534-3669a2fe783b.webp`

## Beat 1 — the gate (0-8s)

- Audio: `meera-b1-vo.wav`
- Prompt: "Animate this still into a 5 to 8 second cinematic shot: the woman stands in heavy rain at the iron gate, rain falling, her hair and clothes moving slightly in the rain, camera holds steady. Her lips move to the attached voiceover. Night, cold blue light, photorealistic, vertical 9:16."

## Beat 2 — the will reading (8-20s)

- Audio: `lawyer-b2.wav`, `meera-b2.wav`, `rekha-b2.wav`
- Prompt: "Animate this still: the lawyer reads from the papers, his lips moving to the attached audio, the two women react in silence. Camera holds steady on the table. Warm lamp light, photorealistic, vertical 9:16."
- If the lips go wrong: split this beat into two shots. Shot A, lawyer close-up with `lawyer-b2.wav` only. Shot B, Meera and Rekha with `meera-b2.wav` and `rekha-b2.wav`. One speaker visible at a time is where lip sync holds.

## Beat 3 — the photo (20-32s)

- Audio: `meera-b3-vo.wav`
- Prompt: "Animate this still: the woman stares at the old photograph, her expression shifting to shock, slight head movement, rain on the window behind. Her lips move to the attached voiceover. Warm desk lamp, photorealistic, vertical 9:16."

## Beat 4 — the confrontation (32-45s)

- Audio: `meera-b4.wav`, `rekha-b4a.wav`, `meera-b4b.wav`, `rekha-b4b.wav`
- Prompt: "Animate this still: the two women face each other in the hallway, speaking in turn, lips matching the attached audio, tense and still. Warm lamp light, photorealistic, vertical 9:16."
- If the lips go wrong: split into alternating close-ups. Meera's lines on her close-up, Rekha's on hers, cut between them.

## Beat 5 — the doorbell (45-60s)

- Audio: `asha-b5.wav`
- Prompt: "Animate this still: the woman in the white kurta stands in the rain in the doorway, rain falling around her, she speaks one line, lips matching the attached audio, then holds still. Cold blue light, photorealistic, vertical 9:16."

## Honest limits

- Seedance is paid. There is no free audio-driven lip sync in this stack.
- Keep each shot 5 to 10 seconds and one speaker visible at a time. Multi-speaker wide shots are where lip sync breaks.
- Faces may still drift between beats. If a beat's face is wrong, regenerate that beat only, same reference still, same audio.
- Nothing posts without Sanju's approval. She sees the cut before it goes up.
