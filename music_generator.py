import mido
import random

current_path = "/Users/lilly/Desktop/projects/markov_chain_music_generator/midi_files/"
total_notes = 0
tempo = 0

# n = 5 for notes and time, n = 9 for velocity
def clean_values(track, value, n):
    global total_notes
    # first position in tracks stores all data about values played
    current_track = mido.MidiFile(new_track).tracks[1]
    all_values = []
    # create an array containing all values played in sequential order
    for m in current_track:
        if value == 'note':
            total_notes += 1
        msg = str(m)
        # add times into the dictionary 
        if 'note_on' in msg:
            # curr_note
            curr_note = msg[msg.rfind(value) + n:].split(' ')[0].split('=').pop()
            all_values.append(curr_note)
            # print(value, curr_note)
        # print(all_values)
    return all_values

def make_markov(value_list, n_gram=2):
    markov_chain = {}
    for i in range(len(value_list)-n_gram-1):
        curr_state, next_state = "", ""
        for j in range(n_gram):
            curr_state += value_list[i + j] + " "
            next_state += value_list[i + j + 1] + " "
        curr_state = curr_state[: -1]
        next_state = next_state[: -1]
        if curr_state not in markov_chain:
            markov_chain[curr_state] = {}
            markov_chain[curr_state][next_state] = 1
        else:
            if next_state in markov_chain[curr_state]:
                markov_chain[curr_state][next_state] += 1
            else:
                markov_chain[curr_state][next_state] = 1

    for curr_state, transition in markov_chain.items():
        total = sum(transition.values())
        for state, count in transition.items():
            markov_chain[curr_state][state] = count/total
    return markov_chain

def generate_song(markov_chain, limit=total_notes/4):
    start_index = random.randint(0, len(markov_chain)-1)
    start = list(markov_chain)[start_index]
    n = 0 
    curr_state = start
    next_state = None
    new_song = []

    while n < limit:
        next_state = random.choices(list(markov_chain[curr_state].keys()), list(markov_chain[curr_state].values()))
        curr_state = next_state[0]
        new_song.append(curr_state)
        n += 1
    return new_song

def make_new_midi(note_list, velocity_list, time_list, current_path, tempo):
    mid_new = mido.MidiFile()
    new_track = mido.MidiTrack()
    mid_new.tracks.append(new_track)
    new_track.append(mido.MetaMessage('set_tempo', tempo=500000))
    
    for num in range(len(note_list)):
        current_notes = note_list[num].split(' ')
        velocity_values = velocity_list[num].split(' ')
        time_values = time_list[num].split(' ')
        for i in range(0, len(current_notes)):
            new_track.append(mido.Message('note_on', note=int(current_notes[i]), velocity=random.randint(0, 127), time = int(time_values[i])))
            
    mid_new.save(current_path + 'new_song.mid')

for i in range(1, 5):
    new_track = current_path + "symphony_1_" + str(i) + ".mid"
    note_list = clean_values(new_track, 'note', 5)
    time_list = clean_values(new_track, 'time', 5)
    velocity_list = clean_values(new_track, 'velocity', 9)
    markov_chain_n = make_markov(note_list)
    markov_chain_t = make_markov(time_list)
    markov_chain_v = make_markov(velocity_list)

note_list = generate_song(markov_chain_n, total_notes)
time_list = generate_song(markov_chain_t, total_notes)
velocity_list = generate_song(markov_chain_v, total_notes)
# print(new_song)
make_new_midi(note_list, velocity_list, time_list, current_path, 2500)