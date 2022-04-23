import mido
import random

current_path = "/Users/lilly/Desktop/projects/markov_chain_music_generator/"
total_notes = 0

def clean_notes(track):
    global total_notes
    # first position in tracks stores all data about notes played
    current_track = mido.MidiFile(new_track).tracks[1]
    all_notes = []
    # create an array containing all notes played in sequential order
    for m in current_track:
        total_notes += 1
        msg = str(m)
        # add times into the dictionary 
        if 'note_on' in msg:
            # curr_note
            curr_note = msg[msg.rfind('note') + 5:].split(' ')[0].split('=').pop()
            all_notes.append(curr_note)
        # print(all_notes)
    return all_notes

def make_markov(note_list, n_gram=2):
    markov_chain = {}
    for i in range(len(note_list)-n_gram-1):
        curr_state, next_state = "", ""
        for j in range(n_gram):
            curr_state += note_list[i + j] + " "
            next_state += note_list[i + j + 1] + " "
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


for i in range(1, 5):
    new_track = current_path + "symphony_1_" + str(i) + ".mid"
    note_list = clean_notes(new_track)
    markov_chain = make_markov(note_list)
# print(list(markov_chain)[0])

# arr = [1,0]
# a = random.randint(0, len(arr))
# print(a)

def generate_song(markov_chain, limit=total_notes):
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

new_song = generate_song(markov_chain, total_notes)
print(new_song)
