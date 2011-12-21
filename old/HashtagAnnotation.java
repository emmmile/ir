import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.Set;


public class HashtagAnnotation {
	
	private static class Topic{
		String an;
		float rho;
		
		public Topic(String s, float f){
			an = s;
			rho = f;
		}
	}
	
/*	private static class WeightTopic{
		String userId;
		float rhoSum;
		
		public Topic(String s, float f){
			an = s;
			rho = f;
		}
	}*/
	
	private static HashMap<String, Topic[]> hashmap_create(BufferedReader file) throws IOException{
		HashMap<String,Topic[]> hm = new HashMap<String,Topic[]>();
		String temp;
		
		String key;
		String [] annotation;
		Topic[] t ;
		
		while ((temp = file.readLine()) != null) {
			temp = temp.replaceAll(" # ", "#");
            annotation = temp.split("#",2);
            
            key = annotation[0];
            annotation = annotation[1].split("#");
            t = new Topic[(annotation.length-1)];
            for(int i=0; i<annotation.length; i++){
            	String [] tmp = annotation[i].split(" ", 2);
            	t[i] = new Topic(tmp[1],Float.valueOf(tmp[0]));
            }
                        
            hm.put(key, t);
        }
		return hm;
	}
	
	private static HashMap<String,Set> annotationForUser(String temp, HashMap<String,Topic[]> hm){
		String [] hashTweetsOthertweets;
		String hashtag;
		
		String [] tmp;
		Topic [] topic;
		
/** key: Annotazione , value: insieme degli user da cui si è ricavata (espansione futura: inserire la freq dell'annotazione per user... 	uso di insiemi di coppie) */
		HashMap<String,Set> annotationHashtag = new HashMap<String,Set>();		
		
		temp = temp.replaceAll(" @", "@");  // da cambiare nella nuova versione
		hashTweetsOthertweets = temp.split("@");
		hashtag = hashTweetsOthertweets[0]; //hashtag
		
		for(int i = 1; i<hashTweetsOthertweets.length; i++){ /* scorro i gruppi tweets raggruppati per utenti*/
			tmp = hashTweetsOthertweets[i].split(" "); //tmp[0] == UserID
			for(int k = 1; k<tmp.length;k++){                             /* scorro i tweets di ogni gruppo */
				topic = hm.get(tmp[k]); // array di annotazioni del tweet tmp[k]
				
				for(Topic t: topic){	/* scorro le annotazioni */
					if (annotationHashtag.containsValue(t.an)){
						annotationHashtag.get(t.an).add(tmp[0]); //associo l'userID all'annotazione
					}else{
						Set set = new LinkedHashSet<String>(); //eventualmente per fare analisi più complesse 												//invece che String una coppia String+Frequenza
						set.add(tmp[0]);
						annotationHashtag.put(s, set);
					}
				}
			}
			
		}
				
		return annotationHashtag;
	}
	
	public static void main(String[] args) throws IOException{
		
		BufferedReader inAnnotation = new BufferedReader(new FileReader(args[1]));
		BufferedReader inHashtag = new BufferedReader(new FileReader(args[0]));		
		String output_filename = args[0] + ".annotationHash";
		
		HashMap<String, Topic[]> hm = hashmap_create(inAnnotation);
		HashMap<String,Set> an;
		
		PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(output_filename)));
		String temp, text;
		
		while ((temp = inHashtag.readLine()) != null) {
			an = annotationForUser(temp, hm);
			Set<String> keys = an.keySet();
			text = temp.split(" ",2)[0]; // non molto chiaro... prende l'hashtag
			
			for(String k : keys){
			    Set<String> value = ((Set<String>)an.get(k)); // qui casto... in previsione usare coppie
			    text += "#"+k+' '+value.size();
			    for (String v: value)
			    	text += ' '+v;
			}
			out.println(text);
		}
	}
	
}
