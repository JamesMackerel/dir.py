#!/bin/bash

for file in ./*
do
    filename=$(basename "$file" .ape)

    if [ "$(basename "$file")" != "$0" ] 
    then
        ffmpeg -i "$filename.ape" "$filename.wav"
    fi
done

