import numpy as np
import pretty_midi
import glob

def piano_roll_to_pretty_midi(piano_roll, fs=1, program=0):
    '''Convert a Piano Roll array into a PrettyMidi object
     with a single instrument.
    Parameters
    ----------
    piano_roll : np.ndarray, shape=(128,frames), dtype=int
        Piano roll of one instrument
    fs : int
        Sampling frequency of the columns, i.e. each column is spaced apart
        by ``1./fs`` seconds.
    program : int
        The program number of the instrument.
    Returns
    -------
    midi_object : pretty_midi.PrettyMIDI
        A pretty_midi.PrettyMIDI class instance describing
        the piano roll.
    '''
    notes, frames = piano_roll.shape
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program)

    # pad 1 column of zeros so we can acknowledge inital and ending events
    piano_roll = np.pad(piano_roll, [(0, 0), (1, 1)], 'constant')

    # use changes in velocities to find note on / note off events
    velocity_changes = np.nonzero(np.diff(piano_roll).T)

    # keep track on velocities and note on times
    prev_velocities = np.zeros(notes, dtype=int)
    note_on_time = np.zeros(notes)

    for time, note in zip(*velocity_changes):
        # use time + 1 because of padding above
        velocity = piano_roll[note, time + 1]
        time = time / fs
        if velocity > 0:
            if prev_velocities[note] == 0:
                note_on_time[note] = time
                prev_velocities[note] = velocity
        else:
            pm_note = pretty_midi.Note(
                velocity=prev_velocities[note],
                pitch=note,
                start=note_on_time[note],
                end=time)
            instrument.notes.append(pm_note)
            prev_velocities[note] = 0
    pm.instruments.append(instrument)
    return pm

def get_piano_roll(midifile):
	#midi_data = pretty_midi.PrettyMIDI('test.midi')
	midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
	piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
	piano_roll = piano_midi.get_piano_roll(fs=20)
	print(piano_roll.shape)
	return piano_roll

def decode(test):
    test=test[:-1] #takes in the endoded data and looks at all lines except the last line (always blank)
    output=test.split("\n") #splits on newline character
    res = len(output) # this is how many samples long the song will be
    arr=np.zeros((128,res)) #initialising a piano roll array with zeros for this length
    timeindex=0
    for x in output:
        newx=x.replace(")(", "-") #this is the seperator between different note/velocity pairs in the same sample
        newx=newx.replace("(","") #removing the outer bracket
        newx=newx.replace(")","") #removing the other outer bracket
        noteGroup = newx.split("-") # splitting into separate note/velocity pairs
        for n in noteGroup:
            if n != "#":
                s=len(n.split(",")) #this is checking to make sure there aren't more commas then expected
                if s==2: # if there is only one  comma then note/velocity follows expected format
                    note,velocity = n.split(",") # splitting into note/velocity
                    if velocity.count("#")>0 or velocity.count('.')>1: # these are flaws in generation so replace with 0
                        velocity=0
                        note = 0
                    elif note.count("#")>0 or note.count('.')>1: # these are flaws in generation so replace with 0
                        note=0
                        velocity = 0
                    note=float(note) #casting to avoid an error

                    if int(note)>126: #casting into int if over 126 it isnt a valid midi note so replace with 0
                        note =0
                        velocity = 0
                    if velocity=="": #checking for a common error when encoding velocity if found replace with 0
                        velocity=0
                        note = 0
                    if int(float(velocity))>126: #casting to int if over 126 it isnt a valid midi vel so replace with 0
                        velocity=0
                        note = 0
                    arr[int(note),timeindex]=velocity # updating point in piano roll with velocity
        timeindex=timeindex+1 #incrementing through to next time index (sample) in song
    #arr=arr.T
    return arr

# encoding both notes and velocity into same string
def encode(arr):
    timeinc=0 #time increment
    outString="" #string initially blank
    for time in arr: #looping through the columns of the piano roll array
        # (actually looping through rows of transposed piano roll so practically the same)
        notesinc = -1 #initialising note increment to -1 will almost immediately be updated to 0
        if np.all(time==0):#if everything in this time increment is 0 write a # to the encoded string (nothing playing)
            outString=outString+"#"
        for vel in arr[timeinc]: #loops through the current time increment (array of velocities)
            notesinc=notesinc+1 #matching the index for array at this time increment to a note
            # so notes and Vel can be grouped together
            if vel != 0: #if Vel!=0 a note is being played so add a note/velocity pair to the encoded file
                noteRep="("+str(notesinc)+","+ str(vel)+")" #this is the combined encoding format
                outString=outString+noteRep
        outString=outString+"\n" #now on a new time increment so move to a new line in encoded file
        timeinc = timeinc+1 #incrementing the sample that is currently being encoded
    return outString

#similar to above function but only encodes notes
def encodeNotes(arr):
    timeinc=0
    outString=""
    for time in arr:
        notesinc = -1
        if np.all(time==0):
            outString=outString+"#"
        for vel in arr[timeinc]:
            notesinc=notesinc+1
            if vel != 0:
                noteRep=str(notesinc) + " "
                outString=outString+noteRep
        outString=outString+"\n"
        timeinc = timeinc+1
    return outString

#gets an encoded version of the file with note/vel and with notes only
#I use this because when reading in from midi file sometimes velocity doesn't match values expected when looking at
#encoded training data
#This may be a small inconsistancy in the prettyMidi conversion but by looking at notes only results are as expected
#i.e the songs generated by sampling the training sample randomly have 100% overlap with training data
def midiToArray(midifile):
    pr = get_piano_roll(midifile)
    arr = pr.T
    outString = encodeNotes(arr) #encoding notes only
    lines=outString.split("\n")
    encodedWithAll=encode(arr) #combined encoding
    linesWithAll = encodedWithAll.split("\n")
    print(lines)
    print("len="+str(len(lines)))
    return lines,linesWithAll#stringRep


def skimFile(linesGenerated,linesGeneratedAll,linesInDataset):
    newLines = [] #array for new song
    i=1
    for l in linesGenerated: #loops through generated midi
        print("checking line: "+str(i))
        i+=1
        if linesInDataset.count(str(l)+"\n")>0: #checks if line is found anywhere in training data
            newLines.append(str(linesGeneratedAll[i-1])+"\n") #if match found add to new song
            print("match -"+str(l))
            #file1.write(l)
        else:
            print("no match -"+l) #no match don't add to new song

    inDataset=len(newLines)/(len(linesGenerated)-1) # getting % found in dataset (-1 because last sample always blank)
    print(inDataset)
    stringRep=""
    for l in newLines:
        stringRep=stringRep+l
    #print(stringRep)
    return stringRep #returning a string version of the new (skimmed) song

with open(r"C:\Users\brenn\PycharmProjects\RNN2\FullyEncoded\fulldataNotes.txt") as text:
    linesInDataset = text.readlines() #all note combinations in the maestro dataset

#reading in the generated song we want to skim and getting encoded data back
midiArray,midiArrayWithAll=midiToArray(r"C:\Users\brenn\Desktop\generatedData\generated\LSTM\split\alt song\25epo\piano.midi")
#getting string version of new song and content overlap with dataset
skimmed=skimFile(midiArray,midiArrayWithAll,linesInDataset)
#generating a MIDI file from skimmed song
decoded = decode(skimmed)
fs = 20
pm = piano_roll_to_pretty_midi(decoded, fs=fs, program=2)
pm.write("skimmedPiano.midi")



