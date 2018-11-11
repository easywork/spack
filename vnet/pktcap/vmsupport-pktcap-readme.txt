/tmp/vmsupport-pktcap # ./vmsupport-pktcap-src.sh
usage: vmsupport-pktcap-src.sh vm_name ip src_port

Example 1 -- SM-glu13 is the source VM , ip 192.168.61.33 port 1022, run the script on the source host

/tmp/vmsupport-pktcap # ./vmsupport-pktcap-src.sh SM-glu13 192.168.61.33 1022

Example 2 -- SM-glu13 is the destination VM , ip 192.168.61.33 port 24007

In the case that two VMs on the same host, then the script need to run on the same host twice, given src port once and dst port once.
/tmp/vmsupport-pktcap # ./vmsupport-pktcap-dst.sh SM-glu13 192.168.61.33 24007, run the script on the destination host

The packet capture will be saved to a folder pcap-timestamp
 
/tmp/vmsupport-pktcap # ls -la
total 28
drwx------    1 356214   203            512 May  4 11:27 .
drwxrwxrwt    1 root     root           512 May  4 11:28 ..
drwxr-xr-x    1 root     root           512 May  4 11:25 pcap-1493897157
drwxr-xr-x    1 root     root           512 May  4 11:26 pcap-1493897164
drwxr-xr-x    1 root     root           512 May  4 11:27 pcap-1493897269
-rwxr-xr-x    1 356214   203           2463 May  4 10:58 vmsupport-pktcap-dst.sh
-rwxr-xr-x    1 356214   203           2462 May  4 11:19 vmsupport-pktcap-src.sh

The script is set to run for 125 seconds

kpath=$(pwd)/pcap-"$timestamp"
len=125s 

The scripts are now in host -- esxmi3vpdc42.selfdcvdc.nuvolait path - -/tmp/vmsupport-pktcap

/tmp/vmsupport-pktcap # hostname
esxmi3vpdc42.selfdcvdc.nuvolait
/tmp/vmsupport-pktcap # pwd
/tmp/vmsupport-pktcap