import numpy as np
import pretty_midi
import glob

#converts a midi file to an array (piano roll representation)
def get_piano_roll(midifile):
	midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
	piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
	piano_roll = piano_midi.get_piano_roll(fs=25)
	print(piano_roll.shape)
	return piano_roll

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


files=glob.glob(r"C:\Users\brenn\PycharmProjects\FYP\customDataset\*.mid") # reading in from folder and getting all .mid
print(files)

#this loop is writing all encoded .mid files to the same file
for f in files:
    pr = get_piano_roll(f) #getting piano roll for current file
    arr = pr.T #transpose array
    outString= encode(arr) #convert array into a string
    file1 = open("CustomPoly.txt","a")
    file1.write(outString) #writing all encoded strings to same file

file1.close()

#this loop writes all encoded .mid files to seperate files
for f in files:
    outString=""
    x= f.split("\\")[-1]
    #print(x)
    name=x.split(".mid")[0] #getting name for file
    pr = get_piano_roll(f) #getting piano roll for file
    arr = pr.T
    outString= encode(arr)
    file1 = open(name+"Poly.txt","a") #getting file name for individual .mid file
    file1.write(outString) #writing to file

    file1.close()




