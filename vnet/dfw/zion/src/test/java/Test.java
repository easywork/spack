import java.util.List;


public class Test {
	
	public static void main(String[] args) {
		
		String testfile = System.getProperty("user.dir") + "/data/" + "firewall.xml";
		DfwReader dfw = new DfwReader();
		dfw.parse(testfile);
		@SuppressWarnings("unchecked")
		List<FirewallRule> ruleset = dfw.getRuleset();
				
		for (FirewallRule r : ruleset) {
			System.out.println(r);
		}
		
	}
	
}