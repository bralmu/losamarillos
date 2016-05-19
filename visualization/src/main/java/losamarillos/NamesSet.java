package losamarillos;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.HashSet;
import java.util.Set;

public class NamesSet {

	public Set<String> getNames() {
		Set<String> names = new HashSet<String>();
		Connection c = null;
		Statement stmt = null;
		try {
			Class.forName("org.sqlite.JDBC");
			c = DriverManager.getConnection("jdbc:sqlite:schedule.db");
			stmt = c.createStatement();
			ResultSet rs = stmt.executeQuery("SELECT * FROM SCHEDULE");
			while (rs.next()) {
				names.add(rs.getString("ORIGIN"));
				names.add(rs.getString("DESTINATION"));
			}
			stmt.close();
			c.close();
		} catch (Exception e) {
			System.err.println(e.getClass().getName() + ": " + e.getMessage());
			System.exit(0);
		}
		return names;
	}
}
