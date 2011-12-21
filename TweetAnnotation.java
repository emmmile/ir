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

public class TweetAnnotation {
	// Just remove the initial numbering to obtain the real text
	public static String get_text(String input) {
		return input.replaceFirst("\\d+\\s+\\d+\\s+", "");
	}

	public static void main(String[] args)throws Exception{
		String lang="it";
		ConfigManager.init("/home/ir2011/ir.tms.xml");  
		// RelatednessCache r = new RelatednessCache(lang);
		Annotator annotator = new Annotator(lang);
		ArticleSearcher as = new ArticleSearcher(lang);  

		String filename = args[0];
		String output_filename = args[0]+".annotation";

		String str;
		String real_text;
		String annot_output;

		int counter = 0;
		List<Annotation> annots;

		try {
		    BufferedReader in = new BufferedReader(new FileReader(filename));
		    PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(output_filename)));

		    while ((str = in.readLine()) != null) {
		        real_text = get_text(str);
			//System.out.println( real_text );
		        annot_output = str.replace( real_text, "" );
		        //System.out.println( annot_output );
			//boolean toPrint = false;

		        // annots = annotator.annotates(real_text, r);
		        annots = annotator.annotates(real_text);
		        for(Annotation a:annots){
		            if (a.getSense() != -2) {//Not disambiguated
		            	if (a.getRho() >= 0.2) {
		            		//toPrint = true;
		            		// stampo soltanto un intero che rappresenta il token e la sua "affidabilita'"
		            		// penso che cosi' dopo sia piu' facile da gestire / ordinare
		              		//annot_output += " # " + a.getRho() + " " + a.getSense();//+ as.getTitleByDoc(a.getSense());
		            		annot_output += "#" + a.getSense() + "@" + a.getRho();
				}
		            }
		        }
		        
		        // stampo solo i tweet che sono stati annotati
		        //if ( toPrint )
		        out.println(annot_output);
		        
		        if( ++counter % 5000 == 0) {
		            System.out.println(counter);
		        }
		    }

		    in.close();
		    out.close();

		} catch (IOException e) {
		    System.out.println(e);
		}
	}
}
