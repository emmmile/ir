#!/bin/bash
# Shell script utility to read a file line line.

# User define Function (UDF)
processLine(){
  line="$@" # get all args
  #  just echo them, but you may need to customize it according to your need
  # for example, F1 will store first field of $line, see readline2 script
  # for more examples
  # F1=$(echo $line | awk '{ print $1 }')
  echo $line
}
 
### Main script stars here ###
FILE1="./data/new.text.sorted"			#file con hashtag (senza simboli codificati in HTML) 
FILE2="./data/new.text.sorted.annotation"	#file di annotazioni relativo al file "FILE1"

FILEOUT1="./data/new.text.sorted.filtered"	#file filtrato solo sulle righe con hashcode
FILEOUT2="./data/new.text.sorted.annotation.filtered" #file filtrato solo sulle righe con hashcode

if [[ -f $FILE1 ]]; then
	rm ./data/*.filtered
fi

# make sure file exist and readable
if [[ ! -f $FILE1 || ! -f $FILE2 ]]; then
	echo "I/O error : does not exists"
	exit 1
elif [[ ! -r $FILE1 || ! -f $FILE2 ]]; then
	echo "I/O error: can not read"
  	exit 2
fi

# read $FILE using the file descriptors
 
BAKIFS=$IFS
line1=""
line2=""
eof1=0			#variabile per controllare l'end of file
#IFS=$(echo -en "\n")  # Set loop separator to end of line
IFS=$'\n' #BUG PROBABILMENTE QUI!!! MA NON RIESCO A LEVARLO!!!

exec 6<"$FILE1"
exec 7<"$FILE2"
while [[ $eof1 -eq 0 ]]
do
	if read line1 <&6; then
		if [[ $line1 == *#* ]]; then	#se la riga letta contiene un "#"
			read line2 <&7
			echo $line1>>"$FILEOUT1"	#scrittura file (time userID tweet)+  #o BUG nella STAMPA
			echo $line2>>"$FILEOUT2"	#scrittura file (time userID (annotation)+)+
		fi
	else
		eof1=1
	fi

done

IFS=$BAKIFS
exit 0

