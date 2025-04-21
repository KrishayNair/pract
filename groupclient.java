Reciever:
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
public class TcpReceiver {
 private static final String HOST = "localhost";
 private static final int PORT = 5000;
 public static void main(String[] args) {
 List<Message> receivedMessages = new ArrayList<>();
 try ( 
    Socket socket = new Socket(HOST, PORT);
 BufferedReader reader = new BufferedReader(
 new InputStreamReader(socket.getInputStream())
 )
 ) {
 System.out.println("Connected to server");
 String message;
 while ((message = reader.readLine()) != null) {
 System.out.println("Receiver received: " + message);
 // Extract sequence number
 String[] parts = message.split(" ");
 int sequenceNumber = Integer.parseInt(parts[1]);
 // Store message
 receivedMessages.add(new Message(sequenceNumber, message));
 // Sort messages by sequence number
 Collections.sort(
 receivedMessages,
 Comparator.comparingInt(Message::getSequenceNumber)
 );
 // Print messages in order
 System.out.println("Ordered messages:");
 for (Message msg : receivedMessages) {
 System.out.println(msg.getMessage());
 }
 }
 } catch (IOException e) {
 System.out.println("Disconnected from server");
 }
 }
 // Helper class to store messages
 static class Message {
 private final int sequenceNumber;
 private final String message;
 public Message(int sequenceNumber, String message) { 
    this.sequenceNumber = sequenceNumber;
 this.message = message;
 }
 public int getSequenceNumber() {
 return sequenceNumber;
 }
 public String getMessage() {
 return message;
 }
 }
} 
