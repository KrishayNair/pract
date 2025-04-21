import java.util.*;
class RingElection {
 static class Process {
 int id; // Process ID
 Process nextProcess; // Next process in the ring
 boolean isLeader = false;
 public Process(int id) {
 this.id = id;
 }
 // Send election message to the next process
 public void sendElectionMessage() {
 System.out.println("Process " + id + " sends election message to Process " +
nextProcess.id);
 nextProcess.receiveElectionMessage(this.id);
 }
 // Receive election message and forward it if necessary
 public void receiveElectionMessage(int senderId) {
 if (senderId > this.id) {
 // Forward the message to the next process
 System.out.println("Process " + id + " forwards election message to Process " +
nextProcess.id);
 nextProcess.receiveElectionMessage(senderId);
 } else if (senderId < this.id) {
 // If the received ID is smaller, pass the message with the current process ID
 System.out.println("Process " + id + " passes the message with its ID " + id);
 nextProcess.receiveElectionMessage(id);
 } else {
 // If senderId == current process ID, this process is the leader
 this.isLeader = true;
 System.out.println("Process " + id + " is elected as the leader.");
 }
 }
 }
 public static void main(String[] args) { 
 // Create a list of processes with unique IDs
 List<Process> processes = new ArrayList<>();
 int numberOfProcesses = 5;
 // Initialize processes
 for (int i = 0; i < numberOfProcesses; i++) {
 processes.add(new Process(i + 1)); // Process IDs start from 1
 }
 // Connect processes in a ring (circular linked list)
 for (int i = 0; i < numberOfProcesses; i++) {
 processes.get(i).nextProcess = processes.get((i + 1) % numberOfProcesses);
 }
 // Start election from a random process (let's start from Process 1)
 System.out.println("\nStarting the election...");
 processes.get(0).sendElectionMessage(); // Process 1 starts the election
 }
} 
   