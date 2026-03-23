#!/usr/bin/env python3
"""Generate happy spring/Easter chiptune music for Easter Egg game.
Outputs MP3 via WAV (lame conversion) or just WAV if lame unavailable."""

import wave
import struct
import math
import os
import subprocess

SAMPLE_RATE = 22050
OUTPUT_DIR = "assets/music"
BPM = 140
BEAT = 60.0 / BPM  # seconds per beat

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Note frequencies
NOTES = {
    'C3': 131, 'D3': 147, 'E3': 165, 'F3': 175, 'G3': 196, 'A3': 220, 'B3': 247,
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 494,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 988,
    'C6': 1047, 'R': 0,  # rest
}

def sine(freq, t):
    if freq == 0: return 0
    return math.sin(2 * math.pi * freq * t)

def square(freq, t):
    if freq == 0: return 0
    return 1.0 if sine(freq, t) >= 0 else -1.0

def triangle(freq, t):
    if freq == 0: return 0
    p = (t * freq) % 1.0
    return 4 * abs(p - 0.5) - 1.0

def pulse(freq, t, duty=0.25):
    if freq == 0: return 0
    p = (t * freq) % 1.0
    return 1.0 if p < duty else -1.0

def envelope_note(t, dur):
    attack = 0.01
    release = min(0.05, dur * 0.3)
    if t < attack:
        return t / attack
    if t > dur - release:
        return max(0, (dur - t) / release)
    return 1.0

def render_track(notes_seq, wave_fn, volume=0.3):
    """Render a sequence of (note_name, beats) into samples."""
    samples = []
    time_offset = 0
    for note, beats in notes_seq:
        dur = beats * BEAT
        n = int(SAMPLE_RATE * dur)
        freq = NOTES.get(note, 0)
        for i in range(n):
            t = i / SAMPLE_RATE
            env = envelope_note(t, dur)
            samples.append(volume * env * wave_fn(freq, t))
        time_offset += dur
    return samples

def mix_tracks(*tracks):
    """Mix multiple tracks together."""
    max_len = max(len(t) for t in tracks)
    result = [0.0] * max_len
    for track in tracks:
        for i in range(len(track)):
            result[i] += track[i]
    # Normalize
    peak = max(abs(s) for s in result) if result else 1
    if peak > 0.95:
        factor = 0.9 / peak
        result = [s * factor for s in result]
    return result

def save_wav(filename, samples, sample_rate=SAMPLE_RATE):
    path = os.path.join(OUTPUT_DIR, filename)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for s in samples:
            clamped = max(-32767, min(32767, int(s * 32767)))
            wf.writeframes(struct.pack("<h", clamped))
    print(f"  {path} ({len(samples)/sample_rate:.1f}s)")
    return path

def wav_to_mp3(wav_path, mp3_path):
    """Convert WAV to MP3 using ffmpeg or lame."""
    for cmd in [
        ["ffmpeg", "-y", "-i", wav_path, "-b:a", "128k", mp3_path],
        ["lame", "--quiet", "-b", "128", wav_path, mp3_path],
    ]:
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            os.remove(wav_path)
            print(f"  -> {mp3_path}")
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    print(f"  (kept as WAV - no ffmpeg/lame found)")
    return False


