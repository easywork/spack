#!/usr/bin/sh

if [ "$#" -ne 2 ] || ! [ -d "$1" ] || ! [ -e "$2" ]; then
      echo -e " \n Usage: fix-mux.sh shared_path host_list " >&2
      echo -e " shared path is the folder has the new namespace_db.py file that alll hosts can access" >&2
      echo -e " host_list file listing all the prepared hosts \n" >&2
      exit 1
fi

SHARE_PATH=$1
HOST_FILE=$2
CMD1="mv /usr/lib/vmware/vsepmux/bin/namespace_db.py /usr/lib/vmware/vsepmux/bin/namespace_db.py.bk"
CMD2="cp $SHARE_PATH/namespace_db.py /usr/lib/vmware/vsepmux/bin/namespace_db.py"
CMD3="/etc/init.d/vShield-Endpoint-Mux restart"
CMD4="/etc/init.d/vShield-Endpoint-Mux status"

for line in `cat $HOST_FILE`;
do
    host="$line"
    echo "working on $host"
    ssh -o "StrictHostKeyChecking no" root@"$host" "$CMD1;$CMD2;$CMD3;$CMD4"
done 