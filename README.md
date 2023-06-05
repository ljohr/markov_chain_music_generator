# Markov Chain Music Generator

## Demo

https://github.com/ljohr/markov_chain_music_generator/assets/46297075/735436a4-e19b-4e46-ac35-6487ed140c6d


## About This Program
This program generates classical piano pieces in the style of Beethoven, Brahms, Chopin, Liszt, or Mendelssohn. Classical piano pieces in midi file format from the Kunst Der Fuge classical music library were used. The Mido Library was used to parse midi files into text. This allowed us to treat the notes played, duration, and velocity of the note played (loudness) as simple text values that we could generate Markov Chains from.

The notes played in a given midi file are represented by one note on an 88-key keyboard, the time represents the duration a note is played, and the velocity represents how hard a note is played (loudness). 

Our clean_values() function parses the data convereted with the Mido Library, so it can be used in other functions. 
The make_markov() function creates a nested dictionary which stores a sequence of notes/times/velocities and the transition probabilities within. This is an example of one entry in our notes Markov chain shows how the sequence of notes 53, 73, and 72 have the possibility of transitioning to three different states (another sequence of notes) each with a probability of 1/3 '53 73 72': {'73 72 53': 0.3333333333333333, '73 72 53': 0.3333333333333333, '73 72 53': 0.3333333333333333}

The generate_song function begins at a random sequence of notes and creates a new classical piece using the transition probabilities stored in the markov chain dictionary.

## How to Use
1. Download this repo
2. Run the following command
```
python music_generator.py
```
3. A midi file in the style of Beethoven, Brahms, Chopin, Liszt, or Mendelssohn will be generated in the new_songs directory.
