

import java.util.List; 
import java.util.Date;
import java.util.Iterator; 

import org.hibernate.HibernateException; 
import org.hibernate.Session; 
import org.hibernate.Transaction;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class TestHibernate {

   private static SessionFactory factory; 

   
@SuppressWarnings("deprecation")
public static void main(String[] args) {
	  
      try {
         factory = new Configuration().configure().buildSessionFactory();
      } catch (Throwable ex) { 
         System.err.println("Failed to create sessionFactory object." + ex);
         throw new ExceptionInInitializerError(ex); 
      }
      
      TestHibernate th = new TestHibernate();
      
      /* Add record in database */
      th.addRule("sec1000", 1001, "test rule", "allow");
     
      /* List down the rules*/
      th.listRules();
      
      /* update the rule with a different action*/
      th.updateRule(1001, "doNothing");
      
      /* List down the rules*/
      th.listRules();
      
      /* delete the rule*/
      th.deleteRule(1001);
      
   }
   
   /* Method to CREATE an employee in the database */
   public Integer addRule(String sectionId, int ruleId, String name, String action){
      Session session = factory.openSession();
      Transaction tx = null;
      Integer recordId = null;
      
      try {
         tx = session.beginTransaction();
         FirewallRule f = new FirewallRule(sectionId, ruleId, name, action);
         recordId = (Integer) session.save(f); 
         tx.commit();
      } catch (HibernateException e) {
         if (tx!=null) tx.rollback();
         e.printStackTrace(); 
      } finally {
         session.close(); 
      }
      return recordId;
   }
   
   /* Method to  READ all the rules */
   public void listRules( ){
      Session session = factory.openSession();
      Transaction tx = null;
      
      try {
         tx = session.beginTransaction();
         // this needs to map to name specified in hbm.xml file
         List employees = session.createQuery("FROM FirewallRule").list(); 
         for (Iterator iterator = employees.iterator(); iterator.hasNext();){
            FirewallRule rule = (FirewallRule) iterator.next(); 
            System.out.println(rule); 
         }
         tx.commit();
      } catch (HibernateException e) {
         if (tx!=null) tx.rollback();
         e.printStackTrace(); 
      } finally {
         session.close(); 
      }
   }
   
   /* Method to UPDATE rule's action */
   public void updateRule(Integer ruleId, String action ){
      Session session = factory.openSession();
      Transaction tx = null;
      
      try {
         tx = session.beginTransaction();
         FirewallRule rule = (FirewallRule)session.get(FirewallRule.class, ruleId); 
         rule.setAction(action);
		 session.update(rule); 
         tx.commit();
      } catch (HibernateException e) {
         if (tx!=null) tx.rollback();
         e.printStackTrace(); 
      } finally {
         session.close(); 
      }
   }
   
   /* Method to DELETE a rule from the records */
   public void deleteRule(Integer ruleId){
      Session session = factory.openSession();
      Transaction tx = null;
      
      try {
         tx = session.beginTransaction();
         FirewallRule rule = (FirewallRule)session.get(FirewallRule.class, ruleId);
         session.delete(rule); 
         tx.commit();
      } catch (HibernateException e) {
         if (tx!=null) tx.rollback();
         e.printStackTrace(); 
      } finally {
         session.close(); 
      }
   }
   
}