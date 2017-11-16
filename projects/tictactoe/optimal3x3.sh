#!/bin/bash
source ./vars
#Play 10 times against random agent in classical 3x3 grid with k=3. No loose is expected
arg="c_${srcname,,}"
argrand="c_randy"
for ((i=0 ; 10 - $i ; i++))
    do 

    python3 game_write.py 3 3 3 $arg $argrand temp
    winner="`cat temp | cut -d';' -f1`"
    if [ $winner -gt 1 ]; then
        echo "Your agent managed to loose against random agent. Please check again your source code."
        exit -1
    fi
    
done

echo "Your agent is at least better than random on 3x3. Great."

for ((i=0 ; 10 - $i ; i++))
    do 

    python3 game_write.py 3 3 3 $arg $arg temp
    winner="`cat temp | cut -d';' -f1`"
    if [ $winner -ne 0 ]; then
        echo "Both agent should meet a tie at each game. Please check again your code"
        exit -1
    fi
    
done

echo "Your agent is correct on 3x3 ! Further tests to be executed outside the submission platform will determine the performance (playtime + score) of your agent"
