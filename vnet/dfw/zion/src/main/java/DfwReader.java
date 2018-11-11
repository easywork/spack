import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.Element;


public class DfwReader {
	
	public String NODE_LIST1 = "layer3" ;
	public List <FirewallRule> ruleset = new ArrayList<FirewallRule>();
	
	public List<FirewallRule> getRuleset(){
		
		return this.ruleset;
		
	}
	
	public void parse(String filename){
		
		try {
			File xmlFile = new File(filename);
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
			Document doc = dBuilder.parse(xmlFile);
			doc.getDocumentElement().normalize();
			
			//read this - http://stackoverflow.com/questions/13786607/normalization-in-dom-parsing-with-java-how-does-it-work
			// doc.getDocumentElement().normalize();

			// System.out.println("Root element :" + doc.getDocumentElement().getNodeName());
		
			/*
			NodeList nList = doc.getElementsByTagName(NODE_LIST1);
			
         
			for (int temp = 0; temp < nList.getLength(); temp++) {

				Node nNode = nList.item(temp);
				
				if (nNode.getNodeType() == Node.ELEMENT_NODE) {

					Element eElement = (Element) nNode;
					String layer3Sections = eElement.getAttribute("layer3Sections");
					System.out.println("Layer 3 section:" + layer3Sections);
					System.out.println("Staff id : " + eElement.getAttribute("id"));
					System.out.println("Salary : " + eElement.getElementsByTagName("salary").item(0).getTextContent());
				}
			}
			*/
			
			parseLayer3Rules(doc);
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	} 
	
	public void parseLayer3Rules(Document doc){
		
		// System.out.println("Root Element:" + doc.getDocumentElement().getNodeName());
		
		Element rootNode = (Element) doc.getElementsByTagName("layer3Sections").item(0);
		
		try {
			
			NodeList sections = rootNode.getElementsByTagName("section");
			
			for (int i = 0; i < sections.getLength(); i++) {
				
				Node section = sections.item(i);
				
				if (section.getNodeType() == Node.ELEMENT_NODE) {
					
					Element e = (Element) section;
					//String uuid_str =  e.getAttribute("id");
					//byte[] bytes = uuid_str.getBytes("UTF-8");
					//UUID sectionId = UUID.nameUUIDFromBytes(bytes);
					String sectionId = e.getAttribute("id");
					
					NodeList rules = (NodeList) e.getElementsByTagName("rule");
					
					for (int j = 0; j < rules.getLength(); j++) {
					
						Node rule = rules.item(j);
						
						if (rule.getNodeType() == Node.ELEMENT_NODE) {
							
							Element x = (Element) rule;
							int ruleId = Integer.valueOf(x.getAttribute("id"));
							String name = x.getElementsByTagName("name").item(0).getTextContent();
							String action = x.getElementsByTagName("action").item(0).getTextContent();
							
							FirewallRule r = new FirewallRule();
							r.setSectionId(sectionId);
							r.setRuleId(ruleId);
							r.setName(name);
							r.setAction(action);
							this.ruleset.add(r);
						}
					}
				}
			}
		} catch (Exception e) {
			
		}
		
	}

} //end of class



