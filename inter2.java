import java.io.*;
import java.util.*;
import java.net.*;
public class TCPClient {
 public static void main(String args[]) throws Exception {
 System.out.println("Connecting...");
 Socket client = new Socket("127.0.0.1", 25);
 System.out.println("Connected!");
 DataInputStream din = new DataInputStream(client.getInputStream());
 DataOutputStream dout = new DataOutputStream(client.getOutputStream());
 Scanner sc = new Scanner(System.in);
 String send = "";
 while (!send.equals("stop")) {
 System.out.print("Send: ");
 send = sc.nextLine();
 dout.writeUTF(send);
 }
 dout.flush();
 String recv = din.readUTF();
 System.out.println("Sum of the integers is: " + recv);
 dout.close();
 din.close();
 client.close();
 }
} 