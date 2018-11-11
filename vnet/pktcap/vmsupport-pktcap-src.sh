#!/bin/sh

if [ $# -ne 3 ]
    then echo "usage: vmsupport-pktcap-src.sh vm_name ip src_port"
    exit
fi

vm_name=$1
#switchport=$(net-stats -l | grep $vm_name | awk {'print $1'})
switchport=$(net-stats -l | grep $vm_name | grep eth0 | awk '{print $1}')
ip=$2
port=$3
vm_worldID=$(esxcli network vm list | grep $vm_name | awk {'print $1'})
#nic=$(esxcli network vm port list -w $vm_worldID | grep "Team Uplink" | awk {'print $3'})
nic=$(esxcli network vm port list -w $vm_worldID | grep $switchport -A 10 | grep "Team Uplink" | awk {'print $3'})
timestamp=`date +%s`
kpath=$(pwd)/pcap-"$timestamp"
len=125s

mkdir $kpath
summarize-dvfilter > $kpath/dvfilter.txt
echo "packet capture on $date $vm_name $ip $port uplink:$nic switchport:$switchport" > $kpath/info.txt

### Packet capture before DFW
# pktcap-uw --switchport 83886242 --dir=0 --stage=0 --srcport 1023 --count 4 -o - | tcpdump-uw -enr -
pktcap-uw --switchport $switchport --dir=0 --stage=0 --ip $ip --tcpport $port -o $kpath/vds_d0s0.pcap &
PID1="$!"

### After DFW
# pktcap-uw --switchport 83886242 --dir=0 --stage=1 --srcport 1023 --count 4 -o - | tcpdump-uw -enr -
pktcap-uw --switchport $switchport --dir=0 --stage=1 --ip $ip --tcpport $port -o $kpath/vds_d0s1.pcap &
PID2="$!"

### uplink before encap
# pktcap-uw --uplink vmnic3 --dir=1 --stage=0 --srcip 192.168.61.33 --srcport 1023 --count 4 -o - | tcpdump-uw -enr -
pktcap-uw --uplink $nic --dir=1 --stage=0 --ip $ip --tcpport $port -o $kpath/nic_d1s0.pcap &
PID3="$!"

### uplink after encap
# pktcap-uw --uplink $vmnic3 --dir=1 --stage=1 --srcip 192.168.61.33 --srcport 1023 --count 4 -o - | tcpdump-uw -enr -
pktcap-uw --uplink $nic --dir=1 --stage=1 -o $kpath/nic_d1s1.pcap &
PID4="$!"

sleep $len
echo "packet capture saved to $kpath"

kill $PID1;                                                                                                                                             
kill $PID2;                                                                                                                                             
kill $PID3;                                                                                                                                             
kill $PID4;                                                                                                                                                

