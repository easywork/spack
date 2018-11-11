#! /bin/bash

filename=$1
dbname=$2
output=$3
if [[ -z "$1" || -z "$3" ]]; then
	echo "pls provide the input and/or output"
	exit
fi

x=''

while read line
do
table="$line"
x="$x -t $table"
done < "$filename"

echo "running CLI:  pg_dump -Fc -U secureall -a $x -d $dbname > $output.sql"
pg_dump -Fc -U secureall -a $x -d $dbname > $output.sql

#echo "running CLI:  pg_dump -c -U secureall $x -d $dbname > $output.sql"
#pg_dump -c -U secureall $x -d $dbname > $output.sql

