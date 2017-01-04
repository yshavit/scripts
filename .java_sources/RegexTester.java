import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

public class RegexTester {
  public static void main(String[] args) {
    if (args.length < 2) {
      System.err.println("Usage: <regex> <match-against> [match-against ...]");
      System.err.println();
      System.err.println("Compiles the given regex and applies it against each of the match-against strings.");
      System.err.println("For each one, prints whether it matched, and if it did, the matched groups.");
      System.exit(1);
    }

    Pattern compiled;
    try {
      compiled = Pattern.compile(args[0]);
    } catch (PatternSyntaxException e) {
      System.err.println("Invalid pattern: " + e.getMessage());
      System.exit(2);
      throw e; // won't get here, but tells javac that "compiled" has been assigned, below
    }
    for (int i = 1; i < args.length; ++i) {
      String matchAgainst = args[i];
      Matcher matcher = compiled.matcher(matchAgainst);
      System.out.print('<');
      System.out.print(matchAgainst);
      System.out.print("> ");
      if (matcher.matches()) {
        System.out.println("MATCH");
        int groupCount = matcher.groupCount();
        System.out.printf("%d group%s", groupCount, groupCount == 1 ? "" : "s");
        if (groupCount > 0) {
          System.out.println(":");
          for (int group = 0; group < groupCount; ++group) {
            System.out.printf("%d: %s%n", group, matcher.group(group + 1));
          }
        } else {
          System.out.println();
        }
      } else {
        System.out.println("NO MATCH");
      }
      if ((i + 1) < args.length) {
        System.out.println("---------------------");
      }
    }
  }
}
