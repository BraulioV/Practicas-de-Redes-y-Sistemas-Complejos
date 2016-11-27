#!/bin/bash
# Used to check the runtime.

MPATH=/home/ECSC/aquirin/AQUIRIN/program/VisualScienceMaps
CPATH=/home/ECSC/aquirin/AQUIRIN/program/VisualScienceMaps/CheckNets/create

SIZE=300
SYMETRY=1
DIAGVALUE=0
TYPE=1		# 0: int, 1: float
MIN=1
MAX=999
PROBAINFINITY=0.0

# Chronometer all the algorithms on all the maps

LISTALGO="$MPATH/Original-Pathfinder/origpf-C1 $MPATH/Binary-Pathfinder/binpf-C18 $MPATH/Fast-Pathfinder/fastpf-C235 $MPATH/MST-Pathfinder/mstpf-prac-C5000 $MPATH/MST-Pathfinder/mstpf-theo-C5000"
echo $LISTALGO

while true
do

map=/tmp/map.net
$CPATH $SIZE $SYMETRY $DIAGVALUE $TYPE $MIN $MAX $PROBAINFINITY > $map

for algo in `echo $LISTALGO`
do
		TPS=`($algo $map > /dev/null) 2>&1 | cut -f3 -d' '`
		#printf "%s %s " $algo $map
		#($algo $map > /dev/null) | grep "Temps"
		printf "$TPS "
done
printf "\n"

done
