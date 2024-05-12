#!/usr/bin/env python3
import mido
import midi_abstraction as mab
import random


def generate(scale: list[set[mab.Note]], ticks: int) -> mido.MidiTrack:
    track = mido.MidiTrack()
    octave = 4
    velocity = 127 // 2

    notes = random.sample(
        scale,
        4,
        counts=[2, 1, 1, 1, 1, 1, 1],
    )
    notes *= 2
    notes += random.sample(
        scale,
        4,
        counts=[2, 1, 1, 1, 1, 1, 1],
    )
    notes += random.sample(scale, 4)

    for s in notes:
        n = next(iter(s))
        note = mab.NOTES[n][octave]

        track.append(
            mido.Message(
                'note_on',
                note = note,
                velocity = velocity,
                time = 0
            )
        )

        track.append(
            mido.Message(
                'note_off',
                note = note,
                velocity = velocity,
                time = 256 // 4
            )
        )

    return track
