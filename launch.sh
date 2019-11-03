#! /bin/bash

if [ $# != 5 ];then
  echo "<addr> <port> <namefile dict> <nb authors> <nb politicians>"
  exit 0
fi

for i in `seq 1 $4`;do
  python3 launch_auteur.py $1 $2 $3 &
done

for i in `seq 1 $5`;do
  python3 launch_politicien.py $1 $2 $3 &
done
