package SCTrans;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import org.osgeo.proj4j.*;

public class Map {
	
	
	public String proj = "";
	
	public boolean interactive = false;
	
	public String dir = " ";

	private CRSFactory crsFactory = new CRSFactory();
	private CRSFactory targetFactory = new CRSFactory();

	private String cr_param = "+proj=utm +zone=32 +ellps=WGS84";
	private CoordinateReferenceSystem cr = crsFactory.createFromParameters("", cr_param);
	

	private CoordinateTransformFactory ctf2 = new CoordinateTransformFactory();
	private CoordinateTransform transforms2;
	
	public String runTranslate(String crname) {
		try {
			BufferedReader loc = new BufferedReader(new FileReader("location.txt"));
			dir = loc.readLine();
			loc.close();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

		String filename = "";
		File filecheck1 = new File(dir + crname + ".xml");
		File filecheck2 = new File(dir + crname + ".cr.xml");
		File filecheck3 = new File(dir + crname + "-1.cr.xml");
		
		if (filecheck1.exists()) {
			filename = dir + crname + ".xml";
			interactive = false;
		} else if (filecheck2.exists()) {
			filename = dir + crname + ".cr.xml";
			interactive = true;
		} else if (filecheck3.exists()){
			filename = dir + crname + "-1.cr.xml";
			interactive = true;
		} else {
			System.out.println("Fault filename");
		}
		
		
		String[] temp1;
		String delimeter1 = "_";
	    temp1 = crname.split(delimeter1);

		String current_dir = System.getProperty("user.dir");    
		String command = "python3 " + current_dir + "/src/MapTool/transformer.py " + filename;

		String[] lines = {"0","0","0"};
		try {
			Process process = Runtime.getRuntime().exec(command);
			BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
			String line;
			int i = 0;
			while ((line = in.readLine()) != null) {
				lines[i] = line;
				i++;
			}
            
            in.close();
			process.waitFor();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		proj = "+proj=tmerc +lat_0=" + lines[0] + " +lon_0=" + lines[1]+" +k=1 +x_0=0.0 +y_0=0.0 +datum=WGS84 +units=m +no_defs";
		String target_param = proj;
		
        CoordinateReferenceSystem target = targetFactory.createFromParameters("", target_param);
		transforms2 = ctf2.createTransform(cr, target);
		

		return crname;
	}

	public double transPointX(String x,String y) {
	    double crX = Double.parseDouble(x);
	    double crY = Double.parseDouble(y);

        ProjCoordinate projCoordinate = new ProjCoordinate(crX,crY);
    	//transforms1.transform(projCoordinate, projCoordinate);
		transforms2.transform(projCoordinate, projCoordinate);

		return projCoordinate.x;
		
	}

	public double transPointY(String x,String y) {
	    double crX = Double.parseDouble(x);
	    double crY = Double.parseDouble(y);
		ProjCoordinate projCoordinate = new ProjCoordinate(crX,crY);
		transforms2.transform(projCoordinate, projCoordinate);

		return projCoordinate.y;
	}

	public double getsin(double rot) {
		return Math.sin(rot);
	}
	
	public double getcos(double rot) {
		return Math.cos(rot);
	}
	
	public double getatan(double y, double x) {
		return Math.atan2(y, x);
	}
	
	public void test(){
		System.out.println("test");
	
		
	}

	public static void main(String ... args) {
		Map map = new Map();		
		map.test();
	}
}
