import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Discretize;

public class DMA03AdithyaAbrahamPhilip {
	public static void main(String[] args) {
		String filename = "bank-data.csv";

		try {

			DataSource source = new DataSource(filename);

			Instances instances = source.getDataSet();
			
			// PART 1

			Set<Integer> notDel = new HashSet<>();
			// don't delete age, sec, region, income
			notDel.addAll(Arrays.asList(new Integer[]{1,2,3,4}));
			
			// delete in reverse so as to not affect indices
			for(int i = instances.numAttributes() - 1;i>=0;i--) {
				if (!notDel.contains(i)) {
					instances.deleteAttributeAt(i);
				}
			}

			// deletion changes the column indices
			final int INDEX_AGE = 0;
			final int INDEX_SEX = 1;
			final int INDEX_REGION = 2;
			final int INDEX_INCOME = 3;
			
			final int NUM_AGE_BINS = 3;
			String[] binLabels = {"YOUNG", "MIDDLE", "OLD"};
			
			// discretize age into 3 bins
			
			instances = discretizeAndRename(instances, INDEX_AGE, NUM_AGE_BINS, binLabels);
			
			// PART 2	
			
			// accept user input 
			if(args.length == 0) {
				System.out.println("Need to pass n as command line argument!");
				return;
			}
			
			int n = Integer.parseInt(args[0]);
			
			System.out.println("Cube Size: " + n);
			System.out.println();
			// for each n-combination of dimensions (age, sex, region) print count and avg. income
			
			for(ArrayList<Integer> comb: getCombinations(new int[]{INDEX_AGE, INDEX_SEX, INDEX_REGION}, n, 0)) {
				String[][] rows = getCubeCellsAsRows(instances, comb, INDEX_INCOME);
				
				ASCIITable.getInstance().printTable(
						new ASCIITableHeader[] { 
								new ASCIITableHeader("Attr. Values", ASCIITable.ALIGN_LEFT),
								new ASCIITableHeader("Count", ASCIITable.ALIGN_LEFT),
								new ASCIITableHeader("Avg. Income", ASCIITable.ALIGN_LEFT)}, // headers
						rows
						);
			}

		} catch (Exception e) {
			e.printStackTrace();

		}
	}
	
	private static String[][] getCubeCellsAsRows(Instances instances, ArrayList<Integer> comb, 
			int fact_index) {
		Integer[] combArr = comb.toArray(new Integer[comb.size()]);

		System.out.println("Selected Attributes: " + getAttributeNames(instances, combArr));
		
		HashMap<Tuple, double[]> cube = getDataCube(instances, fact_index, combArr);
		String[][] rows = new String[cube.keySet().size()][];
		ArrayList<Tuple> sortedKeys = new ArrayList<>();
		sortedKeys.addAll(cube.keySet());
		Collections.sort(sortedKeys);
		int ctr = 0;
		for(Tuple t: sortedKeys) {
			rows[ctr++] = new String[]{"" + t, String.format("%.0f", cube.get(t)[0]),
					String.format("%.2f", cube.get(t)[1]/cube.get(t)[0])};
		}		
		
		return rows;		
	}
	
	/**
	 * Discretizes a given attribute into specified number of bins and applies it on instances
	 * @param instances instances whose values are to be discretized
	 * @param index index of attribute to be discretized
	 * @param numBins number of bins to discretize into
	 * @param binLabels names to be given to each bin in increasing order of cut points
	 * @return instances on which the discretization and renaming has been applied
	 * @throws Exception
	 */
	private static Instances discretizeAndRename(Instances instances, int index, int numBins, String[] binLabels) 
			throws Exception {
		// filters are expected to accept user input, hence indices are 1-based
		// instead of 0-based
		// compensate by adding 1
		Discretize discretize = new Discretize(1 + index + "");
		discretize.setBins(numBins);
		discretize.setInputFormat(instances);
		
		instances = Filter.useFilter(instances, discretize);
		for(int i =0;i<numBins; i++) {
			instances.renameAttributeValue(index, i, binLabels[i]);
		}
		
		return instances;
	}
	
	private static List<String> getAttributeNames(Instances instances, Integer... indices) {
		ArrayList<String> names = new ArrayList<>();
		for(int i = 0;i<indices.length;i++) {
			names.add(instances.attribute(indices[i]).name());
		}
		return names;
	}
	
	public static ArrayList<ArrayList<Integer>> getCombinations(int indices[], int n, int start) {
		ArrayList<ArrayList<Integer>> choices = new ArrayList<>();
		if (n==0) {
			choices.add(new ArrayList<Integer>());
			return choices;
		}
		for(int i = start;i<indices.length - n + 1;i++) {
			for(ArrayList<Integer> choice: getCombinations(indices, n-1, i+1)) {
				choice.add(0, indices[i]);
				choices.add(choice);
			}
		}
		return choices;
	}
	
	/**
	 * 
	 * @param instances
	 * @param factIndex must be numeric
	 * @param dimensionIndices
	 * @return
	 */
	public static HashMap<Tuple, double[]> getDataCube(
			Instances instances, int factIndex, Integer... dimensionIndices) {
		
		HashMap<Tuple, double[]> map = new HashMap<>();
		
		for(int i = 0; i<instances.numInstances(); i++) {
			Instance row = instances.instance(i);
			
			ArrayList<Object> selectedAttrs = new ArrayList<>();
			for(int index: dimensionIndices) {
				if (row.attribute(index).isNumeric()) {
					selectedAttrs.add(row.value(index));		
				} else {
					selectedAttrs.add(row.stringValue(index));		
				}
			}
			
			Tuple t = new Tuple(selectedAttrs.toArray(new Comparable[0]));
			if (!map.containsKey(t)) {
				map.put(t, new double[]{1, row.value(factIndex)});
			} else {
				double arr[] = map.get(t);
				arr[0]++;
				arr[1]+=row.value(factIndex);
			}
		}
		
		return map;
	}
	
	private static class Tuple implements Comparable<Tuple> {
		private Comparable mO[];
		public Tuple(Comparable... o) {
			mO = o;
		}
		
		@Override
		public int hashCode() {
			int sum = 0;
			for(int i = 0; i < mO.length; i++) {
				sum+=mO[i].hashCode();
			}
			return sum;
		}
		
		@Override
		public boolean equals(Object obj) {
			if (!(obj instanceof Tuple)) return false;
			Tuple other = (Tuple) obj;
			if (other.mO.length != mO.length) return false;
			for(int i = 0; i<mO.length; i++) {
				if (!mO[i].equals(other.mO[i])) return false;
			}
			return true;
		}
		
		@Override
		public String toString() {
			if (mO.length == 0) return "All";
			return Arrays.asList(mO).toString();
		}

		/**
		 * lexicographic comparison
		 */
		@Override
		public int compareTo(Tuple o) {
			if (o.mO.length < mO.length) return 1;
			else if (o.mO.length > mO.length) return -1;
			for(int i = 0; i <mO.length; i++) {
				int comp = mO[i].compareTo(o.mO[i]);
				if (comp != 0) {
					return comp;
				}
			}
			return 0;
		}
	}
}
