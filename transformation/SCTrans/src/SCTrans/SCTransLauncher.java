package SCTrans;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
/**
 * 
 */
/**

 * @author SCTrans
 *
 */
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

import org.eclipse.emf.common.util.Diagnostic;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.util.BasicExtendedMetaData;
import org.eclipse.emf.ecore.util.Diagnostician;
import org.eclipse.emf.ecore.util.ExtendedMetaData;
import org.eclipse.emf.ecore.xmi.XMLResource;
import org.eclipse.emf.ecore.xmi.impl.EcoreResourceFactoryImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;
import org.eclipse.m2m.atl.emftvm.EmftvmFactory;
import org.eclipse.m2m.atl.emftvm.ExecEnv;
import org.eclipse.m2m.atl.emftvm.Metamodel;
import org.eclipse.m2m.atl.emftvm.Model;
import org.eclipse.m2m.atl.emftvm.impl.resource.EMFTVMResourceFactoryImpl;
import org.eclipse.m2m.atl.emftvm.util.DefaultModuleResolver;
import org.eclipse.m2m.atl.emftvm.util.ModuleResolver;
import org.eclipse.m2m.atl.emftvm.util.TimingData;

import org.json.JSONObject;
import org.json.XML;
import org.json.JSONArray;

public class SCTransLauncher {

// Some constants for quick initialization and testing.
public final static String IN_METAMODEL = "./metamodels/CommonRoad.ecore";
public final static String IN_METAMODEL_NAME = "CommonRoad";
public final static String OUT_METAMODEL_LGSVL = "./metamodels/Lgsvl.ecore";
public final static String OUT_METAMODEL_NAME_LGSVL = "Lgsvl";
public final static String OUT_METAMODEL_OPENSCENARIO = "./metamodels/OpenSCENARIO.ecore";
public final static String OUT_METAMODEL_NAME_OPENSCENARIO = "OpenSCENARIO";

public final static String TRANSFORMATION_DIR = "./transformations/";
public final static String TRANSFORMATION_MODULE_LGSVL= "cr2lgsvl";
public final static String TRANSFORMATION_MODULE_OPENSCENARIO= "cr2openscenario";

// The input and output metamodel nsURIs are resolved using lazy registration of metamodels, see below.
private String inputMetamodelNsURI;
private String outputMetamodelNsURI;

//Main transformation launch method
public void launch(String inMetamodelPath, String inModelPath, String outMetamodelPath,
		String outModelPath,String outMetamodelName, String transformationDir, String transformationModule){
	
	/* 
	 * Creates the execution environment where the transformation is going to be executed,
	 * you could use an execution pool if you want to run multiple transformations in parallel,
	 * but for the purpose of the example let's keep it simple.
	 */
	ExecEnv env = EmftvmFactory.eINSTANCE.createExecEnv();
	ResourceSet rs = new ResourceSetImpl();


	/*
	 * Load meta-models in the resource set we just created, the idea here is to make the meta-models
	 * available in the context of the execution environment, the ResourceSet is later passed to the
	 * ModuleResolver that is the actual class that will run the transformation.
	 * Notice that we use the nsUris to locate the metamodels in the package registry, we initialize them 
	 * from Ecore files that we registered lazily as shown below in e.g. registerInputMetamodel(...) 
	 */
	Metamodel inMetamodel = EmftvmFactory.eINSTANCE.createMetamodel();
	inMetamodel.setResource(rs.getResource(URI.createURI(inputMetamodelNsURI), true));
	env.registerMetaModel(IN_METAMODEL_NAME, inMetamodel);
	
	Metamodel outMetamodel = EmftvmFactory.eINSTANCE.createMetamodel();
	outMetamodel.setResource(rs.getResource(URI.createURI(outputMetamodelNsURI), true));
	env.registerMetaModel(outMetamodelName, outMetamodel);
	
	/*
	 * Create and register resource factories to read/parse .xmi and .emftvm files,
	 * we need an .xmi parser because our in/output models are .xmi and our transformations are
	 * compiled using the ATL-EMFTV compiler that generates .emftvm files
	 */
	rs.getResourceFactoryRegistry().getExtensionToFactoryMap().put("xmi", new XMIResourceFactoryImpl());
	rs.getResourceFactoryRegistry().getExtensionToFactoryMap().put("emftvm", new EMFTVMResourceFactoryImpl());
	
	// Load models
	Model inModel = EmftvmFactory.eINSTANCE.createModel();
	inModel.setResource(rs.getResource(URI.createURI(inModelPath, true), true));
	env.registerInputModel("IN", inModel);
	
	Model outModel = EmftvmFactory.eINSTANCE.createModel();
	outModel.setResource(rs.createResource(URI.createURI(outModelPath)));
	env.registerOutputModel("OUT", outModel);
	
	/*
	 *  Load and run the transformation module
	 *  Point at the directory your transformations are stored, the ModuleResolver will 
	 *  look for the .emftvm file corresponding to the module you want to load and run
	 */
	ModuleResolver mr = new DefaultModuleResolver(transformationDir, rs);
	TimingData td = new TimingData();
	env.loadModule(mr, transformationModule);
	td.finishLoading();
	env.run(td);
	td.finish();

	EObject outobjectmodel = outModel.getResource().getContents().get(0);
	Diagnostic diagnostic = Diagnostician.INSTANCE.validate(outobjectmodel);
	List<Diagnostic> diagnosticChild = diagnostic.getChildren();
	
	if (diagnosticChild.isEmpty()) {
		if (diagnostic.getSeverity() == Diagnostic.ERROR) {
			System.out.println(diagnostic.getMessage());
		}
	} else {
		for (Diagnostic d : diagnosticChild) {
			if (d.getSeverity() == Diagnostic.ERROR) {
				System.out.println(d.getMessage());
			}
		}
	}
	
	// Save models
	try {
		outModel.getResource().save(Collections.emptyMap());
	} catch (IOException e) {
		e.printStackTrace();
	}
}

private String lazyMetamodelRegistration(String metamodelPath){
	
	Resource.Factory.Registry.INSTANCE.getExtensionToFactoryMap().put("ecore", new EcoreResourceFactoryImpl());

   	
    ResourceSet rs = new ResourceSetImpl();
    // Enables extended meta-data, weird we have to do this but well...
    final ExtendedMetaData extendedMetaData = new BasicExtendedMetaData(EPackage.Registry.INSTANCE);
    rs.getLoadOptions().put(XMLResource.OPTION_EXTENDED_META_DATA, extendedMetaData);

    Resource r = rs.getResource(URI.createFileURI(metamodelPath), true);
    EObject eObject = r.getContents().get(0);
    // A meta-model might have multiple packages we assume the main package is the first one listed
    if (eObject instanceof EPackage) {
        EPackage p = (EPackage)eObject;
        //System.out.println(p.getNsURI());
        EPackage.Registry.INSTANCE.put(p.getNsURI(), p);
        return p.getNsURI();
    }
    return null;
}

public void registerInputMetamodel(String inputMetamodelPath){	
	inputMetamodelNsURI = lazyMetamodelRegistration(inputMetamodelPath);
}


public void registerOutputMetamodel(String outputMetamodelPath){
	outputMetamodelNsURI = lazyMetamodelRegistration(outputMetamodelPath);
}

public void writeLocation(String filepath) throws IOException {
	FileOutputStream outputStream = new FileOutputStream(new File("location.txt"));
	outputStream.write(filepath.getBytes());

}

public String formatXML(String dir, String input) throws IOException {
	//read 
	String file = dir + input;
	FileInputStream fis=new FileInputStream(file);
    InputStreamReader isr=new InputStreamReader(fis, "UTF-8");
    BufferedReader br = new BufferedReader(isr);
    
    String line = "";
    ArrayList<String> arrs = new ArrayList<String>();
    String boolline1 = br.readLine();
    arrs.add(boolline1);
    while ((line=br.readLine())!=null) {
        arrs.add(line);
    }
    br.close();
    isr.close();
    fis.close();
    
    //new file
    String new_file = input;
    new_file = new_file.replace(".cr.xml", "");
    new_file = new_file.replace(".xml", "");
    new_file = new_file + ".xmi";
    String new_file_path = dir + new_file;
    // write
    FileOutputStream fos=new FileOutputStream(new File(new_file_path));
    OutputStreamWriter osw=new OutputStreamWriter(fos, "UTF-8");
    BufferedWriter  bw=new BufferedWriter(osw);
    
    int i = 0;
    if (!boolline1.contains("?xml")) {
        String add_line0 = "<?xml version='1.0' encoding='UTF-8'?>\n";
        bw.write(add_line0);
    } else {
    	bw.write(arrs.get(0)+"\n");
    	i = 1;
    }
    
    String add_line1 = "<commonroad.in.tum.de:DocumentRoot xmi:version=\"2.0\" xmlns:xmi=\"http://www.omg.org/XMI\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:commonroad.in.tum.de=\"file://../metamodels/CommonRoad.ecore\" xsi:schemaLocation=\"../metamodels/CommonRoad.ecore\">\n";
    bw.write(add_line1);
    String arr = null;
    for (;i < arrs.size();i++) {
    	arr = arrs.get(i);
    	bw.write(arr+"\n");
    }
   
    String add_line2 = "</commonroad.in.tum.de:DocumentRoot>";
    bw.write(add_line2);
    
    bw.close();
    osw.close();
    fos.close();
    
    return new_file;
}

public void formatJson(String file) throws IOException {
	String jsonFile = file.replace("_out.xmi", ".json");
	FileInputStream fis = new FileInputStream(file);
    InputStreamReader isr = new InputStreamReader(fis, "UTF-8");
    BufferedReader br = new BufferedReader(isr);
    
    String line1 = "";
    String line2 = "";
    String xml= null;
    line1 = br.readLine();
    line1 = br.readLine();
    
    while ((line1=br.readLine())!=null) {
        xml = xml + line2;
        line2 = line1;
    }
    br.close();
    isr.close();
    fis.close();
    
    
    JSONObject xmlJSONObj = XML.toJSONObject(xml);
    xmlJSONObj.put("controllables", new String[] {});
    xmlJSONObj.put("version","0.01");
    JSONArray xmlarray=xmlJSONObj.getJSONArray("agents");
    for (int i =0; i< xmlarray.length();i++) {
    	
    	if ((!xmlarray.getJSONObject(i).isNull("behaviour")) && (xmlarray.getJSONObject(i).getJSONObject("behaviour").getString("name").equals("NPCLaneFollowBehaviour"))) {
    		//System.out.println(xmlarray.getJSONObject(i).getJSONObject("behaviour").getString("name"));
    		xmlarray.getJSONObject(i).put("waypoints",new String[] {});
    	}
    }
	Random r = new Random();
	xmlJSONObj.getJSONObject("weather").put("rain",r.nextDouble());
	xmlJSONObj.getJSONObject("weather").put("wetness",r.nextDouble());
	xmlJSONObj.getJSONObject("weather").put("damage",r.nextDouble());
	xmlJSONObj.getJSONObject("weather").put("cloudiness",r.nextDouble());
	xmlJSONObj.getJSONObject("weather").put("fog",r.nextDouble());
	
	xmlJSONObj.getJSONObject("time").put("month",r.nextInt(11)+1);
	xmlJSONObj.getJSONObject("time").put("day",r.nextInt(28)+1);
	xmlJSONObj.getJSONObject("time").put("hour",r.nextInt(23));
	xmlJSONObj.getJSONObject("time").put("minute",r.nextInt(60));
	xmlJSONObj.getJSONObject("time").put("second",r.nextInt(60));
	
	
    String jsonPrint = xmlJSONObj.toString(4);
    FileOutputStream fos = new FileOutputStream(new File(jsonFile));
    OutputStreamWriter osw = new OutputStreamWriter(fos, "UTF-8");
    BufferedWriter bw = new BufferedWriter(osw);
    bw.write(jsonPrint);
    bw.close();
    osw.close();
    fos.close();
    
}


public void formatxosc(String dir, String input) throws IOException{
	//read
	String file = input;
	FileInputStream fis=new FileInputStream(file);
    InputStreamReader isr=new InputStreamReader(fis, "UTF-8");
    BufferedReader br = new BufferedReader(isr);
    
    String line = "";
    ArrayList<String> arrs = new ArrayList<String>();
    String boolline1 = br.readLine();
    arrs.add(boolline1);
    while ((line=br.readLine())!=null) {
        arrs.add(line);
    }
    br.close();
    isr.close();
    fis.close();
    
    //new file
    String new_file = input;
    new_file = new_file.replace("_out.xmi", ".xosc");
    String new_file_path = new_file;
    // write
    FileOutputStream fos=new FileOutputStream(new File(new_file_path));
    OutputStreamWriter osw=new OutputStreamWriter(fos, "UTF-8");
    BufferedWriter  bw=new BufferedWriter(osw);    
    
    bw.write(arrs.get(0)+"\n");   
    
    String add_line1 = "<OpenScenario>\n";
    bw.write(add_line1);
    String arr = null;
    for (int i = 2;i < arrs.size();i++) {
    	arr = arrs.get(i);
    	bw.write(arr+"\n");
    }
    
    bw.close();
    osw.close();
    fos.close();
 
}


public static void main(String ... args) throws IOException{
	// out metamodel choose OpenSCENARIO or Lgsvl
	String Out_MetaModel_Name = args[0];
	// in_model name
	String input = args[1];
	// in_model
	String dir = args[2];
	SCTransLauncher l = new SCTransLauncher();
	String IN_MODEL = dir + l.formatXML(dir, input);
	// write dir
	l.writeLocation(dir);
	String OUT_MODEL =IN_MODEL.replace(".xmi", "_out.xmi");
	if (Out_MetaModel_Name.contains("Lgsvl")) {
		System.out.println("Input Model: " + IN_MODEL);
		System.out.println("Target MetaModel: " + Out_MetaModel_Name );
		System.out.println("Transformation Model: " + TRANSFORMATION_MODULE_LGSVL);
		l.registerInputMetamodel(IN_METAMODEL);
		l.registerOutputMetamodel(OUT_METAMODEL_LGSVL);
		System.out.println("Transforming...");
		l.launch(IN_METAMODEL, IN_MODEL, OUT_METAMODEL_LGSVL, OUT_MODEL,OUT_METAMODEL_NAME_LGSVL, TRANSFORMATION_DIR, TRANSFORMATION_MODULE_LGSVL);
		l.formatJson(OUT_MODEL);
		System.out.println("Finish! Output in " + dir);
	}else if(Out_MetaModel_Name.contains("OpenSCENARIO")) {
		System.out.println("Input Model: " + IN_MODEL);
		System.out.println("Target MetaModel: " + Out_MetaModel_Name );
		System.out.println("Transformation Model: " + TRANSFORMATION_MODULE_OPENSCENARIO);
		l.registerInputMetamodel(IN_METAMODEL);
		l.registerOutputMetamodel(OUT_METAMODEL_OPENSCENARIO);
		System.out.println("Transforming...");
		l.launch(IN_METAMODEL, IN_MODEL, OUT_METAMODEL_OPENSCENARIO, OUT_MODEL,OUT_METAMODEL_NAME_OPENSCENARIO, TRANSFORMATION_DIR, TRANSFORMATION_MODULE_OPENSCENARIO);
		l.formatxosc(dir, OUT_MODEL);
		System.out.println("Finish! Output in " + dir);
	}
}

}

