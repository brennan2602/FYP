import random
def genNote():
    num=random.randint(21,108)
    vel=float(random.randint(0,127))
    note="("+str(num)+","+str(vel)+")"
    #print(note)
    return note
file1 = open("generatedPureRand.txt", "a")

for i in range(0,500):
    line=""
    numNotes = random.randint(0, 10)
    if numNotes == 0:
        line="#"
    else:
        for j in range(0,numNotes):
            note=genNote()
            line=line+note
    line=line+"\n"
    print(line)
    file1.write(line)
file1.close()