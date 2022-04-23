from calendar import c
import mido

current_path = "/Users/lilly/Desktop/projects/markov_chain_music_generator/"
new_track = current_path + "etude_op10_no3.mid"


def clean_notes(track):
    # first position in tracks stores all data about notes played
    current_track = mido.MidiFile(new_track).tracks[1]
    all_notes = []

    # create an array containing all notes played in sequential order
    for m in current_track:
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
    print(markov_chain)


note_list = clean_notes(new_track)
make_markov(note_list)