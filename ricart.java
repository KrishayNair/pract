import java.util.*;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
class RicartAgrawala {
 private int id; // Process ID
 private static int numProcesses; // Total number of processes
 private long[] timestamps; // Timestamps for each process (instance-level)
 private static boolean[] inCriticalSection; // Critical section status of each process
 private static Lock lock = new ReentrantLock(); // Lock for synchronizing access to critical
section
 // Constructor
 public RicartAgrawala(int id, int numProcesses) {
 this.id = id;
 RicartAgrawala.numProcesses = numProcesses;
 timestamps = new long[numProcesses]; // Instance-level array
 if (inCriticalSection == null) {
 inCriticalSection = new boolean[numProcesses]; // Initialize critical section array if not done
yet
 }
 } 
  // Request to enter critical section
 public void requestCriticalSection() {
 lock.lock();
 try {
 timestamps[id] = System.currentTimeMillis(); // Set the timestamp for this request
 System.out.println(
 "Process " + id + " requesting critical section at " + timestamps[id]
 );
 // Send requests to all other processes
 for (int i = 0; i < numProcesses; i++) {
 if (i != id) {
 sendRequest(i);
 }
 }
 // Wait for replies from all other processes
 for (int i = 0; i < numProcesses; i++) {
 if (i != id) {
 waitForReply(i);
 }
 }
 // Enter the critical section
 enterCriticalSection();
 } finally {
 lock.unlock();
 }
 }
 // Simulate sending request to another process
 private void sendRequest(int receiverId) {
 // Simulate network communication
 System.out.println(
 "Process " + id + " sent request to Process " + receiverId
 );
 }
 // Simulate receiving a reply from another process
 private void waitForReply(int senderId) {
 // Simulate network communication (waiting for reply) 
  System.out.println(
 "Process " + id + " received reply from Process " + senderId
 );
 }
 // Enter the critical section
 private void enterCriticalSection() {
 System.out.println("Process " + id + " entered critical section.");
 try {
 // Simulate work in the critical section
 Thread.sleep(1000); // Simulate some work
 } catch (InterruptedException e) {
 e.printStackTrace();
 }
 // Leave critical section and release the resources
 leaveCriticalSection();
 }
 // Simulate leaving the critical section
 private void leaveCriticalSection() {
 System.out.println("Process " + id + " leaving critical section.");
 }
 // Main method to run the simulation
 public static void main(String[] args) {
 int numProcesses = 3; // Number of processes in the system
 List<RicartAgrawala> processes = new ArrayList<>();
 // Create processes
 for (int i = 0; i < numProcesses; i++) {
 processes.add(new RicartAgrawala(i, numProcesses));
 }
 // Simulate processes requesting the critical section
 for (RicartAgrawala process : processes) {
 new Thread(() -> process.requestCriticalSection()).start();
 }
 }
} 