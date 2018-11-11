#! /bin/bash

filename=$1
dbname=$2

if [[ -z "$1" || -z "$2" ]]; then
        echo "One of these parameters -- table list, DB name"
        exit
fi

while read line
do
table="$line"
echo "psql -U secureall -d $dbname -c "drop table $table""
#psql -U secureall -d $dbname -c "drop table $table"
psql -U secureall -d $dbname -c "delete from $table"
done < "$filename"
