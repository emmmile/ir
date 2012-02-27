
import it.unipi.di.tms.config.ConfigManager;
import it.unipi.di.tms.semantic.Annotator;
import it.unipi.di.tms.semantic.RelatednessCache;
import it.unipi.di.tms.semantic.Annotation;
import it.unipi.di.tms.semantic.Similarity;
import it.unipi.di.tms.preprocessor.wiki.articles.ArticleSearcher;
import it.unipi.di.tms.preprocessor.wiki.anchors.Anchor;
import it.unipi.di.tms.preprocessor.wiki.anchors.AnchorSearcher;

import java.util.List;
import java.io.*;

public class AnnotateText {


	public static void main(String[] args)throws Exception{
		String lang="it";
		ConfigManager.init("/home/ir2011/ir.tms.xml");  
		Annotator annotator = new Annotator(lang);
		ArticleSearcher as = new ArticleSearcher(lang);
		
		//AnchorSearcher anchorSearcher = new AnchorSearcher("it");
		//Anchor an = anchorSearcher.searchAnchor( args[0] ); 

		/*for( int wid : an.getSortedPages() ){   //getSortedPage restituisce tutti gli id degli articoli linkati da quell'ancora
			System.out.println( as.getTitleByDoc(wid) );     
			String command = "/bin/bash -c \"grep \\\"^" + as.getTitleByDoc(wid) + "\\\" data/allusers/allusers.topics";
			command += " | sed 's/" + as.getTitleByDoc(wid) + " //' | sed 's/ #/\\n#/g'\"";  
			System.out.println( command );     
			
			try {
				Process proc = Runtime.getRuntime().exec( command );
				BufferedReader read = new BufferedReader(new InputStreamReader(proc.getInputStream()));
				try {
					proc.waitFor();
				} catch(InterruptedException e) {
					System.out.println(e.getMessage());
				}
			
				while(read.ready()) {
					System.out.println(read.readLine());
				}
        		} catch(IOException e) {
				System.out.println(e.getMessage());
			}
		}*/
		PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(args[0])));
		
		List<Annotation> annots;
		annots = annotator.annotates( args[1] );
		for(Annotation a:annots){
			if (a.getSense() != -2) {//Not disambiguated
				//if (a.getRho() >= 0.05) {
					out.println( as.getTitleByDoc(a.getSense()) ); //+ " " + a.getRho() );
				//}
			}
		}
		
		out.close();
	}
	
}

