#!/bin/bash
for i in `seq 1 $1`;
do
        python client.py $i & python client.py $i & python client.py $i & 
done    
