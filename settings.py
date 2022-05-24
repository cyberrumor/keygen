#!/usr/bin/env python3

# rhythms controls the layout of measures.
# 1024 is a whole note, 512 is a half note, etc.
# For example, [1024, 1024, 2048] would produce
# a chord progression with three unique chords arranged
# in note duration as quarter, quarter, half.
# Each entry must have a sum of 4096, which is one measure.
# We don't consider diminished chords in keygen, which gives
# us a theoretical maximum of 6 chords per progression.
# Keygen artificially limits this to 4, so don't exceed 4.
rhythms = [[1024] * 4]
rhythms.append([1024, 1024, 2048])

# chord_velocity_min controls the lowest possible keypress pressure for any note in a chord.
# this must be less than chord_velocity_max. Lowest acceptible is 0.
chord_velocity_min = 50

# chord_velocity_max controls the greatest possibel keypress pressure for any note in chord.
# this must be greater than chord_velocity_min. Max acceptible is 127.
chord_velocity_max = 70

# octs controls the possible octave selection for each note in a chord.
# This expects 3 values per entry, and each entry will have every value used in sequence.
# Each entry has an equal chance of being selected on a per-chord basis.
# valid values are 0 through 8. C4 in this context is in octave 5.
octs = [
		[2, 3, 4],
		[3, 3, 3],
		[4, 4, 4],
	]

# possible_whole_notes dictates the order of note durations in the melody.
# each entry must have a sum of 1024.
possible_whole_notes = [
		# [128] * 8, # eight eigths
		[256] * 4, # four quarter notes
		[512] * 2, # two half notes
		# [1024], # one whole note,
		[512, 256, 256], # half, quarter, quarter
		# [256, 256, 512], # quarter, quarter, half

		# unique patterns
		[128, 128, 128, 128, 512],
		[256, 256, 128, 128, 128, 128],
		# [128, 128, 256, 512],
		[512, 128, 128, 256],
		[512, 256, 128, 128],
	]

# flip determines whether it is possible to use reversed order for possible_whole_notes.
# if set to True, there is a 50/50 chance of reversal. This operation occurs before rev
# and before walk.
flip = True

# walk determines whether the notes in the motif have a 50/50 chance to be sorted by pitch.
# ascending. This operation occurs after flip, before rev.
walk = True

# rev determines wehther the entire motif has a 50/50 chance to be reversed.
# if this and walk are both true, there is a possibility for descending scales rather
# than just ascending. This operation occurs after flip and walk.
rev = True

# melody_velocity_min is the lowest possible keypress pressure for any note in a melody.
# accepts 0 through 127. Must be less than melody_velocity_max.
melody_velocity_min = 50

# melody_velocity_max is the greatest possibel keypress pressure for any note in a melody.
# accepts 0 through 127. Must be greater than melody_velocity_min.
melody_velocity_max = 70

# melody_octaves controls the possible octave assigned to each note in a melody,
# on a per-note basis. Equal chance, so you can use duplicates here to increase the
# chance that a particular octave is selected. 0 through 8.
melody_octaves = [4, 5, 5, 5, 6, 6, 6, 6]

# to define the number of unique measures, their order, repition, etc,
# please see # SET UP RHYTHMS and # SET UP FORM in keygen.py.



if __name__ == '__main__':
	print("This file is imported by keygen.py, and does nothing when ran directly.")
	print("Please open this in a text editor to modify parameters.")
	input("Press [Enter] to close.")
	exit()
