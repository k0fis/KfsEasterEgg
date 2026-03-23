#!/usr/bin/env python3
"""Generate 8-bit style sound effects for Easter Egg game using pure Python."""

import wave
import struct
import math
import random
import os

SAMPLE_RATE = 22050
OUTPUT_DIR = "assets/sounds"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_wav(filename, samples, sample_rate=SAMPLE_RATE):
    path = os.path.join(OUTPUT_DIR, filename)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for s in samples:
            clamped = max(-32767, min(32767, int(s * 32767)))
            wf.writeframes(struct.pack("<h", clamped))
    print(f"  {path} ({len(samples)} samples, {len(samples)/sample_rate:.2f}s)")

def sine(freq, t):
    return math.sin(2 * math.pi * freq * t)

def square(freq, t):
    return 1.0 if sine(freq, t) >= 0 else -1.0

def triangle(freq, t):
    p = (t * freq) % 1.0
    return 4 * abs(p - 0.5) - 1.0

def noise():
    return random.uniform(-1, 1)

def envelope(t, attack, decay, sustain_level, sustain, release, total):
    if t < attack:
        return t / attack
    t -= attack
    if t < decay:
        return 1.0 - (1.0 - sustain_level) * (t / decay)
    t -= decay
    if t < sustain:
        return sustain_level
    t -= sustain
    if t < release:
        return sustain_level * (1.0 - t / release)
    return 0.0


def gen_hop():
    """Short bouncy hop sound - rising pitch."""
    duration = 0.15
    samples = []
    n = int(SAMPLE_RATE * duration)
    for i in range(n):
        t = i / SAMPLE_RATE
        freq = 300 + 600 * (t / duration)  # rising pitch
        vol = envelope(t, 0.01, 0.05, 0.5, 0.02, 0.07, duration)
        samples.append(vol * 0.6 * square(freq, t))
    return samples


def gen_egg():
    """Cheerful egg collect - two quick ascending notes."""
    samples = []
    notes = [(523, 0.08), (784, 0.12)]  # C5, G5
    for freq, dur in notes:
        n = int(SAMPLE_RATE * dur)
        for i in range(n):
            t = i / SAMPLE_RATE
            vol = envelope(t, 0.005, 0.02, 0.6, dur - 0.055, 0.03, dur)
            samples.append(vol * 0.5 * triangle(freq, t))
    return samples


def gen_golden():
    """Sparkly golden egg - ascending arpeggio."""
    samples = []
    notes = [(523, 0.07), (659, 0.07), (784, 0.07), (1047, 0.15)]  # C5 E5 G5 C6
    for freq, dur in notes:
        n = int(SAMPLE_RATE * dur)
        for i in range(n):
            t = i / SAMPLE_RATE
            vol = envelope(t, 0.005, 0.02, 0.6, dur - 0.055, 0.03, dur)
            s = 0.4 * triangle(freq, t) + 0.2 * sine(freq * 2, t)
            samples.append(vol * s)
    return samples


def gen_hit():
    """Getting hit by dog/tractor - harsh noise burst."""
    duration = 0.3
    samples = []
    n = int(SAMPLE_RATE * duration)
    for i in range(n):
        t = i / SAMPLE_RATE
        vol = envelope(t, 0.005, 0.1, 0.3, 0.05, 0.15, duration)
        freq = 150 - 100 * (t / duration)  # falling pitch
        s = 0.4 * square(freq, t) + 0.4 * noise()
        samples.append(vol * s)
    return samples


def gen_win():
    """Level complete fanfare - happy ascending melody."""
    samples = []
    # C E G C' E' G' C''
    notes = [(523, 0.1), (659, 0.1), (784, 0.1), (1047, 0.15),
             (1175, 0.1), (1319, 0.1), (1568, 0.3)]
    for freq, dur in notes:
        n = int(SAMPLE_RATE * dur)
        for i in range(n):
            t = i / SAMPLE_RATE
            vol = envelope(t, 0.01, 0.03, 0.7, dur - 0.08, 0.04, dur)
            s = 0.35 * triangle(freq, t) + 0.15 * sine(freq * 2, t)
            samples.append(vol * s)
    return samples


def gen_lose():
    """Game over - sad descending notes."""
    samples = []
    notes = [(392, 0.2), (349, 0.2), (311, 0.2), (262, 0.5)]  # G4 F4 Eb4 C4
    for freq, dur in notes:
        n = int(SAMPLE_RATE * dur)
        for i in range(n):
            t = i / SAMPLE_RATE
            vol = envelope(t, 0.01, 0.05, 0.5, dur - 0.1, 0.04, dur)
            samples.append(vol * 0.5 * square(freq, t))
    return samples


print("Generating sound effects...")
save_wav("hop.wav", gen_hop())
save_wav("egg.wav", gen_egg())
save_wav("golden.wav", gen_golden())
save_wav("hit.wav", gen_hit())
save_wav("win.wav", gen_win())
save_wav("lose.wav", gen_lose())
print("Done! 6 sound effects generated.")
