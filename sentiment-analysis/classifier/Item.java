package classifier;

import java.util.HashMap;
import java.util.Map;

/**
 * class representing a tweet in weighted majority algorithm
 */
public class Item {
	
	private String _text;
	private String _polarity;
	private String _target;
	private Map<Integer,String> _cl2pol;
	
	/**
	 * @param text the tweet's text
	 */
	public Item(String text) {
		this._text = text;
		_cl2pol = new HashMap<Integer, String>();
	}
	
	/**
	 * gets the tweet's text 
	 * @return the tweet's text
	 */
	public String getText() {
		return _text;
	}
	
	/**
	 * sets a given text
	 * @param text the tweet's text
	 */
	public void setText(String text) {
		this._text = text;
	}
	
	/**
	 * gets the tweet's polarity
	 * @return the tweet's polarity
	 */
	public String getPolarity() {
		return _polarity;
	}
	
	/**
	 * sets the tweet's polarity
	 * @param polarity the tweet's polarity
	 */
	public void setPolarity(String polarity) {
		this._polarity = polarity;
	}
	
	/**
	 * gets a map that associates classifiers' id to polarities
	 * @return a map that associates classifiers' id to polarities
	 */
	public Map<Integer, String> getCl2pol() {
		return _cl2pol;
	}
	
	/**
	 * sets a given map
	 * @param cl2pol a map that associates classifiers' id to polarities
	 */
	public void setCl2pol(Map<Integer, String> cl2pol) {
		this._cl2pol = cl2pol;
	}
	
	/**
	 * gets the tweet's target polarity
	 * @return tweet's target polarity
	 */
	public String getTarget() {
		return _target;
	}
	
	/**
	 * sets a given target polarity
	 * @param target the tweet's target polarity
	 */
	public void setTarget(String target) {
		this._target = target;
	}
	
	
}
