import java.util.*;
import java.util.concurrent.*;
class Node implements Runnable {
 private int nodeId;
 private BlockingQueue<TimeRequest> coordinatorQueue;
 private BlockingQueue<Double> adjustmentQueue;
 public Node(
 int nodeId,
 BlockingQueue<TimeRequest> coordinatorQueue,
 BlockingQueue<Double> adjustmentQueue
 ) {
 this.nodeId = nodeId;
 this.coordinatorQueue = coordinatorQueue;
 this.adjustmentQueue = adjustmentQueue;
 }
 @Override
 public void run() {
 // Simulate a node with a random clock time (in milliseconds)
 int localTime = new Random().nextInt(2000) + 1000;
 // Simulate network delay (between 10ms to 100ms)
 try {
 Thread.sleep(new Random().nextInt(90) + 10);
 } catch (InterruptedException e) {
 Thread.currentThread().interrupt();
 }
 // Send the local time to the coordinator
 try {
 coordinatorQueue.put(new TimeRequest(nodeId, localTime));
 } catch (InterruptedException e) {
 Thread.currentThread().interrupt();
 }
 // Wait for time adjustment from the coordinator
 try {
 double adjustment = adjustmentQueue.take();
 double adjustedTime = localTime + adjustment;
 System.out.println(
 "Node " +
 nodeId +
 " adjusted time from " +
 localTime +
 " to " +
 adjustedTime
 );
 } catch (InterruptedException e) {
 Thread.currentThread().interrupt();
 }
 }
}
class TimeRequest {
 int nodeId;
 int localTime;
 public TimeRequest(int nodeId, int localTime) {
 this.nodeId = nodeId;
 this.localTime = localTime;
 }
}
class Coordinator implements Runnable {
 private int numNodes;
 private BlockingQueue<TimeRequest> coordinatorQueue;
 private BlockingQueue<Double> adjustmentQueue;
 public Coordinator(
 int numNodes,
 BlockingQueue<TimeRequest> coordinatorQueue,
 BlockingQueue<Double> adjustmentQueue
 ) {
 this.numNodes = numNodes;
 this.coordinatorQueue = coordinatorQueue;
 this.adjustmentQueue = adjustmentQueue;
 } 
 @Override
 public void run() {
 int totalTime = 0;
 List<TimeRequest> nodeTimes = new ArrayList<>();
 // Collect time from all nodes
 for (int i = 0; i < numNodes; i++) {
 try {
 TimeRequest timeRequest = coordinatorQueue.take();
 nodeTimes.add(timeRequest);
 totalTime += timeRequest.localTime;
 } catch (InterruptedException e) {
 Thread.currentThread().interrupt();
 }
 }
 // Calculate the average time
 double averageTime = totalTime / (double) numNodes;
 System.out.println("Coordinator calculated average time: " + averageTime);
 // Send adjustment to each node
 for (TimeRequest timeRequest : nodeTimes) {
 double adjustment = averageTime - timeRequest.localTime;
 System.out.println(
 "Coordinator sending adjustment " +
 adjustment +
 " to Node " +
 timeRequest.nodeId
 );
 try {
 adjustmentQueue.put(adjustment);
 } catch (InterruptedException e) {
 Thread.currentThread().interrupt();
 }
 }
 }
}
public class BerkeleyAlgorithm {
 public static void main(String[] args) throws InterruptedException {
 int numNodes = 5; // Number of nodes
 BlockingQueue<TimeRequest> coordinatorQueue = new LinkedBlockingQueue<>();
 BlockingQueue<Double> adjustmentQueue = new LinkedBlockingQueue<>();
 // Start the coordinator thread
 Thread coordinatorThread = new Thread(
 new Coordinator(numNodes, coordinatorQueue, adjustmentQueue)
 );
 coordinatorThread.start();
 // Start the node threads
 List<Thread> nodeThreads = new ArrayList<>();
 for (int i = 0; i < numNodes; i++) {
 Node node = new Node(i, coordinatorQueue, adjustmentQueue);
 Thread nodeThread = new Thread(node);
 nodeThreads.add(nodeThread);
 nodeThread.start();
 }
 // Wait for all nodes to finish
 for (Thread nodeThread : nodeThreads) {
 nodeThread.join();
 }
 // Wait for the coordinator to finish
 coordinatorThread.join();
 }
} 
