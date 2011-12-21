C=javac 

J=java -Xmx2G

all: filter

filter:
	$C TweetFilter.java
	$C TweetAnnotation.java
	$C AnchorSearcher.java

