#!/usr/bin/env python3
import midi_abstraction
import sys

def get_keys_with_notes(notes):
    results = []
    for mode in midi_abstraction.list_modes():
        for note in [i for i in midi_abstraction.list_notes() if len(i) == 1]:
            key = midi_abstraction.Key(f"{note}_{mode}")
            if set(notes).issubset(set(key.list_notes())):
                results.append({key.name: key.list_notes()})
    return results


if __name__ == '__main__':
    args = sys.argv[1:]
    notes = [i.lower() for i in args]

    for key in get_keys_with_notes(notes):
        print(key)
