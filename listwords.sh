#!/bin/sh
a=1

until [ $a -gt 126 ]
do
	echo $a
	curl http://www.yougowords.com/5-letters-$a | tr -d '\n' | sed 's/.*<strong>Page [0-9][0-9]*:<\/strong>\([^<]*\)<.*/\1/' >> yougowords_5letter.txt
	a=`expr $a + 1`
done
