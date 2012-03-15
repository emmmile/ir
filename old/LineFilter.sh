### Main script stars here ###
FILE1="../data/i3terroni-dataset/prova1.#"			#file filtrato con grep " #"
FILE2="../data/i3terroni-dataset/prova2.#"			#file filtrato con grep "#"

FILEOUT="../data/i3terroni-dataset/withoutHashtag.#"	#tweets non considerati nella vecchia analisi

if [[ -f $FILEOUT ]]; then
	rm ../data/i3terroni-dataset/withoutHashtag.#
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
eof2=0			#variabile per controllare l'end of file
#IFS=$(echo -en "\n")  # Set loop separator to end of line
IFS=$'\n' #BUG PROBABILMENTE QUI!!! MA NON RIESCO A LEVARLO!!!

exec 6<"$FILE1"
exec 7<"$FILE2"

read line1 <&6
while [[ $eof1 -eq 0 ]]
do
	while [[ $eof2 -eq 0 ]]
	do
		if read line2 <&7; then
			while [[ $eof1 -eq 0 && $line1 != $line2 ]]	
			do
				echo $line2>>"$FILEOUT"	#scrittura file
				if read line2 <&7; then
					echo ciao > /dev/null
				else
					eof2=1
				fi
			done

			if [[ $eof1 -eq 1 ]]; then
				eof=1
				echo $line2>>"$FILEOUT"	#scrittura file
			else
				if read line1 <&6; then
					echo ciao > /dev/null
				else
					eof1=1
				fi
			fi
		else
			eof2=1
		fi
	done
done

IFS=$BAKIFS
exit 0

