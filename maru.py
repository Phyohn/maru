# maru.py
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

slump = pd.read_csv('slump.txt',names=('eigenvalue','difference'))
data = pd.read_csv('data.txt',names=('eigenvalue','dai','Rotation','BB','RB','date','model','holl'))
merged = pd.merge(slump, data)

merged = merged.drop_duplicates()
merged = merged.sort_values('dai')
#case error
daiser = merged.loc[:,'dai']
merged.insert(0,'dailist', daiser)
dailist = pd.read_csv('dailist.txt',names=('dailist','ku'))
merged = pd.merge(dailist, merged, how='outer')
merged = merged.fillna(0).astype('int64')


ksyu = pd.read_csv('ksyu.txt', header=None)
model = (ksyu.iloc[:,0]).values.tolist()
kisyumei = (ksyu.iloc[:,1]).values.tolist()

merged = merged.replace(model,kisyumei)
comp = merged.reindex(columns=['dai','Rotation','BB','RB','difference','date','model'])
#comp = comp.sort_values('dai')

now = datetime.datetime.now()
strdate = now.strftime('%m:%d %H:%M:%S')
comp.to_csv(f'../{strdate}.csv', header=False, index=False)

quit()
