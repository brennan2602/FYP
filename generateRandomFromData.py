import glob
import random
import pretty_midi
import numpy as np


def generateFromData(lines):
    i=0
    outString=""
    while i<=1500: #will generate a song that is 1500 samples long
        num = random.randint(1, len(lines)) #picking a random number between 1 and the length of the encoded data file
        #print(str(len(lines))+ " - "+str(num))
        line=lines[num-1] # getting a random encoded line from the dataset
        numSample= random.randint(1,20) # deciding how long to hold on a sample for (random between 1 and 20)
        for j in range(0, numSample):
            if i<=1500: #another limit to ensure song is under 1500 samples long
                outString=outString+line
            i+=1
    return outString

#taken from prettyMidi docs
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
                #
                # This error checking is likely redundant given the encoded file isn't coming from a ML model
                # The fact generated file is coming from sampled encoded training file should mean there are no issues
                # Checks are just kept here to maintain consistency across scripts and as a precaution
                #
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

#going through directory of encoded datasets
files=glob.glob(r"C:\Users\brenn\PycharmProjects\FYP\venv\encodedFiles\*.txt")

for f in files:
    x= f.split("\\")[-1]
    name=x.split(".txt")[0]
    print(name)
    with open(f) as text:
        lines = text.readlines()
        #print(lines)
    #lines is an encoded training file
    generated = generateFromData(lines) #this is where the random sampling/generation is done
    decoded = decode(generated) #decoding random generation
    fs = 20
    pm = piano_roll_to_pretty_midi(decoded, fs=fs, program=2) #converting to midi
    pm.write("GenWith"+name+".midi")
