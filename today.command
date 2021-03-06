#!/bin/zsh
cd `dirname $0`
#Split sentences
echo -n > new.txt
cat /Users/mac2018/Applications/Collection/maru/Raw/*.chl* | sed 's/ //g'| sed -e 's/\:443\,\"path\"\:\"\/api\/v1\.7\.4/\n/g' | >new.txt

#loop sentences
loop=($(cat new.txt | grep '/hall/machines","query":"date'|sed 's/.*hall_code=\([0-9]\{4\}\)&model_code=\([0-9]\{6\}\)".*202[0-9]\{5\}\(.*\)\(202[0-9]\{5\}\)\(.*\)\(202[0-9]\{5\}\).*/\6,\2,\1,\5/g'))
#empty data.txt
echo -n > data.txt
#no sort
for ((i=1; i<1+`echo ${#loop[*]}`; i++))
do echo ${loop[i]} > tmp.txt
code=($(grep -ao '^[0-9]\{8\},[0-9]\{6\},[0-9]\{4\}' tmp.txt))
cat tmp.txt | sed 's/machine_number/\n/g'| grep 'machine_id' | tr -d \\\\\"\: | sed -E "s/^([0-9]{4}),machine_id(.*),number_of_all_starts([0-9]{1,}|null),availabletrue.*bbs([0-9]{1,}|null),number_of_rbs([0-9]{1,}|null),.*/\2,\1,\3,\4,\5,$code/g" | sed 's/null/0/g' | tr -cd '0123456789\n\,' | tee -a data.txt
done

#Organize by element
cat data.txt > tmp.txt
grep -E '1[0-9]{3}$' tmp.txt | > data.txt

#multislump
cat new.txt | grep '/machine\/slump\/compare\"\,\"query\"\:\"date' | sed 's/machine_id/\n/g' | grep 'max\\\"\:[1-9]000\,\\\"min\\\"\:-[1-9]000'| tr -d \}\,\{\\\"time\\\"\:\\\" | tr -d \\\"\,\\\"value\\\"\: |sed 's/\\\\\\/,/g' | tr -d \\ | sed -E 's/\[\]/,0/g' | sed 's/\(.*\)x.*\([0-9]\{4\}\)nsbd.*\,\([-0-9]\{1,\}\).*/\3,\1/g' | sed -E 's/([-0-9]{1,}),[^0-9]*([0-9]*)[^0-9]*([0-9]*)[^0-9]*([0-9]*)[^0-9]*([0-9]*).*/\2\3\4\5,\1/g'| tee tmp.txt
#eachslump
cat new.txt | grep 'machine\/slump\"\,\"query\"\:\"date' | sed 's/.*machine_id\=\(.*\)HTTP\/1\.1\"\,\"headers\".*value\\\"\:\([-0-9]\{1,\}\)\(.*\)/\2,\1/g'| sed -E 's/\%20//g'|sed -E 's/([-0-9]{1,}),[^0-9]*([0-9]*)[^0-9]*([0-9]*)[^0-9]*([0-9]*)[^0-9]*([0-9]*).*/\2\3\4\5,\1/g' | grep -vE "[a-z]+[A-Z]+" | tee -a tmp.txt

sort -uk 1n -t , tmp.txt | > slump.txt

#to string
ksyu=($(cat new.txt | grep -m 1 'machine/models?hall' | sed -E 's/\{\\\"model_code\\\"\:\\\"/\n/g' | sed -E 's/^([0-9]{6}).*model_name\\\"\:\\\"(.*)\\\"\,\\\"count\\.*/\1,\2/g' | grep '\\u' | sed -E 's/\\\\/\\/g'))
echo $ksyu | sed 's/ /\n/g' | tee ksyu.txt

python maru.py

newcsv=$(ls -1t /Users/mac2018/Applications/Collection/linkdata/*.csv | head -1)    #get only pass
filename=${newcsv##*/}???#filenameandextention
fnonly=${filename%.*}   #filename
#Wildcards are disabled by enclosing them in ""
#Double parentheses for string comparison operations
#2/1branch nana
#hollcode pickup grep -m 1 
hollna=$(cut -f 8 -d "," data.txt |grep -m 1 '[0-9]\{4\}')

if [ $hollna -eq 1864 ]; then
	store="maruhuku"
elif [ $hollna -eq 1411 ]; then
	store="nana"
else
	echo "error"
fi

fileNum=0
extension="csv"

if [[ $fnonly = maruhuku* ]] || [[ $fnonly = nana* ]]; then
	echo "Oops! it's error"
	echo "Cancel and finish"
else
	er=($( cut -f 1 -d "," $newcsv))
	daiban="null"
	for ((i=1;i<1+`echo ${#er[*]}`;i++))
		do
		test $daiban = null && daiban=$er[i]
		if [ $daiban -eq `echo $(($er[i]))` ]; then
			echo "ok$er[i]"
			daiban=$((daiban + 1))
		elif [ 0 -eq `echo $(($er[i]))` ]; then
			echo "error$daiban"
			daiban=`expr 1 + $daiban`
		elif [ $daiban -gt `echo $(($er[i]))` ]; then
			echo "error$daiban"
			print "????????????"
			exit
		else
			while [ $daiban -ne `echo $(($er[i]))` ]
				do
				echo $daiban
				daiban=`expr 1 + $daiban`
			done
		daiban=`expr 1 + $daiban`
		echo "ok$er[i]"
		fi
	done
fi
	
while ls /Users/mac2018/Applications/Collection/linkdata/*.csv | grep -w $store >/dev/null; do
	fileNum=`expr $fileNum + 1`
	store=${store}_${fileNum}
done
mv $newcsv /Users/mac2018/Applications/Collection/linkdata/${store}.${extension}

print "fin"