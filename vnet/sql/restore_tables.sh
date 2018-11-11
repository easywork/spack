#! /bin/bash

filename=$1
dbname=$2
dump=$3
if [[ -z "$1" || -z "$2" || -z "$3" ]]; then
	echo "One of these parameters -- table list, DB name, dump file is missed"
	exit
fi

x=''

while read line
do
table="$line"
x="$x -t $table"
done < "$filename"

echo "running CLI:  pg_restore -U secureall $x -d $dbname $dump"
pg_restore -U secureall $x -d $dbname $dump
