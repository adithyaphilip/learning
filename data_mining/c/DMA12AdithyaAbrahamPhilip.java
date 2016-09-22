import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.InterquartileRange;

import java.io.File;
import java.util.*;

public class DMA12AdithyaAbrahamPhilip {

    static double[][] mQs;

    public static void main(String[] args) {
        try {
            if(args.length == 0) {
                System.out.println("Usage: At least one input file must be specified on the command line");
                System.exit(1);
            }
            Scanner sc = new Scanner(new File(args[0]));

            DataSource dataSource = new DataSource(sc.nextLine());
            final double OPF = sc.nextDouble();

            sc.close();

            Instances instances = dataSource.getDataSet();

            mQs = new double[instances.numAttributes()][];

            List<List<Integer>> outliers = getOutlierInfo(instances, OPF);

            printOutlierStats(instances, getAttributeOutlierStats(instances, outliers));
            printInstanceOutlierStats(instances, outliers);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static List<List<Integer>> getOutlierInfo(Instances instances, double opf) throws Exception {
        List<List<Integer>> outliers = new ArrayList<>();
        Instances result = filterIqr(instances, opf);
        for (int i = 0; i < result.numInstances(); i++) {
            List<Integer> att = new ArrayList<>();
            for (int j = 0; j < instances.numAttributes(); j++) {
                if (isOutlier(instances, result, i, j)) {
                    att.add(j);
                }
            }
            outliers.add(att);
        }

        return outliers;
    }

    public static int[][] getAttributeOutlierStats(Instances instances, List<List<Integer>> outliers) {
        int[][] stats = new int[instances.numAttributes()][2];
        for (int i = 0; i < instances.numInstances(); i++) {
            List<Integer> attList = outliers.get(i);
            for (int att : attList) {
                double median = getMedian(instances, 0, instances.numInstances() - 1, att);
                stats[att][isOutlierLow(instances, i, att, median) ? 0 : 1]++;
            }
        }
        return stats;
    }

    public static boolean isOutlier(Instances instances, Instances result, int index, int att) throws Exception {
        return result.instance(index).stringValue(att * 2 + instances.numAttributes()).equals("yes");
    }

    public static boolean isOutlierLow(Instances instances, int index, int att, double median) {
        return instances.instance(index).value(att) < median;
    }

    public static Instances filterIqr(Instances instances, double opf) throws Exception {
        InterquartileRange range = new InterquartileRange();
        range.setInputFormat(instances);
        range.setExtremeValuesAsOutliers(true);
        range.setOutlierFactor(opf);
        range.setDetectionPerAttribute(true);

        return Filter.useFilter(instances, range);
    }

    public static double getMedian(Instances orig, int lower, int upper, int att) {
        Instances instances = new Instances(orig);
        instances.sort(att);
        int tot = upper - lower + 1;
        if (tot % 2 == 0) {
            return (instances.instance(lower + tot / 2 - 1).value(att) + instances.instance(lower + tot / 2).value(att)) / 2;
        } else {
            return instances.instance(lower + tot / 2).value(att);
        }
    }

    public static void printOutlierStats(Instances instances, int[][] stats) {
        ArrayList<OutlierStats> list = new ArrayList<>();
        for (int i = 0; i < stats.length; i++) {
            list.add(new OutlierStats(i, stats[i][0], stats[i][1]));
        }
        Collections.sort(list, new Comparator<OutlierStats>() {
            @Override
            public int compare(OutlierStats o1, OutlierStats o2) {
                return o2.high + o2.low - o1.high - o1.low;
            }
        });
        System.out.println(String.format("%-25s %-7s %-7s %-7s", "Attribute Name", "Low", "High", "Total"));
        for (OutlierStats os : list) {
            System.out.println(String.format("%-25s %-7d %-7d %-7d", instances.attribute(os.attIndex).name(),
                    os.low, os.high, os.low + os.high));
        }
    }

    public static void printInstanceOutlierStats(Instances instances, List<List<Integer>> outliers) throws Exception {
        List<InstanceOutlierStats> list = new ArrayList<>();

        Instances results = filterIqr(instances, 0);
        for (int i = 0; i < outliers.size(); i++) {
            list.add(new InstanceOutlierStats(i, outliers.get(i), instances, results));
        }
        Collections.sort(list, new Comparator<InstanceOutlierStats>() {
            @Override
            public int compare(InstanceOutlierStats o1, InstanceOutlierStats o2) {
                return o2.outlierAtts.size() - o1.outlierAtts.size();
            }
        });

        List<InstanceOutlierStats>[] numAtts = new List[list.get(0).outlierAtts.size()];
        for (InstanceOutlierStats stat : list) {
            if (stat.outlierAtts.size() == 0) continue;
            if (numAtts[stat.outlierAtts.size() - 1] == null) {
                numAtts[stat.outlierAtts.size() - 1] = new ArrayList<>();
            }
            numAtts[stat.outlierAtts.size() - 1].add(stat);
        }

        for (int i = numAtts.length - 1; i >= 0; i--) {
            System.out.println("Number of Attributes In Outlier Range: " + (i + 1));
            System.out.println("Number of Instances: " + numAtts[i].size());
            System.out.println("Descriptive labels for each instance:");
            for (InstanceOutlierStats stat : numAtts[i]) {
                System.out.println(stat);
            }
            System.out.println();
        }
    }

    private static class OutlierStats {
        final int attIndex;
        final int low;
        final int high;

        public OutlierStats(int attIndex, int low, int high) {
            this.attIndex = attIndex;
            this.low = low;
            this.high = high;
        }
    }

    private static class InstanceOutlierStats {
        final int index;
        final Instances rI;
        final Instances oI;
        final List<Integer> outlierAtts;

        public InstanceOutlierStats(int index, List<Integer> outlierAtts, Instances oI, Instances rI) {
            this.index = index;
            this.outlierAtts = outlierAtts;
            this.rI = rI;
            this.oI = oI;
        }

        @Override
        public String toString() {
            String result = "";
            Instance instance = oI.instance(index);
            for (int i = 0; i < instance.numAttributes(); i++) {
                result += getLabel(i);
            }
            //result+=oI.instance(index).value(oI.numAttributes()-1);

            return result;
        }

        private String getLabel(int att) {
            try {
                if (isOutlier(oI, rI, index, att)) {
                    if (isOutlierLow(oI, index, att, getMedian(oI, 0, oI.numInstances() - 1, att))) {
                        return "LOW|";
                    } else {
                        return "HIGH|";
                    }
                } else {
                    return "MEDIUM|";
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}
