import mido

current_path = "/Users/lilly/Documents/Final Project/"


def main():
    # name of new track
    new_track = current_path + "etude_op10_no3.mid"
    
    # first position in tracks stores all data about notes played
    current_track = mido.MidiFile(new_track).tracks[1]

    # all track info about notes pressed is in the first track
    # format = note on keyboard, 
    markov_chain = dict()
    for i in range(21, 108):
        curr_note = "note_" + str(i)
        markov_chain[curr_note] = []

    for m in current_track:
        msg = str(m)
        curr_note = ""
        # add times into the dictionary 
        if 'note_on' in msg:
            # curr_note
            if curr_note == "":
                next_note = msg[msg.rfind('note') + 5:].split(' ')[0].split('=').pop()
                curr_note = "note_" + str(next_note)
                continue
            # add count 
            markov_chain[curr_note] = "hi"
        print(markov_chain)
            
            # curr_note = "note_" + str(count)
        # print(markov_chain)
        # count += 1
        # markov_chain['note']['time'] = msg[msg.rfind('time')+5:].split(' ')[0].split('=')
        # print(markov_chain)
        # print(markov_chain)
# def parse_message(current_track):
#     # for note in ()
#     if 'note_on' in current_track:
#         on = True
#     elif 'note_off' in current_track:
#         on = False
#     else:
#         on = None
    
#     result = current_track.rfind('time')
#     print(result)

# def make_chain():


# def make_song(tempo=500000):
    # mid_new = mido.MidiFile()
    # new_song = mido.MidiTrack()
    # mid_new.tracks.append(new_song)
    # new_song.append(mido.MetaMessage('set_tempo', tempo=50000, time = 0))
    # new_song.append(mido.Message('note_on', note=35, velocity=39, time=312))
    # new_song.append(mido.Message('note_on', note=37, velocity=39, time=312))
    # mid_new.save(current_path + 'mid_new.mid')


main()


# make_song()