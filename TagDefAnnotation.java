//prende un file .text e restituisce un file .annotation con TweetID + Annotation (file.java di pau modificato)

import it.unipi.di.tms.config.ConfigManager;
import it.unipi.di.tms.semantic.Annotator;
import it.unipi.di.tms.semantic.RelatednessCache;
import it.unipi.di.tms.semantic.Annotation;
import it.unipi.di.tms.semantic.Similarity;
import it.unipi.di.tms.preprocessor.wiki.articles.ArticleSearcher;

import java.util.List;

import java.io.BufferedReader;
import java.io.FileReader;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.PrintWriter;

import java.io.IOException;

public class TagDefAnnotation {

    // Get the tweet_id and the date
    public static String[] def_string(String input) {
    	String temp = input.replaceAll(".}", "}");
        return temp.split("}");
    }

    // Get the text
    public static String get_text(String input) {
        return input.replaceFirst("\\d+ \\d+ ", "");
    }

	public static void main(String[] args)throws Exception{
		String lang="en";
		ConfigManager.init("/home/ir2011/ir.tms.xml");  
		Annotator annotator = new Annotator(lang);
		ArticleSearcher as = new ArticleSearcher(lang);  

		String filename = args[0];
		String output_filename = args[0] + ".annotation";

        String str;
        String[] definitions;
        String text;

        int counter = 1;

		List<Annotation> annots;

        try {
            BufferedReader in = new BufferedReader(new FileReader(filename));
            PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(output_filename)));
 
            while ((str = in.readLine()) != null) {
                definitions = def_string(str);
                //text = get_text(str); inutile

                String hashtag = definitions[0].replaceAll(" ", "");
                String def = "";
                for(int i=1; i<definitions.length;i++){
	                annots = annotator.annotates(definitions[i]);
	                for(Annotation a:annots){
	                    if (a.getSense() != -2) { //Not disambiguated
	                    	if (a.getRho() >= 0.2)
	                    		def += "#" + as.getTitleByDoc(a.getSense())+ "^" + a.getRho() ;
	                    }
	                }
                }
                if(def.compareTo("")!=0){
                	out.println(hashtag + " " + def);
                	System.out.println(hashtag);
                }
                // Counter to have a feeling of progress
                if(counter % 50000 == 0) {
                    System.out.println(counter);
                }
                counter += 1;
            }

            in.close();
            out.close();

        } catch (IOException e) {
            System.out.println(e);
        }

	}

}