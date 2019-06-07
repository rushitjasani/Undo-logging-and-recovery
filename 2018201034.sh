#!/bin/bash

arg_cnt="$#" 

if [ $arg_cnt -eq 1 ]
then
    python 2018201034_2.py "$1"
else
    python 2018201034_1.py "$1" "$2"
fi