def gen_track_01():
    """Happy Spring Walk - cheerful C major melody."""
    # Melody (pulse wave) - 8 bars, repeat 4x = 32 bars total ~55s
    melody_bar = [
        # Bar 1-2: C major ascending
        ('C5', 0.5), ('D5', 0.5), ('E5', 1), ('G5', 1), ('E5', 0.5), ('D5', 0.5),
        ('C5', 1), ('R', 0.5), ('E5', 0.5), ('G5', 1), ('A5', 0.5), ('G5', 0.5),
        # Bar 3-4: answer phrase
        ('F5', 1), ('E5', 0.5), ('D5', 0.5), ('C5', 1), ('D5', 1),
        ('E5', 0.5), ('G5', 0.5), ('F5', 0.5), ('E5', 0.5), ('D5', 1), ('C5', 1),
        # Bar 5-6: variation
        ('E5', 1), ('E5', 0.5), ('F5', 0.5), ('G5', 1), ('A5', 1),
        ('G5', 0.5), ('F5', 0.5), ('E5', 1), ('D5', 0.5), ('E5', 0.5), ('C5', 1),
        # Bar 7-8: ending phrase
        ('D5', 0.5), ('E5', 0.5), ('F5', 0.5), ('E5', 0.5), ('D5', 1), ('G4', 1),
        ('C5', 2), ('R', 1), ('R', 1),
    ]
    melody = melody_bar * 4

    # Bass (triangle) - simple root notes
    bass_bar = [
        ('C3', 2), ('G3', 2), ('A3', 2), ('G3', 2),
        ('F3', 2), ('C3', 2), ('G3', 2), ('C3', 2),
        ('C3', 2), ('E3', 2), ('F3', 2), ('C3', 2),
        ('D3', 2), ('G3', 2), ('C3', 2), ('C3', 2),
    ]
    bass = bass_bar * 4

    # Arpeggio (square, quiet) - fast arpeggiated chords
    arp_bar = [
        ('C4', 0.5), ('E4', 0.5), ('G4', 0.5), ('E4', 0.5),
        ('C4', 0.5), ('E4', 0.5), ('G4', 0.5), ('E4', 0.5),
        ('A3', 0.5), ('C4', 0.5), ('E4', 0.5), ('C4', 0.5),
        ('G3', 0.5), ('B3', 0.5), ('D4', 0.5), ('B3', 0.5),
        ('F3', 0.5), ('A3', 0.5), ('C4', 0.5), ('A3', 0.5),
        ('C4', 0.5), ('E4', 0.5), ('G4', 0.5), ('E4', 0.5),
        ('G3', 0.5), ('B3', 0.5), ('D4', 0.5), ('B3', 0.5),
        ('C4', 0.5), ('E4', 0.5), ('G4', 0.5), ('E4', 0.5),
    ]
    arp = arp_bar * 4

    melody_samples = render_track(melody, lambda f, t: pulse(f, t, 0.25), 0.30)
    bass_samples = render_track(bass, triangle, 0.25)
    arp_samples = render_track(arp, lambda f, t: square(f, t) * 0.5, 0.12)

    return mix_tracks(melody_samples, bass_samples, arp_samples)


def gen_track_02():
    """Easter Bunny Bounce - G major, more bouncy feel."""
    melody_bar = [
        # Phrase 1 - bouncy
        ('G5', 0.5), ('R', 0.25), ('G5', 0.25), ('A5', 0.5), ('B5', 0.5), ('D5', 1),
        ('E5', 0.5), ('G5', 0.5), ('A5', 1), ('G5', 1),
        # Phrase 2
        ('B5', 0.5), ('A5', 0.5), ('G5', 0.5), ('E5', 0.5), ('D5', 1), ('G4', 1),
        ('A4', 0.5), ('B4', 0.5), ('D5', 0.5), ('E5', 0.5), ('G5', 2),
        # Phrase 3 - higher
        ('A5', 1), ('B5', 0.5), ('A5', 0.5), ('G5', 1), ('E5', 1),
        ('D5', 0.5), ('E5', 0.5), ('G5', 1), ('A5', 1), ('R', 1),
        # Phrase 4 - resolve
        ('B5', 0.5), ('A5', 0.5), ('G5', 1), ('E5', 0.5), ('D5', 0.5),
        ('G4', 1), ('G5', 2), ('R', 1),
    ]
    melody = melody_bar * 4

    bass_bar = [
        ('G3', 2), ('D3', 2), ('E3', 2), ('G3', 2),
        ('G3', 2), ('E3', 2), ('D3', 2), ('G3', 2),
        ('A3', 2), ('G3', 2), ('E3', 2), ('D3', 2),
        ('G3', 2), ('D3', 2), ('G3', 2), ('G3', 2),
    ]
    bass = bass_bar * 4

    arp_bar = [
        ('G4', 0.5), ('B4', 0.5), ('D5', 0.5), ('B4', 0.5),
        ('G4', 0.5), ('B4', 0.5), ('D5', 0.5), ('B4', 0.5),
        ('E4', 0.5), ('G4', 0.5), ('B4', 0.5), ('G4', 0.5),
        ('D4', 0.5), ('G4', 0.5), ('B4', 0.5), ('G4', 0.5),
        ('A3', 0.5), ('D4', 0.5), ('F4', 0.5), ('D4', 0.5),
        ('G3', 0.5), ('B3', 0.5), ('D4', 0.5), ('B3', 0.5),
        ('D4', 0.5), ('G4', 0.5), ('B4', 0.5), ('G4', 0.5),
        ('G4', 0.5), ('B4', 0.5), ('D5', 0.5), ('B4', 0.5),
    ]
    arp = arp_bar * 4

    melody_samples = render_track(melody, lambda f, t: pulse(f, t, 0.25), 0.30)
    bass_samples = render_track(bass, triangle, 0.25)
    arp_samples = render_track(arp, lambda f, t: pulse(f, t, 0.125), 0.10)

    return mix_tracks(melody_samples, bass_samples, arp_samples)


