import weka.core.AttributeStats;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.experiment.Stats;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Discretize;
import weka.gui.beans.ScatterPlotMatrix;

public class DM02AdithyaAbrahamPhilip {
	public static void main(String[] args) {
		String filename = "bank-data.csv";

		try {

			DataSource source = new DataSource(filename);

			Instances instances = source.getDataSet();

			// Delete the ID attribute
			instances.deleteAttributeAt(0);

			// deletion changes the column indices
			final int INDEX_AGE = 0;
			final int INDEX_INCOME = 3;

			// print min, max, mean, std. dev. for age and income
			printStats(instances.attributeStats(INDEX_AGE), "Age");
			printStats(instances.attributeStats(INDEX_INCOME), "Income");

			// print covariance and correlation coefficient
			printCovCorr(instances, INDEX_AGE, INDEX_INCOME);

			// discretize income into 4 bins and print their frequencies
			discretizeAndPrint(instances, INDEX_INCOME, 4);			

			// display a scatter plot of age and income
			
			// first remove all other attributes
			for (int i = instances.numAttributes() - 1; i>=0;i--) {
				if (i!= INDEX_AGE && i != INDEX_INCOME) instances.deleteAttributeAt(i);
			}
			// show scatter plot
			showScatterPlot(instances);

		} catch (Exception e) {
			e.printStackTrace();

		}
	}

	/**
	 * prints an ASCII table for given name and AttributeStats
	 * 
	 * @param attrStats
	 *            AttributeStats for attribute to display, obtained from
	 *            instances.attributeStats(int)
	 * @param name
	 *            name of attribute for which stats are being printed
	 */
	public static void printStats(AttributeStats attrStats, String name) {
		System.out.println("Stats for " + name + ":");
		Stats stats = attrStats.numericStats;
		ASCIITable.getInstance().printTable(
				new String[] { "Min", "Max", "Mean", "Std. Dev." }, // headers
				new String[][] { { "" + stats.min, "" + stats.max,
						"" + stats.mean, "" + stats.stdDev } });
	}

	public static void printCovCorr(Instances instances, int first_index,
			int second_index) {

		double sum1_1 = 0; // normal sum
		double sum2_1 = 0;
		double sum1_2 = 0; // sum of squares
		double sum2_2 = 0;
		double sum_prod = 0; // sum of products
		int n = instances.numInstances();

		for (int i = 0; i < n; i++) {
			double a1 = instances.instance(i).value(first_index);
			double a2 = instances.instance(i).value(second_index);
			sum1_1 += a1;
			sum2_1 += a2;
			sum1_2 += a1 * a1;
			sum2_2 += a2 * a2;
			sum_prod += a1 * a2;
		}

		double mean1 = sum1_1 / n; // average of first attribute
		double mean2 = sum2_1 / n; // average of second attribute
		double mean_prod = sum_prod / n; // average of sum of products
		double stdDev_1 = Math.sqrt((sum1_2 - n * Math.pow(mean1, 2)) / n);
		double stdDev_2 = Math.sqrt((sum2_2 - n * Math.pow(mean2, 2)) / n);

		// calculate covariance
		final double cov = mean_prod - mean1 * mean2;
		// calculate coefficient of correlation
		final double corCo = cov / (stdDev_1 * stdDev_2);

		System.out.println(instances.attribute(first_index).name() + " and "
				+ instances.attribute(second_index).name() + " comparison:");
                ASCIITable.getInstance().printTable(
				new String[] { "Covariance", "Correlation Coeff." }, // headers
				new String[][] { { "" + cov, "" + corCo } });

	}

	public static void discretizeAndPrint(Instances instances, int index,
			int bins) throws Exception {
		System.out.println("Discretization of "
				+ instances.attribute(index).name() + " into in " + bins
				+ " bins:");

		// create a new discretization filter
		Discretize discretize = new Discretize();

		// filters are expected to accept user input, hence indices are 1-based
		// instead of 0-based
		// compensate by adding 1
		discretize.setAttributeIndices(index + 1 + "");

		// Set number of bins
		discretize.setBins(bins);

		discretize.setInputFormat(instances);

		// discretize
		Instances output = Filter.useFilter(instances, discretize);
		// get frequencies of bins
		int freqs[] = output.attributeStats(index).nominalCounts;
		// get cut points of discretization
		double[] cutPoints = discretize.getCutPoints(index);

		// print out bin ranges with frequencies

		System.out.print("(-inf, ");
		for (int i = 0; i < cutPoints.length; i++) {
			double p = cutPoints[i];
			System.out.println(p + "]");
			System.out.println(" Frequency: " + freqs[i]);
			System.out.print("(" + p + ", ");
		}
		System.out.println("inf)");
		System.out.println(" Frequency: " + freqs[freqs.length - 1]);
	}

	public static void showScatterPlot(Instances instances) throws Exception {
		final javax.swing.JFrame jf = new javax.swing.JFrame();
		jf.getContentPane().setLayout(new java.awt.BorderLayout());
		final ScatterPlotMatrix as = new ScatterPlotMatrix();
		as.setInstances(instances);

		jf.getContentPane().add(as, java.awt.BorderLayout.CENTER);
		jf.addWindowListener(new java.awt.event.WindowAdapter() {
			public void windowClosing(java.awt.event.WindowEvent e) {
				jf.dispose();
				System.exit(0);
			}
		});
		jf.setSize(800, 600);
		jf.setVisible(true);
	}
}
