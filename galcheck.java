import javax.naming.*;
import javax.naming.directory.*;
import java.util.Hashtable;

public class LdapEmailCheck {
    public static void main(String[] args) {
        String ldapServer = "ldap://your_ldap_server";
        String domain = "yourdomain.com";
        String adminUser = "your_username@" + domain;
        String adminPassword = "your_password";
        String emailToCheck = "user@yourdomain.com";

        Hashtable<String, String> env = new Hashtable<>();
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        env.put(Context.PROVIDER_URL, ldapServer);
        env.put(Context.SECURITY_AUTHENTICATION, "simple");
        env.put(Context.SECURITY_PRINCIPAL, adminUser);
        env.put(Context.SECURITY_CREDENTIALS, adminPassword);

        try {
            DirContext ctx = new InitialDirContext(env);
            String searchFilter = "(mail=" + emailToCheck + ")";
            SearchControls sc = new SearchControls();
            sc.setSearchScope(SearchControls.SUBTREE_SCOPE);

            NamingEnumeration<SearchResult> results = ctx.search("dc=yourdomain,dc=com", searchFilter, sc);
            boolean exists = results.hasMore();
            ctx.close();

            System.out.println("Email exists in GAL: " + exists);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
