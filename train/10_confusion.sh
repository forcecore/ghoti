#!/bin/bash
# This script runs make mix, make train, make predict iteration multiple times
# and generates confusion table.

prefix=test
tmp_dir=confusion
iterations=100

make data
rm -f accu

if [ ! -d $tmp_dir ] ; then
	mkdir $tmp_dir
fi

for i in $(seq 1 $iterations) ; do
	make mix
	make train
	make predict >> accu
	mv $prefix.predict $tmp_dir/$prefix.$i.predict
	mv $prefix $tmp_dir/$prefix.$i
done

./cmp.pl $tmp_dir/$prefix 1 $iterations
