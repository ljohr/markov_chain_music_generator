import mido
import random

current_path = "/Users/lilly/Desktop/projects/markov_chain_music_generator/midi_files/"
total_notes = 0
cur_tempo = int(mido.bpm2tempo(120))

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

def make_markov(value_list, n_gram=3):
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

def generate_song(markov_chain, limit=total_notes):
    start_index = random.randint(0, len(markov_chain)-1)
    start = list(markov_chain)[start_index]
    while int(start[0:2]) < 48 or int(start[0:2]) > 67:
        start_index = random.randint(0, len(markov_chain)-1)
        start = list(markov_chain)[start_index]

    print("start is", start)
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

def make_new_midi(note_list, velocity_list, time_list, current_path):
    mid_new = mido.MidiFile()
    new_track = mido.MidiTrack()
    mid_new.tracks.append(new_track)
    new_track.append(mido.MetaMessage('set_tempo', tempo=cur_tempo))
    
    for num in range(len(note_list)):
        current_notes = note_list[num].split(' ')
        velocity_values = velocity_list[num].split(' ')
        time_values = time_list[num].split(' ')
        # print(time_values)
        count = 0
        last_time = 0
        for i in range(0, len(current_notes)):
            # print("current_notes", current_notes)
            # print("time_values  ", time_values)

            # print("current_note[i]", current_notes[i])
            # print("time_value[i]  ", time_values[i])
            cur_vel = random.randint(0, 127)
            cur_time = int(time_values[i])
            # if i % 2 == 0:
            #     cur_time += 100
            if cur_vel < 50:
                cur_vel = 0
            if abs(cur_time - last_time) < 100:
                cur_time += 100
            # if count > 15:
            #     count = 0
            #     cur_vel = 0
            #     cur_time = 480
            # if cur_time > 360:
            #     print(cur_time)
            #     cur_time = random.randint(0, 127)
            
            new_track.append(mido.Message('note_on', note=int(current_notes[i]), velocity=cur_vel, time=cur_time))
            
            last_time = cur_time
                
            
    mid_new.save(current_path + 'new_song.mid')

for i in range(1, 5):
    new_track = current_path + "symphony_1_" + str(i) + ".mid"
    # new_track = current_path + "ballade23.mid"
    # new_track = current_path + "ballade38.mid"
    # new_track = current_path + "project2.mid"
    note_list = clean_values(new_track, 'note', 5)
    time_list = clean_values(new_track, 'time', 5)
    #print("notes", note_list, "time", time_list)
    # print(time_list)
    velocity_list = clean_values(new_track, 'velocity', 9)
    markov_chain_n = make_markov(note_list)
    # print(markov_chain_n)
    markov_chain_t = make_markov(time_list)
    # print(markov_chain_t)
    #print(markov_chain_t)
    # for time in markov_chain_t:
    #     if int(time) > 120:
    #         print(time)
    markov_chain_v = make_markov(velocity_list)

note_list = generate_song(markov_chain_n, total_notes)
print(max(markov_chain_t))
print(min(markov_chain_n))
time_list = generate_song(markov_chain_t, total_notes)
# print(time_list)
velocity_list = generate_song(markov_chain_v, total_notes)
# print(new_song)
make_new_midi(note_list, velocity_list, time_list, current_path)