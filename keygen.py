#!/usr/bin/env python3
import sys
import random
import mido
import midi_abstraction

def get_music(source, mixin, rhythm):

	opt = [i for i in source.list_chords() if 'dim' not in i]
	length = len(rhythm) - 2

	progression = []
	while len(progression) < length:
		progression.append(opt[random.randint(1, len(opt) - 1)])

	# get a borrowed chord
	last_chords = []
	for i in mixin.list_chords():
		if 'dim' not in i and i not in progression:
			last_chords.append(i)

	last_chord = random.choice(last_chords)
	progression.append(last_chord)
	progression = [opt[0]] + progression

	# produce a motif, 4 notes long, repeated twice each measure
	scale = source.list_notes()
	altscale = mixin.list_notes()
	uncommon_index = []
	common_index = []

	if source.name != mixin.name:
		for a, b in zip(scale, altscale):
			if a != b:
				uncommon_index.append(scale.index(a))
			else:
				common_index.append(scale.index(a))
	else:
		for a, b in zip(scale, altscale):
			if a == b:
				uncommon_index.append(scale.index(a))
				common_index.append(scale.index(a))

	motif = []
	for i in random.choices(common_index, k = 4):
		motif.append(i)

	# fit tonal center into motif at either beginning or end, if it's not already in there
	if 0 not in motif:
		spot = random.choice([-1, 0])
		motif[spot] = 0

	# pick random non start non end to put outlier
	spot = random.choice(range(1, len(motif) - 1))
	outlier = random.choice(uncommon_index)
	motif[spot] = outlier
	motif *= 2

	chord_result = []
	for i in range(len(rhythm)):
		# we need to doctor the notes of the motif if it won't fit with the chord.
		chord_notes = []
		chord_result.append([])
		for e in range(len(midi_abstraction.chords(progression[i]))):
			octave = random.choice([3, 4, 4, 4, 4])
			chord_result[i].append({})
			chord_result[i][e]['name'] = progression[i]
			chord_result[i][e]['rhythm'] = rhythm[i]
			chord_result[i][e]['vel'] = random.randint(50, 70)
			chord_result[i][e]['pitch'] = midi_abstraction.chords(progression[i])[e][octave]
			chord_notes.append(midi_abstraction.notes(midi_abstraction.chords(progression[i])[e][octave]))

	melody = []
	for i in progression:
		if i in source.list_chords():
			motif_test = [scale[x] for x in motif]
		else:
			motif_test = [altscale[x] for x in motif]
		for x in motif_test:
			melody.append(x)

	melody_result = []
	for i in range(len(melody)):
		melody_result.append([])
		melody_result[i].append({})
		melody_result[i][0]['name'] = melody[i]
		melody_result[i][0]['rhythm'] = 128
		octave = random.choice([5, 5, 6])
		melody_result[i][0]['pitch'] = midi_abstraction.notes(melody[i])[octave]
		melody_result[i][0]['vel'] = random.randint(50, 70)
	return chord_result, melody_result

def get_track(data, kind, measure):
	tracks = []
	beat = 0
	for part in data:
		for sound in part:
			t = mido.MidiTrack()
			n = sound['pitch']
			v = sound['vel']
			t.append(mido.Message('note_on', note = n, velocity = v, time = beat + measure))
			t.append(mido.Message('note_off', note = n, velocity = v, time = sound['rhythm']))
			tracks.append(t)
			if kind == 'melody':
				beat += sound['rhythm']

		if kind == 'chord':
			beat += part[0]['rhythm']

	result = mido.merge_tracks(tracks)
	return result

