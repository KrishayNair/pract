import java.rmi.Remote;
import java.rmi.RemoteException;
// Remote interface
public interface Calculator extends Remote {
 int add(int a, int b) throws RemoteException;
}
import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;
// Remote object implementation
public class CalculatorImpl extends UnicastRemoteObject implements Calculator {
 protected CalculatorImpl() throws RemoteException {
 super();
 }
 @Override
 public int add(int a, int b) throws RemoteException {
 return a + b;
 }
}
import java.rmi.Naming;
public class RMIClient {
 public static void main(String[] args) {
 try {
 // Lookup the remote object
 Calculator calculator = (Calculator)
Naming.lookup("rmi://localhost:5000/CalculatorService");
 // Call remote method
 int result = calculator.add(5, 10);
 System.out.println("Result from RMI Server: " + result);
 } catch (Exception e) { 
     e.printStackTrace();
 }
 }
}
import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;
public class RMIServer {
 public static void main(String[] args) {
 try {
 LocateRegistry.createRegistry(5000); // Use port 5000
 // Create instance of remote object
 Calculator calculator = new CalculatorImpl();
 // Bind the remote object to a name
 Naming.rebind("rmi://localhost:5000/CalculatorService", calculator);
 System.out.println("RMI Server is running...");
 } catch (Exception e) {
 e.printStackTrace();
 }
 }
}
