import mido
import random
import os

# get the current working directory so up to /markov_chain_music_generator/
current_path = os.path.abspath(os.path.dirname(__file__)) + "/"

midi_path = "midi_files/"
new_song_path = "new_songs/"

# check if midi_files folder exists
if not os.path.exists(current_path + midi_path):
    print("midi_files folder is missing")
    exit(1)

# check new_song_path exists and make folder if not
if not os.path.exists(current_path + new_song_path):
    os.makedirs(current_path + new_song_path)


cur_tempo = int(mido.bpm2tempo(130))    # set bpm
new_file_notes = 1500                   # set number of notes in new file
n_gram = 4                              # set number of notes/durations/velocities to consider for markov chains

note_len = 5
vel_len = 9

# n = 5 for notes and time, n = 9 for velocity
def clean_values(new_track, value, n):
    # not all midi files store the note information in the same place 
    # so loop through and find the correct array
    curr_track = mido.MidiFile(new_track).tracks
    for i in range(0, len(curr_track)-1):
        if "note_on" in str(curr_track[i]):
            current_track = curr_track[i]
    all_values = []
    # create an array containing all values played in sequential order
    for m in current_track:
        msg = str(m)
        # add times into the dictionary 
        if "note_on" in msg:
            # curr_note
            curr_note = msg[msg.rfind(value) + n:].split(" ")[0].split("=").pop()
            all_values.append(curr_note)
    return all_values

def make_markov(value_list, n_gram):
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

def generate_song(markov_chain, new_file_notes, type):
    start_index = random.randint(0, len(markov_chain)-1)
    start = list(markov_chain)[start_index]
    min = 0
    max = 0
    # if reading array of notes, choose from C3 to G4
    if type == "notes":
        min = 40
        max = 67
    # if velocity too loud or quiet, set new velocity
    elif type == "velocity":
        min = 60
        max = 90
    # if time too long or short, set new time
    elif type == "time":
        min = 50
        max = 300

    while int(start[0:2]) < min or int(start[0:2]) > max:
        start_index = random.randint(0, len(markov_chain)-1)
        start = list(markov_chain)[start_index]
    n = 0 
    curr_state = start
    next_state = None
    new_song = []

    while n < new_file_notes:
        # if a string of notes never leads to another (last notes in a file)
        try: 
            markov_chain[curr_state].keys()
        # genenerate a new starting point
        except KeyError:
            curr_state = list(markov_chain)[random.randint(0, len(markov_chain)-1)]

        next_state = random.choices(list(markov_chain[curr_state].keys()), list(markov_chain[curr_state].values()))
        curr_state = next_state[0]
        new_song.append(curr_state)
        n += 1
    return new_song

def make_new_midi(note_list, velocity_list, time_list, current_path, composer):
    mid_new = mido.MidiFile()
    new_track = mido.MidiTrack()
    mid_new.tracks.append(new_track)
    new_track.append(mido.MetaMessage("set_tempo", tempo=cur_tempo))
    
    for num in range(len(note_list)):
        current_notes = note_list[num].split(" ")
        velocity_values = velocity_list[num].split(" ")
        time_values = time_list[num].split(" ")
        last_time = 0
        
        for i in range(0, len(current_notes)):
            cur_time = int(time_values[i])
            # if time between notes is too tight, increase gap
            if abs(cur_time - last_time) < 100:
                cur_time += 100
            
            new_track.append(mido.Message("note_on", note=int(current_notes[i]), velocity=int(velocity_values[i]), time=cur_time))
            last_time = cur_time
                
    mid_new.save(current_path + new_song_path + "new_song_" + composer + ".mid" )

# find all midi files in a given folder
def get_midi_files(composer):
    midi_files = []
    for r, d, f in os.walk(current_path + midi_path + composer):
        for file in f:
            if file.endswith(".mid"):
                midi_files.append(file)
    return midi_files

def run_program(composer):
    composer_path = composer + "/"
    midi_files = get_midi_files(composer_path)

    for file in midi_files:
        new_track = current_path + midi_path + composer_path + file
        note_list = clean_values(new_track, "note", note_len)
        time_list = clean_values(new_track, "time", note_len)
        velocity_list = clean_values(new_track, "velocity", vel_len)
        markov_chain_n = make_markov(note_list, n_gram)
        markov_chain_t = make_markov(time_list, n_gram)
        markov_chain_v = make_markov(velocity_list, n_gram)

    note_list = generate_song(markov_chain_n, new_file_notes, "notes")
    time_list = generate_song(markov_chain_t, new_file_notes, "time")
    velocity_list = generate_song(markov_chain_v, new_file_notes, "velocity")
    make_new_midi(note_list, velocity_list, time_list, current_path, composer)

#main section
print("♫ Welcome to the Markov Chain Music Generator ♫")
print("Listen to a new song in the style of (1) Beethoven, (2) Brahms, (3) Chopin, (4) Liszt, or (5) Mendelssohn")
print("Enter a number between 1 to 5 to generate a song in the style of your favorite composer: ")

while True:
    try:
        user_input = input()
        if user_input == "q":
            print("Exiting program")
            break
        user_input = int(user_input)
        composer = ""
        if user_input == 1:
            composer = "beethoven"
        elif user_input == 2:
            composer = "brahms"
        elif user_input == 3:
            composer = "chopin"
        elif user_input == 4:
            composer = "liszt"
        elif user_input == 5:
            composer = "mendelssohn"
        print("♫ Generating Song ♫")
        run_program(composer)
    except ValueError:
        print("Wrong input")
        print("Enter a number between 1 to 5 to generate a song in the style of your favorite composer")
        print("(1) Beethoven, (2) Brahms, (3) Chopin, (4) Liszt, or (5) Mendelssohn")
        print("Or enter q to quit")
        continue
    else:
        print("♫ New song generated! ♫")
        print("Find song in " + current_path + new_song_path)
        break