if __name__ == '__main__':
	# get a modal key
	if len(sys.argv) > 1:
		if len(sys.argv) > 3:
			print('Modal Mixture Usage: python3 keygen.py "d_dorian" "ionian"')
			print('Single Mode Usage: python3 keygen.py "a_mixolydian"')
			print('Random Mode Usage: python3 keygen.py')
			exit()
		n = sys.argv[1].split('_')[0]
		m = sys.argv[1].split('_')[1]
		if len(sys.argv) == 3:
			altmode = sys.argv[-1]
		else:
			altmode = m
	else:
		n = random.choice([i for i in midi_abstraction.universe() if len(i) < 2])
		all_modes = midi_abstraction.list_modes()
		all_modes.pop(all_modes.index('locrian'))
		m = random.choice(all_modes)
		altmode = False

	k = n + '_' + m
	print(f'key: {k}')

	# set file resolution
	mid = mido.MidiFile(type = 1, ticks_per_beat = 256)

	# get our song key object: source
	source = midi_abstraction.Key(k)

	own_note = source.name.split('_')[0]

	if not altmode:
		altmode = {}
		all_modes = midi_abstraction.list_modes()
		random.shuffle(all_modes)

		for i in all_modes:
			score = 0
			if i != source.mode and i != 'locrian':
				new_dict = {}
				test_key = midi_abstraction.Key(own_note + '_' + i)
				sames = len([i for i in test_key.list_notes() if i in source.list_notes()])
				new_dict[test_key.name] = sames
				if not altmode:
					altmode = new_dict
				elif sames >= max(list(altmode.values())) - 2:
					altmode = new_dict
				else:
					continue

		mixin = midi_abstraction.Key(list(altmode.keys())[0])

	else:
		mixin = midi_abstraction.Key(own_note + '_' + altmode)

	print(f'secondary mode: {mixin.name}')


	# set up rhythms
	chord_rhythms = [[1024] * 4]
	# chord_rhythms.append([1024, 1024, 2048])
	melody_rhythms = [[256] * 16]

	chords_a, melody_a = get_music(source, mixin, random.choice(chord_rhythms))
	chords_b, melody_b = get_music(source, mixin, random.choice(chord_rhythms))
	chords_c, melody_c = get_music(source, mixin, random.choice(chord_rhythms))
	chords_d, melody_d = get_music(source, mixin, random.choice(chord_rhythms))
	chords_e, melody_e = get_music(source, mixin, random.choice(chord_rhythms))
	chords_f, melody_f = get_music(source, mixin, random.choice(chord_rhythms))
	chords_g, melody_g = get_music(source, mixin, random.choice(chord_rhythms))
	chords_h, melody_h = get_music(source, mixin, random.choice(chord_rhythms))
	chords_i, melody_i = get_music(source, mixin, random.choice(chord_rhythms))

	melody_z = melody_a[0:int(len(melody_a) / 2)] * 2
	chords_z = [[{'name': 'a', 'vel': 0, 'rhythm': 4096, 'pitch': 0}]]

	# set up form
	c_patterns = [
		[chords_z] + [chords_a, chords_b, chords_a, chords_c, chords_d, chords_e, chords_e, chords_f] * 2 + [chords_z] +
		[chords_h, chords_g, chords_h, chords_i, chords_i, chords_i]
	]

	m_patterns = [
		[melody_b] + [melody_a, melody_b, melody_a, melody_c, melody_d, melody_e, melody_e, melody_f] * 2 + [melody_z] +
		[melody_h, melody_g, melody_a, melody_i, melody_i, melody_i]
	]

	form = random.randint(0, len(c_patterns) - 1)
	blueprint = [
		{'pattern': c_patterns[form], 'kind': 'chord'},
		{'pattern': m_patterns[form], 'kind': 'melody'}
	]

	# compile the tracks
	parts = []
	for part in blueprint:
		measure = 0
		tracks = []
		for pattern in part['pattern']:
			track = get_track(pattern, part['kind'], measure)
			tracks.append(track)
			measure += 4096
		mix = mido.merge_tracks(tracks)
		parts.append(mix)

	for part in parts:
		mid.tracks.append(part)

	# write the file

	if mixin.name != source.name:
		filename = k + '_' + mixin.name.split('_')[-1] + '.mid'
	else:
		filename = k + '.mid'

	mid.save(filename)
	print(f'saved as: {filename}')


