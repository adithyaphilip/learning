import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;

import javax.imageio.ImageIO;

public class DMA10AdithyaAbrahamPhilip {
	
	// factor to multiply distance by in the euclidian distance measure
	final static double COLOR_EPS = 0.3;
	final static double PHYS_EPS = 1;
	final static int MIN_PTS = 30;
	
	private static class Pixel {
		final double x; // column position in image
		final double y; // row position in image
		final double red;
		final double blue;
		final double green;
		// cluster number once assigned, if -1 is noise
		int cno = -1;
		public Pixel(double x, double y, double r, double g, double b) {
			this.x = x;
			this.y = y;
			red = r;
			green = g;
			blue = b;
		}
	}

	public static void main(String[] args) throws Exception {
		if (args.length != 2) {
			System.out.println("Usage: <program> input.gif output.gif");
			System.exit(1);
		}
		BufferedImage in = ImageIO.read(new File(args[0]));

		int numPixels = in.getHeight() * in.getWidth();		
		
		Pixel[] pixels = new Pixel[numPixels];

		int ictr = 0;
		for (int i = 0; i < in.getHeight(); i++) {
			for (int j = 0; j < in.getWidth(); j++) {
				Color c = new Color(in.getRGB(j, i));
				// store normalised values in the pixel
				Pixel pixel = new Pixel(j/(double)in.getWidth(), i/(double)in.getHeight(), c.getRed()/255.0, c.getGreen()/255.0, c.getBlue()/255.0);
				pixels[ictr++] = pixel;
			}
		}
		
		int cnum = dbScan(pixels, MIN_PTS, COLOR_EPS, PHYS_EPS);
		
		double rgbsums[][] = new double[cnum][3];
		int cctr[] = new int[cnum];
		
		// for each cluster, get sum of rgb values of all points in it
		for(int i = 0; i<pixels.length; i++) {
			int cluster = pixels[i].cno;
			if (cluster == -1) continue;
			//de-normalize the values
			rgbsums[cluster][0] += pixels[i].red*255;
			rgbsums[cluster][1] += pixels[i].green*255;
			rgbsums[cluster][2] += pixels[i].blue*255;
			cctr[cluster]++;
			// System.out.println(i + " " + cluster);
		}
		
		// get averages of cluster colors
		for(int i = 0; i<rgbsums.length; i++) {
			rgbsums[i][0] /= cctr[i];
			rgbsums[i][1] /= cctr[i];
			rgbsums[i][2] /= cctr[i];
		}
		
		// output image
		BufferedImage out = new BufferedImage(in.getWidth(), in.getHeight(), BufferedImage.TYPE_INT_RGB);

		int ctr = 0;
		int noise = 0;
		for (int i = 0; i < in.getHeight(); i++) {
			for (int j = 0; j < in.getWidth(); j++) {
				int cluster = pixels[ctr++].cno;
				if (cluster != -1) {
					out.setRGB(j, i, new Color((100 + (int)rgbsums[cluster][1])%255, (int)rgbsums[cluster][2], (int)rgbsums[cluster][0]).getRGB());
				} else {
					noise++;
					out.setRGB(j, i, new Color((100 + (int)(pixels[ctr-1].green*255))%255, (int)(pixels[ctr-1].blue*255), (int)(pixels[ctr-1].red*255)).getRGB());
				}
			}
		}		
	
		File f = new File(args[1]);
		ImageIO.write(out, "GIF", f);

		System.out.println("Total no. of pixels: " + numPixels);
		System.out.println("No. of clusters: " + cnum);
		System.out.println("No. of noise points: " + noise);
		
		// table
		System.out.println(String.format("%-10s|%-10s|%-10s|%-10s|%-10s", "Cluster #", "Size", "Avg. Red", "Avg. Green", "Avg. Blue"));
		for(int i = 0; i<cnum; i++) {
			System.out.println(String.format("%-10d|%-10d|%-10.0f|%-10.0f|%-10.0f", i, cctr[i], rgbsums[i][0], rgbsums[i][1], rgbsums[i][2]));			
		}
		System.out.println("");
	}
	
	/**
	 * 
	 * @param pixels array of all pixels in image
	 * @param minPts
	 * @param eps
	 * @return number of clusters formed
	 */
	public static int dbScan(Pixel[] pixels, int minPts, double colorEps, double physEps) {
		int currCluster = -1;
		for(int i = 0; i<pixels.length; i++) {
			Pixel pixel = pixels[i];
			
			if (pixel.cno != -1) continue;
			ArrayList<Integer> neighbours = getNeighbours(i, pixels, colorEps, physEps);
			if (neighbours.size() >= minPts) {
				currCluster++;
				addToCluster(neighbours, pixels, colorEps, physEps, minPts, currCluster);
			}
		}
		return currCluster + 1;
	}
	
	public static ArrayList<Integer> getNeighbours(int i, Pixel pixels[], double colorEps, double physEps) {
		ArrayList<Integer> n = new ArrayList<>();
		for(int j = 0; j<pixels.length; j++) {
			Pixel p1 = pixels[i], p2 = pixels[j];
			if (getColorDistance(p1, p2) <= colorEps && getPhysicalDistance(p1, p2) <= physEps) {
				// will include p1 itself
				n.add(j);
			}
		}
		return n;
	}
	
	public static double getColorDistance(Pixel p1, Pixel p2) {
		return Math.sqrt(
				Math.pow(p1.red - p2.red, 2)
				+ Math.pow(p1.green - p2.green, 2)
				+ Math.pow(p1.blue - p2.blue, 2)
				);
	}
	
	public static double getPhysicalDistance(Pixel p1, Pixel p2) {
		return Math.sqrt(Math.pow((p1.x - p2.x), 2)+ Math.pow((p1.y - p2.y), 2));
	}
	
	public static void addToCluster(ArrayList<Integer> n, Pixel[] pixels, double colorEps, double physEps, int minPts, int c) {
		// System.out.println(c);
		ArrayList<Integer> nt = new ArrayList<>();
		for (int i:n) {
			if (pixels[i].cno ==-1) {
				nt.add(i);
				pixels[i].cno = c;
			}
		}
		for (int i:nt) {
				ArrayList<Integer> n2 = getNeighbours(i, pixels, colorEps, physEps);
				if (n2.size()>=minPts) {
					addToCluster(n2, pixels, colorEps, physEps, minPts, c);
				}
		}
	}
	
}