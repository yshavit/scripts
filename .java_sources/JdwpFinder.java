import com.sun.tools.attach.VirtualMachine;
import java.util.*;

class JdwpFinder {
  public static void main(String[] args) {
    if (args.length == 0) {
      System.err.println("Please pass in a list of PIDs to look up");
      System.exit(1);
    }
    for (String pid : args) {
      String addr = "<unknown>";
      VirtualMachine vm = null;
      try {
        vm = VirtualMachine.attach(pid);
        Properties props = vm.getAgentProperties();
        addr = props.getProperty("sun.jdwp.listenerAddress");
        addr = addr.replaceAll(":", " = ");
      } catch (Exception e) {
        // ignore
      } finally {
        if (vm != null) {
          try {
            vm.detach();
          } catch (Exception e) {
            // ignore
          }
        }
      }
      System.out.printf("pid %s: %s%n", pid, addr);
    }
  }
}
