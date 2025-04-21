import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
public class TcpServer {
 private static final String HOST = "localhost";
 private static final int PORT = 5000;
 private static int sequenceNumber = 0;
 public static void main(String[] args) {
 try (ServerSocket serverSocket = new ServerSocket(PORT)) {
 System.out.println("Server listening on " + HOST + ":" + PORT);
 while (true) {
 Socket clientSocket = serverSocket.accept();
 System.out.println("Client connected");
 handleClient(clientSocket);
 }
 } catch (IOException e) {
 e.printStackTrace();
 }
 }
 private static void handleClient(Socket clientSocket) {
 ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
 try {
 OutputStream outputStream = clientSocket.getOutputStream();
 PrintWriter writer = new PrintWriter(outputStream, true);
 Runnable sendMessageTask = () -> {
 String message = "Message " + sequenceNumber;
 System.out.println("Server sending: " + message);
 writer.println(message);
 sequenceNumber++;
 };
 scheduler.scheduleAtFixedRate(sendMessageTask, 0, 2, TimeUnit.SECONDS);
 // Wait for client to disconnect
 clientSocket.getInputStream().read();
 } catch (IOException e) {
 System.out.println("Client disconnected");
 } finally {
 scheduler.shutdown();
 try {
 clientSocket.close();
 } catch (IOException e) {
 e.printStackTrace();
 }
 }
 }
} 