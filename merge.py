# merge.py
import cv2
import base64
import numpy as np
from PIL import Image
import io
import os
import pathlib
import datetime
import time
import platform
import codecs
import pandas as pd

data = pd.read_csv('data.txt',names=('dai','Rotation','BB','RB','difference','date','machine'))
daiser = data.loc[:,'dai']
data.insert(0,'dailist', daiser)
print(data.loc[:,:'date'])

dailist = pd.read_csv('dailist.txt',names=('dailist','ku'))
merged = pd.merge(dailist, data, how='outer')
merged = merged.fillna(0)
#If there is a character string, the whole cannot be replaced with astype'int64', so specify the column name and change the type.
merged = merged.astype({'dai': 'int64','Rotation':'int64','BB':'int64','RB':'int64','difference':'int64','date':'int64'})

comp = merged.reindex(columns=['dai','Rotation','BB','RB','difference','date','machine'])

now = datetime.datetime.now()
strdate = now.strftime('%m:%d %H:%M:%S')
comp.to_csv(f'../{strdate}.csv', header=False, index=False)

quit()
