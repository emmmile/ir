package main;


import java.util.LinkedList;
import java.util.List;

import commands.CalculateWmPrecisionCommand;
import commands.ConstructCommand;
import commands.ConstructWmCommand;
import commands.PrepareTrainCommand;

import classifier.ClassifierBuilder;
import classifier.IClassifier;
import classifier.Invoker;
import classifier.Item;
import classifier.WeightedMajority;
import classifier.WekaClassifier;
import util.Options;
import weka.classifiers.Classifier;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.functions.MultilayerPerceptron;
import weka.classifiers.functions.VotedPerceptron;
import weka.classifiers.trees.J48;
import wlsvm.WLSVM;

public class Main {
	
	public static void main(String[] args) throws Exception {
	    
		//costruzione classificatori
		/*ClassifierBuilder clb = new ClassifierBuilder();
		Options opt = new Options();
		clb.setOpt(opt);
		opt.setSelectedFeaturesByFrequency(true);
		opt.setNumFeatures(150);
		opt.setRemoveEmoticons(true);
		clb.prepareTrain();
		clb.prepareTest();
		NaiveBayes nb = new NaiveBayes();
		WekaClassifier wc = clb.constructClassifier(nb);
		wc.classify("i am very sad");*/
		

		//uso classificatori già costruiti
		/*List<IClassifier> classifiers = new LinkedList<IClassifier>();
		ClassifierBuilder cb = new ClassifierBuilder();
		WekaClassifier wc1 = cb.retrieveClassifier("weka.classifiers.bayes.NaiveBayes");
		WekaClassifier wc2 = cb.retrieveClassifier("weka.classifiers.trees.J48");
		WekaClassifier wc3 = cb.retrieveClassifier("weka.classifiers.functions.VotedPerceptron");
		classifiers.add(wc1);
		classifiers.add(wc2);
		classifiers.add(wc3);
		WeightedMajority wm  = new WeightedMajority(classifiers);
		Item item = wm.weightedClassify("i am very sad");
		item.setTarget("4");
		wm.setTarget(item);
		System.out.println(wm.get_cl2weight().get(1) + " " + wm.get_cl2weight().get(2) + " " + wm.get_cl2weight().get(3));*/
		
		Options opt = new Options();
		ClassifierBuilder clb = new ClassifierBuilder();
		PrepareTrainCommand ptc = new PrepareTrainCommand(clb);
		ConstructCommand cc = new ConstructCommand(clb);
		ConstructWmCommand cwmc = new ConstructWmCommand(clb);
		CalculateWmPrecisionCommand calcPrec = new CalculateWmPrecisionCommand(clb);
		clb.setOpt(opt);
		Invoker inv = new Invoker(ptc, cc, cwmc, calcPrec);

		
		if(args[0].equals("prepareTrain")) {
			if(args.length>1 && (args[1].equals("-sf") || args[1].equals("-re")))
				opt.setSelectedFeaturesByFrequency(true);
			if(args.length>2 && (args[2].equals("-re") || args[2].equals("-sf")))
				opt.setRemoveEmoticons(true);
			inv.prepareTrain();
		} else if(args[0].equals("construct")) {
			opt.setClassifierName(args[1]);
			if(args.length>2)
				opt.setNumFeatures(Integer.parseInt(args[2]));
			inv.construct();
		} else if(args[0].equals("weightedMajority")) {
			int i = 1;
			opt.setWmClassifiersName(new LinkedList<String>());
			while(i < args.length) {
				opt.getWmClassifiersName().add(args[i]);
				i++;
			}
			inv.constructWm();
		} else if (args[0].equals("evaluateWm")) {
			int i = 1;
			opt.setWmClassifiersName(new LinkedList<String>());
			while(i < args.length) {
				opt.getWmClassifiersName().add(args[i]);
				i++;
			}
			inv.calculateWmPrecision();
		}
	}
}
