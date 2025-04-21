import java.util.ArrayList;
import java.util.List;
import java.util.Random;
class Node {
 int nodeId;
 int totalNodes;
 boolean isLeader;
 boolean isActive;
 boolean electionInProgress;
 public Node(int nodeId, int totalNodes) {
 this.nodeId = nodeId;
 this.totalNodes = totalNodes;
 this.isLeader = false;
 this.isActive = true;
 this.electionInProgress = false;
 } 
 // Start the election process
 public void startElection() {
 if (!isActive) {
 System.out.println("Node " + nodeId + " is inactive.");
 return;
 }
 System.out.println("Node " + nodeId + " started the election.");
 // Notify all nodes with higher IDs
 for (int i = nodeId + 1; i < totalNodes; i++) {
 System.out.println(
 "Node " + nodeId + " sends 'election' message to Node " + i + "."
 );
 }
 // Simulate waiting for replies
 try {
 Thread.sleep(new Random().nextInt(2000) + 1000);
 } catch (InterruptedException e) {
 e.printStackTrace();
 }
 electionResponse();
 }
 // Election response logic
 public void electionResponse() {
 if (electionInProgress) return;
 electionInProgress = true;
 // Simulate the situation where higher nodes reply
 List<Integer> higherNodes = new ArrayList<>();
 for (int i = nodeId + 1; i < totalNodes; i++) {
 higherNodes.add(i);
 }
 if (!higherNodes.isEmpty()) {
 System.out.println(
 "Node " + nodeId + " receives election message. Sending reply."
 );
 try {
 Thread.sleep(new Random().nextInt(1000) + 500);
 } catch (InterruptedException e) {
 e.printStackTrace();
 }
 // A higher node starts a new election
 int nextNode = higherNodes.get(new Random().nextInt(higherNodes.size()));
 System.out.println(
 "Node " + nodeId + " started new election as higher node responds."
 );
 // Simulate the election with the next node
 new Node(nextNode, totalNodes).startElection();
 } else {
 // No higher node responded, this node is the leader
 System.out.println(
 "Node " + nodeId + " wins the election and becomes the leader."
 );
 isLeader = true;
 for (int i = 0; i < totalNodes; i++) {
 if (i != nodeId) {
 System.out.println(
 "Node " + nodeId + " sends 'victory' message to Node " + i + "."
 );
 }
 }
 stopElection();
 }
 }
 // Simulate node crash (failure)
 public void crash() {
 isActive = false;
 System.out.println("Node " + nodeId + " crashed and is inactive.");
 }
 // Simulate node recovery
 public void recover() {
 isActive = true;
 System.out.println("Node " + nodeId + " recovered and is active.");
 }
 // Stop election process once a leader is elected
  private void stopElection() {
 election.setLeaderElected(true); // Notify the election process to stop
 }
}
public class election {
 private static boolean leaderElected = false; // Shared flag to stop election once a leader is
elected
 public static synchronized void setLeaderElected(boolean status) {
 leaderElected = status;
 }
 public static synchronized boolean isLeaderElected() {
 return leaderElected;
 }
 // Method to simulate node failure/recovery
 public static void simulateCrashOrRecovery(List<Node> nodes) {
 Random random = new Random();
 while (!isLeaderElected()) {
 int nodeIndex = random.nextInt(nodes.size());
 Node node = nodes.get(nodeIndex);
 if (random.nextDouble() < 0.2) {
 if (node.isActive) {
 node.crash();
 } else {
 node.recover();
 }
 }
 try {
 Thread.sleep(5000);
 } catch (InterruptedException e) {
 e.printStackTrace();
 }
 }
 }
 // Method to simulate the start of the election process
 public static void electionProcess(List<Node> nodes) {
 Random random = new Random();
 while (!isLeaderElected()) {
 int nodeIndex = random.nextInt(nodes.size());
 Node node = nodes.get(nodeIndex);
 if (node.isActive) {
 node.startElection();
 }
 try {
 Thread.sleep(random.nextInt(3000) + 2000); // Random delay to simulate failure detection
 } catch (InterruptedException e) {
 e.printStackTrace();
 }
 }
 }
 public static void main(String[] args) {
 int totalNodes = 5;
 List<Node> nodes = new ArrayList<>();
 // Create 5 nodes
 for (int i = 0; i < totalNodes; i++) {
 nodes.add(new Node(i, totalNodes));
 }
 // Start the election process in a separate thread
 Thread electionThread = new Thread(() -> electionProcess(nodes));
 electionThread.start();
 // Simulate random crashes and recoveries in a separate thread
 Thread crashThread = new Thread(() -> simulateCrashOrRecovery(nodes));
 crashThread.start();
 }
} 