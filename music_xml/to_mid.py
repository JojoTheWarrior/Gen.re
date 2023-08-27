from music21 import stream, note, chord, volume



# # Create a "silent" note (no pitch, zero volume)
# silent_note = note.Note()
# silent_note.volume = volume.Volume(velocity=0)  # Set volume to zero
# silent_note.quarterLength=1/4

# rest = note.Rest()
# rest.quarterLength = 1/4


def audio(RIGHT_HAND,LEFT_HAND, title):
    # Create a stream to hold the triads
    left_holds = stream.Part()
    right_holds = stream.Part()

    # Create triads from the provided list

    prev = None
    length = 1/4
    print(LEFT_HAND)
    for notes in LEFT_HAND:
        print("in loop")
        print()
        print(notes)
        if(notes == ""):
            continue
        elif (notes == ['z'] or notes == ['Z'] or notes == 'z' or notes == 'Z'):
            rest = note.Rest(quarterLength=0.25)
            print("we are at a ZZZZ")
            left_holds.append(rest)
            print("applied append")
            prev = None
        else:
            chords = chord.Chord(notes)  # Each triad is a quarter note
            if (notes != prev):
                chords.quarterLength = length
                left_holds.append(chords)
                length = 1/4
            else:
                print("holding note: ")
                length = length + 1/4

            prev = chords
    



    prev = None
    length = 1/4
    prev = None
    length = 1/4

    for notes in RIGHT_HAND:
        print("in loop")
        print()
        print(notes)
        if(notes == ""):
            continue
        elif (notes == ['z'] or notes == ['Z'] or notes == 'z' or notes == 'Z'):
            rest = note.Rest(quarterLength=0.25)
            right_holds.append(rest)
            prev = None
        else:
            chords = chord.Chord(notes)  # Each triad is a quarter note
            if (notes != prev):
                chords.quarterLength = length
                right_holds.append(chords)
                length = 1/4
            else:
                length = length + 1/4

            prev = chords
    


    # Create a score to hold the triads
    score = stream.Score()
    score.insert(0, left_holds)
    score.insert(0,right_holds)

    # Save the score as a MIDI file
    output_path = f'{title}.mid'
    score.write('midi', fp=output_path)

    print("MIDI file saved at:", output_path)