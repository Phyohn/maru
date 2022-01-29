#!/bin/zsh
cd `dirname $0`
cat cd /Users/mac2018/Applications/Collection/maru/formerge/*.csv | grep '[0-9]\{3,\}' |>new.txt
sort -uk 1n -t , new.txt | > data.txt

python merge.py

print "fin"