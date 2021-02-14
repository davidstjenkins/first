#!/bin/bash
A=($(ls boot/vmlinuz* | cut -c 14- | cut -d- -f1))
j=${#A[*]}
i=1
echo ${A[*]}
echo $j 
while [ $i -lt $j ]
do 
  u=$(echo ${A[$i]} | cut -d. -f1)
  v=$(echo ${A[${i}-1]} | cut -d. -f1)
  if [ $u -lt $v ]
    then u=$v
  fi
  let i++
done
B=($(ls boot/vmlinuz-${u}* | cut -d. -f2))
j=${#B[*]}
i=1
while [ $i -lt $j ]
do
  w=$(echo ${B[$i]} | cut -d. -f2)
  x=$(echo ${B[$i-1]} | cut -d. -f2)
  if [ $w -lt $x ]
    then w=$x
  fi
  let i++
done
C=($(ls boot/vmlinuz-${u}.${w}* | cut -d. -f3 | cut -d- -f1))
j=${#C[*]}
i=1
while [ $i -lt $j ]
do
  y=$(echo ${C[$i]} | cut -d. -f3)
  z=$(echo ${C[$i-1]} | cut -d. -f3)
  if [ $y -lt $z ]
    then y=$z
  fi
  let i++
done
D=($(ls boot/vmlinuz-${u}.${w}.${y}* | cut -d- -f3))
j=${#D[*]}
i=1
while [ $i -lt $j ]
do
  a=$(echo ${D[$i]} | cut -d. -f3)
  b=$(echo ${D[$i-1]} | cut -d. -f3)
  if [ $a -lt $b ]
    then a=$b
  fi
  let i++
done
echo vmlinuz-${u}.${w}.${y}-${a}-generic

