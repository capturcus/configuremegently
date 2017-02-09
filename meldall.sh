#!/bin/bash
for i in `cat paths.txt`;
do
    path="${i/#\~/$HOME}"
    touch merged/$(basename $i)
    meld $path merged/$(basename $i) dotfiles/$(basename $i) ;
done
