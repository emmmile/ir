#!/bin/bash
#script dei i3terroni modificato

#LIST=$(ls | grep block)
LIST="./data/new.text.sorted"
# sed 's/#//g' #per togliere anche l' "#" dal testo
for i in $LIST; do cat $i | sed 's/@[^ ]*//g' | sed 's/#//g' | sed -r 's@https?://[^ ]*@@g' | sed "/^[[:digit:]]*\s[[:digit:]]*\s*$/d" > "./data/new.text.sorted.cleaned.withoutHash"; done
