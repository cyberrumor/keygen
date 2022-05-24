#!/usr/bin/env python3
import sys
import random
import mido
import midi_abstraction
import settings

# accepts midi_abstraction.Key, midi_abstraction.Key,
# list of integers that summmarize to 4096.
# outputs two lists of dicts, where each dict represents a measure of data.
# the first output list is for chords, the other for melody.
def get_music(source, mixin, rhythm):
	# beginning determines whether the tonal cennter will be the first or last note of the
	# motif. This isn't used until later but is defined outside of the loop for increased
	# consistency on location of tonal center. Matters most if rev and walk are false.
	beginning = random.choice([True, False])

	# get a list of chord options, exclude diminished.
	opt = [i for i in source.list_chords() if 'dim' not in i]
	length = len(rhythm) - 2

	progression = []
	while len(progression) < length:
		progression.append(opt[random.randint(1, len(opt) - 1)])

	# get a borrowed chord
	last_chords = []
	for i in mixin.list_chords():
		# don't consider diminished chords, as they're difficult to automatically accommodate.
		if 'dim' not in i and i not in progression:
			last_chords.append(i)

	last_chord = random.choice(last_chords)
	progression.append(last_chord)
	progression = [opt[0]] + progression

	chord_result = []
	melody_result = []
	for i in range(len(rhythm)):
		# we need to doctor the notes of the motif if it won't fit with the chord.
		chord_notes = []
		chord_result.append([])
		octs = random.choice(settings.octs)

		for e in range(len(midi_abstraction.chords(progression[i]))):
			octave = octs[e]
			chord_result[i].append({})
			chord_result[i][e]['name'] = progression[i]
			chord_result[i][e]['rhythm'] = rhythm[i]
			chord_result[i][e]['vel'] = random.randint(settings.chord_velocity_min, settings.chord_velocity_max)
			chord_result[i][e]['pitch'] = midi_abstraction.chords(progression[i])[e][octave]
			chord_notes.append(midi_abstraction.notes(midi_abstraction.chords(progression[i])[e][octave]))

		# whole note melody rhythms
		possible_whole_notes = settings.possible_whole_notes

		# collect appropriate number of melody rhythms
		melody_rhythm = []
		c = random.choice(possible_whole_notes)
		flip = settings.flip
		if flip and random.choice([True, False]):
			c.reverse()
		melody_rhythm += c

		num_whole_notes = int(chord_result[i][e]['rhythm'] / 1024)
		melody_rhythm *= num_whole_notes

		# produce a motif, len(melody_rhythm) notes long
		scale = source.list_notes()
		altscale = mixin.list_notes()
		uncommon_index = []
		common_index = []

		# index the 
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

		# increase the length of motify possibilities so we can make a melody without so much repitition
		common_index *= 2
		common_index += uncommon_index * 2
		motif = random.sample(common_index, len(melody_rhythm))

		# Guarantee the tonal center is either the first or last note of the motif.
		if 0 not in [motif[0], motif[-1]]:
			walk = settings.walk
			rev = settings.rev

			# rev and walk may make "beginning" seem redundant, but note that "beginning"
			# is defined outside of the loop, which will cause the song to have a more
			# consistent location for the tonal center, especially if rev and walk are false.
			if beginning:
				motif[0] = 0
			else:
				motif[-1] = 0

			if walk and random.choice([True, False]):
				sorted(motif)
			if rev and random.choice([True, False]):
				motif.reverse()


		# Guarantee the motif selects notes available from the current chord. This only matters for modal mixture.
		melody = []
		if chord_result[i][e]['name'] in source.list_chords():
			motif_test = [scale[x] for x in motif]
		else:
			motif_test = [altscale[x] for x in motif]
		for h in motif_test:
			melody.append(h)

		melody_result.append([])
		for w in range(len(melody_rhythm)):
			melody_result[i].append({})
			melody_result[i][w]['name'] = melody[w]
			melody_result[i][w]['rhythm'] = melody_rhythm[w]
			octave = random.choice(settings.melody_octaves)
			melody_result[i][w]['pitch'] = midi_abstraction.notes(melody[w])[octave]
			melody_result[i][w]['vel'] = random.randint(settings.melody_velocity_min, settings.melody_velocity_max)

	return chord_result, melody_result

# accepts output from get_music, string of either "chord" or "melody",
# and integer divisible by 4096 (this determines the global position of the measure).
# outputs mido.MidiTrack.
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

	# set file resolution. If you multiply this to increase quality, make sure to increase all other time values by the same factor.
	mid = mido.MidiFile(type = 1, ticks_per_beat = 256)

	# get our song key object: source
	source = midi_abstraction.Key(k)

	own_note = source.name.split('_')[0]
	# if no key was specified, use modal mixture, but not with locrian. Locrian has no tonal center.
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


	# SET UP RHYTHMS
	rhythms = settings.rhythms

	chords_a, melody_a = get_music(source, mixin, random.choice(rhythms))
	chords_b, melody_b = get_music(source, mixin, random.choice(rhythms))
	chords_c, melody_c = get_music(source, mixin, random.choice(rhythms))
	chords_d, melody_d = get_music(source, mixin, random.choice(rhythms))
	chords_e, melody_e = get_music(source, mixin, random.choice(rhythms))
	chords_f, melody_f = get_music(source, mixin, random.choice(rhythms))
	chords_g, melody_g = get_music(source, mixin, random.choice(rhythms))
	chords_h, melody_h = get_music(source, mixin, random.choice(rhythms))
	chords_i, melody_i = get_music(source, mixin, random.choice(rhythms))

	# SET UP FORM
	c_patterns = [
		[chords_a, chords_a, chords_b, chords_b] * 2 +
		[chords_c, chords_d, chords_c, chords_d] +
		[chords_e, chords_e, chords_e, chords_e] +
		[chords_a, chords_a, chords_b, chords_b] * 2 +
		[chords_c, chords_d, chords_c, chords_d] +
		[chords_f, chords_g, chords_h, chords_h] * 2 +
		[chords_a, chords_i, chords_a, chords_b]
	]

	m_patterns = [
		[melody_a, melody_a, melody_b, melody_b] * 2 +
		[melody_c, melody_d, melody_c, melody_d] +
		[melody_e, melody_e, melody_e, melody_e] +
		[melody_a, melody_a, melody_b, melody_b] * 2 +
		[melody_c, melody_d, melody_c, melody_d] +
		[melody_f, melody_g, melody_h, melody_h] * 2 +
		[melody_a, melody_i, melody_a, melody_b]
	]

	# "form" ensures that you are using the same pattern structure for chords and melodies,
	# in case multiple are defined. Only one is defined by default.
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
		# parts.append(mix)
		mid.tracks = [mix]

		# write the file

		if mixin.name != source.name:
			filename = k + '_' + mixin.name.split('_')[-1] + '_' + part['kind'] + '.mid'
		else:
			filename = k + '_' + part['kind'] + '.mid'

		mid.save(filename)
		print(f'saved as: {filename}')

	input("Press [Enter] to close.")


