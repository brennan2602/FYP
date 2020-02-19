import random
def genNote():
    num=random.randint(21,108) #this is the range a piano covers in MIDI, picking a random note
    vel=float(random.randint(0,127)) #picking a velocity value
    note="("+str(num)+","+str(vel)+")" #this is a note representation (combined encoding)
    #print(note)
    return note

file1 = open("generatedPureRand.txt", "a")
#generating 500 lines of a text file 500 sample long song
for i in range(0,500):
    line=""
    numNotes = random.randint(0, 10) #how many notes to play on a line 0-10 for each finger that could possibly play
    if numNotes == 0:
        line="#" #Write "#" if no notes being played
    else:
        for j in range(0,numNotes): # will generate between 1-10 notes for this line of the sample
            note=genNote()
            line=line+note
    line=line+"\n"
    print(line)
    file1.write(line) #writing to encoded file
file1.close()