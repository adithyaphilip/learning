import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.Scanner;
import java.util.function.Predicate;

import weka.associations.Apriori;
import weka.associations.FPGrowth;
import weka.associations.FPGrowth.AssociationRule;
import weka.associations.FPGrowth.BinaryItem;
import weka.core.Attribute;
import weka.core.Instances;
import weka.core.SelectedTag;
import weka.core.converters.ConverterUtils.DataSource;

public class DMA05AdithyaAbrahamPhilip {
	public static void main(String[] args) throws Exception {
		if(args.length == 0) {
			System.err.println("Path to config file needs to be first argument.");
			System.exit(1);
		}
		// read in config file - first argument
		Scanner sc = new Scanner(new File(args[0]));
		
		sc.nextLine(); // discard comment in config file
		
		final String DATA_PATH = sc.nextLine();
		
		final String[] delIndStr = sc.nextLine().split(":");
		
		final String[] reqAttrsStr = sc.nextLine().split(":");
		
		final double MIN_LIFT = Double.parseDouble(sc.nextLine()); 	
		final double MIN_SUPPORT = Double.parseDouble(sc.nextLine());
		
		// finished reading config file
		sc.close();
		
		DataSource source = new DataSource(DATA_PATH);
		Instances instances = source.getDataSet();
		
		for(int i = 0;i<delIndStr.length;i++) {
			instances.deleteAttributeAt(instances.attribute(delIndStr[i]).index());
		}
		
		List<AssociationRule> filtered = getFpGrowthResult(instances, MIN_LIFT, MIN_SUPPORT, 
				reqAttrsStr);
		
		printOutput(filtered);
	}
	
	public static List<AssociationRule> getFpGrowthResult(
			Instances instances, double minLift, double minSupport, String[] reqAttrsStr) 
					throws Exception {
		
		FPGrowth fpGrowth = new FPGrowth();
		// set metric type to lift
		fpGrowth.setMetricType(new SelectedTag(1, Apriori.TAGS_SELECTION));
		fpGrowth.setMinMetric(minLift);
		fpGrowth.setLowerBoundMinSupport(minSupport);
		// this does not guarantee LHS, only that the attributes are either in LHS or RHS
		// this is why we still need to filter the result
		fpGrowth.setRulesMustContain(String.join(":", reqAttrsStr));
		
		// perform FPGrowth algorithm
		fpGrowth.buildAssociations(instances);		

		final ArrayList<Attribute> reqAttrs = new ArrayList<>(reqAttrsStr.length);
		for(int i = 0;i<reqAttrsStr.length;i++) {
			// 0 because it means present
			reqAttrs.add(instances.attribute(reqAttrsStr[i]));
		}
		
		List<AssociationRule> rules = fpGrowth.getAssociationRules();
		rules.removeIf(new Predicate<AssociationRule>() {
			@Override
			public boolean test(AssociationRule t) {
				int matches = 0;
				for(Iterator<BinaryItem> i = t.getPremise().iterator(); i.hasNext();) {
					for(Attribute a: reqAttrs) {
						if(i.next().getAttribute().equals(a)) {
							matches++;						
						}
					}			
				}
				return matches != reqAttrs.size();
			}
		});
		return rules;
	}
	
	public static void printOutput(List<AssociationRule> rules) {
		final int INDEX_PREMISE = 0;
		final int INDEX_CONSEQUENCE = 1;
		final int INDEX_TOT_SUP = 2;
		final int INDEX_LIFT = 3;
		final int INDEX_CONFIDENCE = 4;
		
		String[][] rows = new String[rules.size()][5];
		for(int i = 0; i<rules.size(); i++) {
			AssociationRule rule = rules.get(i);
			rows[i][INDEX_PREMISE] = rule.getPremise().toString();
			rows[i][INDEX_CONSEQUENCE] = rule.getConsequence().toString();
			rows[i][INDEX_TOT_SUP] = rule.getTotalSupport() + "";
			rows[i][INDEX_LIFT] = String.format("%.4f", rules.get(i).getMetricValue());
			rows[i][INDEX_CONFIDENCE] = String.format("%.4f", rule.getTotalSupport()/(double)rule.getPremiseSupport());
		}
		Arrays.sort(rows, new Comparator<String[]>() {

			@Override
			public int compare(String[] o1, String[] o2) {
				return Double.parseDouble(o2[INDEX_CONFIDENCE]) - Double.parseDouble(o1[INDEX_CONFIDENCE]) > 0 ? 1 : -1;
			}
		});
		if (rows.length == 0) {
			System.out.println("No valid rules found!");
			return;
		}
		ASCIITable.getInstance().printTable(
				new ASCIITableHeader[] { 
						new ASCIITableHeader("Premise", ASCIITable.ALIGN_LEFT),
						new ASCIITableHeader("Consequence", ASCIITable.ALIGN_LEFT),
						new ASCIITableHeader("Tot. Support", ASCIITable.ALIGN_LEFT),
						new ASCIITableHeader("Lift", ASCIITable.ALIGN_LEFT),
						new ASCIITableHeader("Confidence", ASCIITable.ALIGN_LEFT)}, // headers
				rows
				);
	}
	
	interface Validator {
		boolean isValid(AssociationRule rule);
	}
}