def gen_track_03():
    """Sunny Farm - F major, relaxed and warm."""
    melody_bar = [
        # Phrase 1
        ('F5', 1), ('A5', 0.5), ('G5', 0.5), ('F5', 1), ('C5', 1),
        ('D5', 0.5), ('F5', 0.5), ('A5', 1), ('G5', 1), ('R', 0.5), ('F5', 0.5),
        # Phrase 2
        ('A5', 1), ('G5', 0.5), ('F5', 0.5), ('E5', 1), ('D5', 1),
        ('C5', 0.5), ('D5', 0.5), ('F5', 1.5), ('R', 0.5), ('R', 1),
        # Phrase 3
        ('C5', 0.5), ('D5', 0.5), ('F5', 1), ('G5', 1), ('A5', 1),
        ('G5', 0.5), ('F5', 0.5), ('D5', 1), ('C5', 1), ('R', 1),
        # Phrase 4
        ('D5', 0.5), ('F5', 0.5), ('A5', 1), ('G5', 0.5), ('F5', 0.5),
        ('E5', 0.5), ('D5', 0.5), ('C5', 1), ('F5', 2),
    ]
    melody = melody_bar * 4

    bass_bar = [
        ('F3', 2), ('C3', 2), ('D3', 2), ('C3', 2),
        ('F3', 2), ('A3', 2), ('F3', 2), ('C3', 2),
        ('F3', 2), ('G3', 2), ('A3', 2), ('F3', 2),
        ('D3', 2), ('C3', 2), ('F3', 2), ('F3', 2),
    ]
    bass = bass_bar * 4

    arp_bar = [
        ('F4', 0.5), ('A4', 0.5), ('C5', 0.5), ('A4', 0.5),
        ('F4', 0.5), ('A4', 0.5), ('C5', 0.5), ('A4', 0.5),
        ('D4', 0.5), ('F4', 0.5), ('A4', 0.5), ('F4', 0.5),
        ('C4', 0.5), ('E4', 0.5), ('G4', 0.5), ('E4', 0.5),
        ('F4', 0.5), ('A4', 0.5), ('C5', 0.5), ('A4', 0.5),
        ('G4', 0.5), ('B4', 0.5), ('D5', 0.5), ('B4', 0.5),
        ('D4', 0.5), ('F4', 0.5), ('A4', 0.5), ('F4', 0.5),
        ('F4', 0.5), ('A4', 0.5), ('C5', 0.5), ('A4', 0.5),
    ]
    arp = arp_bar * 4

    melody_samples = render_track(melody, lambda f, t: triangle(f, t), 0.32)
    bass_samples = render_track(bass, triangle, 0.22)
    arp_samples = render_track(arp, lambda f, t: pulse(f, t, 0.25), 0.10)

    return mix_tracks(melody_samples, bass_samples, arp_samples)


print("Generating music tracks...")

for name, gen_fn in [("track_01", gen_track_01), ("track_02", gen_track_02), ("track_03", gen_track_03)]:
    print(f"\n{name}:")
    samples = gen_fn()
    wav_path = save_wav(f"{name}.wav", samples)
    mp3_path = os.path.join(OUTPUT_DIR, f"{name}.mp3")
    wav_to_mp3(wav_path, mp3_path)

print("\nDone! 3 music tracks generated.")
