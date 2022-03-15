# maru.py
#python -i
import cv2
import base64
import numpy as np
from PIL import Image
import io
import os
import pathlib
import datetime
import sys
import time
import platform
import codecs
import pandas as pd

def csv_stdout(df_c):
	return df_c.to_csv(sys.stdout)

def intdate():
	today = datetime.datetime.now()
	intdt= int(today.strftime('%Y%m%d'))

def yes_no_input():
	while True:
		choice = input("           OK? [y/N]: ( q = quit )").lower()
		if choice in ['y', 'ye', 'yes']:
			return True
		elif choice in ['n', 'no']:
			return False
		elif choice in ['q', 'Q']:
			return quit()

slump = pd.read_csv('slump.txt',names=('eigenvalue','difference'))
data = pd.read_csv('data.txt',names=('eigenvalue','dai','Rotation','BB','RB','date','model','holl'))
merged = pd.merge(slump, data)

merged = merged.drop_duplicates()
merged = merged.sort_values('dai')
#case error
daiser = merged.loc[:,'dai']
merged.insert(0,'dailist', daiser)
#dailist branch 1864maru 1411nana
hollna = data['holl'].values[1]
if hollna == 1864:
	print ('1864maru')
	dailist = pd.read_csv('dailistmaru.txt',names=('dailist','ku'))
elif hollna == 1411:
	print ('1411nana')
	dailist = pd.read_csv('dailistnana.txt',names=('dailist','ku'))
else:
	print ('error')

merged = pd.merge(dailist, merged, how='outer')
merged = merged.fillna(0).astype('int64')


ksyu = pd.read_csv('ksyu.txt', header=None)
model = (ksyu.iloc[:,0]).values.tolist()
kisyumei = (ksyu.iloc[:,1]).values.tolist()

merged = merged.replace(model,kisyumei)
#max column plus
merged['max'] = int(0)
comp = merged.reindex(columns=['dai','Rotation','BB','RB','difference','max','model','date'])
comp.dtypes

#auto seriesmachine bank
#pd.Series.unique()
#defdai = comp.loc[:,'model'].unique()

#series to df
#defdaidf = pd.DataFrame(defdai)
#defdaidf.insert(0,'namebank', defdai)
#defdaidf = defdaidf.astype({'namebank':'str'})
#dainame = pd.read_csv('namebank.csv',names=('namebank','neoname'))
#dainame = dainame.astype({'namebank':'str','neoname':'str'})
#drop_duplicates(subset=['namebank']
#dainame = dainame.drop_duplicates(subset=['namebank'])
#newdailist = pd.merge(defdaidf, dainame, how='outer')
#newdailist = newdailist.reindex(columns=['namebank','neoname'])
#newdailist.to_csv('./namebank.csv', header=False, index=False)

#auto model_name_bank
model_name_df = pd.DataFrame(comp['model'].drop_duplicates())
model_name_df['fuga'] = '0'
rename_list_df = pd.read_csv('namebank.csv',names=('model','renamed_model_name'))
merged_model_name_df = pd.merge(model_name_df, rename_list_df , how='outer').drop(columns='fuga')
sorted_model_df = merged_model_name_df.sort_values('renamed_model_name', na_position='first')
empty_value = (sorted_model_df['renamed_model_name'].isnull())

if empty_value.sum() > 0 :
	csv_stdout(sorted_model_df)
	new_model_list = (sorted_model_df['model'])[empty_value].tolist()
	renamed_new_model_list = []
	for new_model in new_model_list:
		newshortname = input(f"new model arrive. {new_model}  (q = quit) Input newname. ")
		if newshortname == "q" :
			print("Finish!")
			quit()
			brake
		else:
			print(f'{new_model} is "{newshortname}"')
			if yes_no_input():
				renamed_new_model_list.append(newshortname)	
			else:
				pass
	'''	
	create a zipped list of tuples from above lists
	'''
	
	zippedlist =  list(zip(new_model_list, renamed_new_model_list))
	
	'''
	create df
	'''
	df_by_list = pd.DataFrame(zippedlist, columns = ['model', 'renamed_model_name'])
	added_sorted_model_df = pd.merge(sorted_model_df, df_by_list, on=('model', 'renamed_model_name'), how = 'outer').drop_duplicates(subset='model', keep='last')
	#sorted_model_df = sorted_model_df.replace( new_model_list, renamed_new_model_list)
	print("done!")
	sorted_model_df = added_sorted_model_df.sort_values('renamed_model_name', na_position='first')
else:
	pass

print("all model name has arrived")
sorted_model_df.to_csv('./namebank.csv', header=False, index=False)


#rename
dailist_df =  pd.read_csv('namebank.csv', header=None)
longname_list = (dailist_df.iloc[:,0]).values.tolist()
shortname_list = (dailist_df.iloc[:,1]).values.tolist()
comp = comp.replace(longname_list,shortname_list)

now = datetime.datetime.now()
strdate = now.strftime('%m:%d %H:%M:%S')
comp.to_csv(f'/Users/mac2018/Applications/Collection/linkdata/{strdate}.csv', header=False, index=False)
#test
quit()
