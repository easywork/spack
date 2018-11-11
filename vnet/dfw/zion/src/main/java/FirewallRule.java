import java.util.UUID;


public class FirewallRule {

	private String sectionId;
//	private String applyTo; 
	private int ruleId;
	private String name;
	private String action;
	
	public FirewallRule(){
	}
	
	public FirewallRule(String sectionId, int ruleId, String name, String action){
		this.sectionId = sectionId;
		this.ruleId = ruleId;
		this.name = name;
		this.action = action;
	}
	
	public String getSectionId() {
		return sectionId;
	}
	
	public void setSectionId(String id) {
		this.sectionId = id;
	}
	
	public int getRuleId() {
		return ruleId;
	}
	
	public void setRuleId(int ruleId) {
		this.ruleId = ruleId;
	}
	
	public String getName() {
		return name;
	}
	
	public void setName(String name) {
		this.name = name;
	}
	
	public String getAction() {
		return action;
	}
	
	public void setAction(String action) {
		this.action = action;
	}
	
	@Override
	public String toString() {
		return "Rule ID:" + ruleId + " Section ID:" + sectionId + " Name:" + name + " Action:" + action; 
	}
	
	
}
