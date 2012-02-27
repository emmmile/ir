
.phony:	clean

all:
	javac -sourcepath . -classpath .:lib/libsvm.jar:lib/weka.jar:lib/wlsvm.jar main/*.java

clean:
	-rm main/*.class
	-rm commands/*.class
	-rm classifier/*.class
	-rm documents/*.class
	-rm util/*.class

