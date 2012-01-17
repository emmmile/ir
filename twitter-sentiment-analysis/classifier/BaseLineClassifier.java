package classifier;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.LinkedList;
import java.util.List;
import java.util.StringTokenizer;

/**
 * a classifier that only counts positive and negative terms from given lists
 */
public class BaseLineClassifier implements IClassifier {
	
	private class Polarity{
		public List<String> result; 
		public List<Double> pos;
		public List<Double> neg;
		
		Polarity(List<String> r, List<Double> p, List<Double> n){
			this.result = r;
			this.pos = p;
			this.neg = n;
		}
		
	}
	
	/**
	 * evaluates the classifier
	 */
	@Override
	public void evaluate() throws Exception {
		int giuste = 0, sbagliate = 0;
		FileInputStream fstream = new FileInputStream("files/test_base.txt");
        DataInputStream in = new DataInputStream(fstream);
        BufferedReader br = new BufferedReader(new InputStreamReader(in));
		List<String> res_pos = new LinkedList<String>();
		List<String> res_neg = new LinkedList<String>();
		//res_pos = extractFeatures("files/pos.txt");
		//res_neg = extractFeatures("files/neg.txt");
		Polarity p = extractFeatures("files/pol.csv"); //aggiunta **
		int pos = 0;
		int neg = 0;
		String strLine, pol;
		int i = 0;
		while((strLine = br.readLine()) != null) {
			String[] items = strLine.split(";;");
    		pol = items[0];
    		StringTokenizer st = new StringTokenizer(items[5].toLowerCase()," .,?!}{_");
    		while(st.hasMoreTokens()) {
    			String s = st.nextToken();
    			
    			
    			for (int k = 0; k<p.result.size(); k++) { // ciclo aggiunto **
    				if(p.result.contains(s)){
    					pos += p.pos.get(k);
    					neg += p.neg.get(k);
    					}
    			}
    			
    			/**if(res_pos.contains(s))
					pos++;
				else if(res_neg.contains(s))
					neg++;**/
    		}
			i++;
			if(pos>=neg && pol.equals("4") || pos<neg && pol.equals("0")) 
				giuste++;
			else
				sbagliate++;
			pos = 0;
			neg = 0;
		}
		System.out.println(giuste);
		System.out.println(sbagliate);
	}

	/**
	 * no action
	 */
	@Override
	public void train() throws Exception {
		// TODO Auto-generated method stub
	}

	/**
	 * classifies a tweet
	 * @param stringa a string to classify
	 * @return the tweet's polarity
	 */
	@Override
	public String classify(String stringa) {
		//List<String> res_pos = new LinkedList<String>();
		//List<String> res_neg = new LinkedList<String>();
		//res_pos = extractFeatures("files/pos.txt");
		//res_neg = extractFeatures("files/neg.txt");
		Polarity p = extractFeatures("files/pol.csv"); //aggiunta **
		int pos = 0;
		int neg = 0;
		String data = stringa;
		System.out.print(stringa);
		////String[] items = data.split(" "); ????? ma che controlla una parola alla volta???
	
		/*for (String string : res_pos) {
			if(data.contains(string))
				pos++;
		}
		for (String string : res_neg) {
			if(data.contains(string))
				neg++;
		}
		*/
		
		for (int i = 0; i<p.result.size(); i++) { // ciclo aggiunto **
			String s = p.result.get(i);
			if(data.contains(s)){
				pos += p.pos.get(i);
				neg += p.neg.get(i);
				}
		}
		
		if(pos>=neg) //QUI POTREMMO USARE I VALORI CALCOLATI
			return "4";
		else
			return "0";
		
	}
	
	/**
	 * creates a list of terms from an input file
	 * @param path path of file from which terms can be extracted
	 * @return a list of terms
	 */
	public Polarity extractFeatures(String path) {
		List<String> result = new LinkedList<String>();
		List<Double> pos = new LinkedList<Double>(); // aggiunta **
		List<Double> neg = new LinkedList<Double>(); // aggiunta **
		Polarity pol = null;
		
		try{
            FileInputStream fstream = new FileInputStream(path);
            DataInputStream in = new DataInputStream(fstream);
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            String strLine;
            while ((strLine = br.readLine()) != null) {
            	String[] token = strLine.split("\t");
                result.add(token[0]);
                pos.add(Double.valueOf(token[1]));
                neg.add(Double.valueOf(token[2]));
            }
            pol = new Polarity(result,pos,neg);
            in.close();
        }catch (Exception e){
            System.err.println("Errore: " + e.getMessage());
        }
        return pol;
    }
}
