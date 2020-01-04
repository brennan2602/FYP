import numpy as np
import os
from os import path
import shutil
import pandas as pd

data = pd.read_csv('maestro-v2.0.0.csv')
#my_data = np.genfromtxt('maestro-v2.0.0.csv', delimiter=',', dtype=str,encoding="utf8")
dstTrain="\\train\\"
dstVal="\\validate\\"
dstTest="\\test\\"


#print(my_data.shape)
print(data.head())
splits = data['split'].tolist()
midi = data['midi_filename'].tolist()

val = midi[1].split('/')
val=val[1]
print(val)
for x in range(0,len(midi),1):
    val = midi[x].split('/')
    val = val[1]
    print(val)
#     print(splits[x])
#     print(midi[x])
    if splits[x]=="train":
        dst=dstTrain+val
        print(dst)
        os.makedirs(dst)
        shutil.copy(midi[x], dst)
    if splits[x]=="test":
        dst=dstTest+val
        print(dst)
        os.makedirs(dst)
        shutil.copy(midi[x], dst)
    if splits[x]=="validation":
        dst=dstVal+val
        print(dst)
        os.makedirs(dst)
        shutil.copy(midi[x], dst)

# for f in files:
#     shutil.copy(path.join(src, f), dst)