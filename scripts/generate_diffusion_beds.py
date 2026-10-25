#!/usr/bin/env python3
"""Generate reproducible-seed AudioLDM2 ambience beds for VoxConverse augmentation."""

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from diffusers import AudioLDM2Pipeline
from transformers import GPT2LMHeadModel

MODEL_ID = "cvssp/audioldm2"
PROMPTS = (
    "room tone in a small office, air conditioner hum, no speech, no voices",
    "quiet apartment room tone, distant city hum, no speech, no voices",
    "indoor hallway ventilation hum, no speech, no voices",
    "light rain outside a window, soft indoor ambience, no speech, no voices",
    "distant traffic ambience, low rumble, no speech, no voices",
    "cafe ambience with only non-vocal sounds (utensils, footsteps), no speech, no voices",
    "wind through trees, leaves rustling, no speech, no voices",
)
NEGATIVE_PROMPT = "speech, talking, voices, dialogue, conversation, singing, lyrics, words, narration"
COUNT = 96
SAMPLE_RATE = 16000
SECONDS = 30.0
STEPS = 30
GUIDANCE = 3.5
SEED = 12345


def as_tensor(value):
    if isinstance(value, torch.Tensor):
        return value
    for name in ("text_embeds", "pooler_output"):
        tensor = getattr(value, name, None)
        if isinstance(tensor, torch.Tensor):
            return tensor
    items = value.to_tuple() if hasattr(value, "to_tuple") else value
    if isinstance(items, (tuple, list)) and items and isinstance(items[0], torch.Tensor):
        return items[0]
    raise TypeError(f"Unexpected text encoder output: {type(value)}")


def load_pipeline(device, dtype):
    pipe = AudioLDM2Pipeline.from_pretrained(MODEL_ID, torch_dtype=dtype)
    language_model = GPT2LMHeadModel.from_pretrained(
        MODEL_ID, subfolder="language_model", torch_dtype=dtype
    )
    try:
        pipe.register_modules(language_model=language_model)
    except Exception:
        pipe.language_model = language_model
    pipe = pipe.to(device)
    text_encoder = getattr(pipe, "text_encoder", None)
    if text_encoder is not None and hasattr(text_encoder, "get_text_features"):
        original = text_encoder.get_text_features

        def patched(*args, **kwargs):
            return as_tensor(original(*args, **kwargs))

        text_encoder.get_text_features = patched
    return pipe


def valid_bed(path):
    if not path.is_file():
        return False
    try:
        info = sf.info(path)
        return (
            info.samplerate == SAMPLE_RATE
            and info.channels == 1
            and info.subtype == "PCM_16"
            and info.frames == int(SAMPLE_RATE * SECONDS)
        )
    except RuntimeError:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path("data/voxconverse/diffusion_beds_16k")
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    remaining = [
        i for i in range(COUNT)
        if args.overwrite or not valid_bed(args.output / f"bed_{i:04d}.wav")
    ]
    if not remaining:
        print(f"All {COUNT} beds are present and valid.")
        return

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    pipe = load_pipeline(device, dtype)

    for i in remaining:
        generator = torch.Generator(device=device).manual_seed(SEED + i)
        generated = pipe(
            prompt=PROMPTS[i % len(PROMPTS)],
            negative_prompt=NEGATIVE_PROMPT,
            audio_length_in_s=SECONDS,
            num_inference_steps=STEPS,
            guidance_scale=GUIDANCE,
            generator=generator,
        )
        audio = np.asarray(generated.audios[0], dtype=np.float32)
        if audio.ndim > 1:
            audio = audio[:, 0]
        audio = np.clip(audio, -1.0, 1.0)
        if len(audio) != int(SAMPLE_RATE * SECONDS):
            raise ValueError(f"Unexpected bed duration for index {i}: {len(audio)} samples")
        sf.write(args.output / f"bed_{i:04d}.wav", audio, SAMPLE_RATE, subtype="PCM_16")
        print(f"Generated {i + 1}/{COUNT}: bed_{i:04d}.wav")


if __name__ == "__main__":
    main()
