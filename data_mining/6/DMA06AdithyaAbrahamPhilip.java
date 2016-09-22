import java.io.File;
import java.util.Scanner;

import weka.classifiers.Classifier;
import weka.classifiers.trees.BFTree;
import weka.classifiers.trees.J48;
import weka.core.Attribute;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.instance.Resample;

public class DMA06AdithyaAbrahamPhilip {
	public static void main(String[] args) throws Exception {
		if(args.length == 0) {
			System.err.println("Path to config file needs to be first argument.");
			System.exit(1);
		}
		
		final int seed = 201;
		
		// read in config file - first argument
		Scanner sc = new Scanner(new File(args[0]));
		
		sc.nextLine(); // discard comment in config file
		
		final String DATA_PATH = sc.nextLine();		
		final int sampleSize = Integer.parseInt(sc.nextLine());
		final String className = sc.nextLine();

		sc.close();
		// finished reading config file
		
		DataSource source = new DataSource(DATA_PATH);
		Instances orig  = source.getDataSet();
		orig.setClass(orig.attribute(className));
		
		Instances[] split = getTrainingAndTestSets(orig, seed, sampleSize);
		Instances trainingSet = split[0];
		Instances testSet = split[1];
		
		// just a test, can be removed before production
		for(int i = 0; i<trainingSet.numInstances(); i++) {
			for(int j = 0;j <testSet.numInstances(); j++) {
				if(testSet.instance(j).value(3) == trainingSet.instance(i).value(3)) {
					throw new AssertionError("Testing and training set have duplicated elements!");
				}
			}
		}
		
		J48 c45Classifier = new J48();
		c45Classifier.buildClassifier(trainingSet);
		
		BFTree giniClassifier = new BFTree();
		giniClassifier.buildClassifier(trainingSet);
		
		System.out.println("C4.5 Decision Tree");
		System.out.println("-----------------------");
		System.out.println(c45Classifier);
		System.out.println("Gini Decision Tree");
		System.out.println("-----------------------");
		System.out.println(giniClassifier);
		System.out.println();
		System.out.println("Prediction Results:");

		classifyAndPrint(testSet, className, new String[] {"Actual", "Predicted by C45", "Predicted by Gini"}, c45Classifier, giniClassifier);
	}
	
	/**
	 * classifies every instance based on passed classifier array and creates a table with supplied headings 
	 * and a column for the actual class of the instance, followed by a column for each classifier's result,
	 * in the order in which they were passed in the array
	 */
	private static void classifyAndPrint(Instances testSet, String className, 
			String[] headings, Classifier... classifier) throws Exception {	
		
		String[][] rows = new String[testSet.numInstances()][1 + classifier.length];
		for(int i = 0; i<testSet.numInstances(); i++) {
			Instance instance = testSet.instance(i);
			Attribute classAttr = testSet.attribute(className);
			rows[i][0] = instance.stringValue(classAttr);
			int classifierStartIndex = 1;
			for(int j = 0; j < classifier.length; j++) {
				rows[i][classifierStartIndex+j] = classAttr.value((int)classifier[j].classifyInstance(instance));
			}
		}
		ASCIITable.getInstance().printTable(
				headings, // headers
				rows
				);
	}
	
	/**
	 * index 0 - training set
	 * index 1 - test set
	 */
	private static Instances[] getTrainingAndTestSets(Instances orig, int seed, int sampleSize)
			throws Exception {
		// get training set
		Instances trainingSet = Filter.useFilter(orig, getResampleForTraining(orig, seed, sampleSize));
		// get test set
		Resample sample = getResampleForTraining(orig, seed, sampleSize);
		sample.setInvertSelection(true); // to get what was left out earlier
		Instances testSet = Filter.useFilter(orig, sample);
		
		return new Instances[]{trainingSet, testSet};
	}
	
	/**
	 * @return the Resample filter that can be used to get the training set
	 * @throws Exception
	 */
	private static Resample getResampleForTraining(Instances orig, int seed, int sampleSize) throws Exception {
		Resample sample = new Resample();
		sample.setNoReplacement(true);
		sample.setInputFormat(orig);
		sample.setRandomSeed(seed);
		sample.setSampleSizePercent(sampleSize/(double)orig.numInstances()*100);
		
		return sample;
	}
}
