
import it.unipi.di.tms.config.ConfigManager;
import it.unipi.di.tms.preprocessor.wiki.articles.ArticleSearcher;
import it.unipi.di.tms.preprocessor.wiki.anchors.Anchor;
//import it.unipi.di.tms.preprocessor.wiki.anchors.AnchorSearcher;

public class AnchorSearcher {
	public static void main(String[] args)throws Exception{
		String lang="it";
		ConfigManager.init("/home/ir2011/ir.tms.xml");

		ArticleSearcher as = new ArticleSearcher(lang);
		System.out.println( as.getTitleByDoc( Integer.valueOf( args[0] ) ) );
	}

}
