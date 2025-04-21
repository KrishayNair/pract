class Process:
    def __init__(self, id):
        self.id = id
        self.next_process = None
        self.is_leader = False

    def send_election_message(self):
        print(f"Process {self.id} sends election message to Process {self.next_process.id}")
        self.next_process.receive_election_message(self.id)

    def receive_election_message(self, sender_id):
        if sender_id > self.id:
            # Forward the message to next process
            print(f"Process {self.id} forwards election message to Process {self.next_process.id}")
            self.next_process.receive_election_message(sender_id)
        elif sender_id < self.id:
            # Pass message with current process ID
            print(f"Process {self.id} passes the message with its ID {self.id}")
            self.next_process.receive_election_message(self.id)
        else:
            # This process is the leader
            self.is_leader = True
            print(f"Process {self.id} is elected as the leader.")

def main():
    # Create processes
    processes = [Process(i) for i in range(1, 6)]  # Create processes 1 to 5
    
    # Connect processes in a ring
    for i in range(len(processes)):
        processes[i].next_process = processes[(i + 1) % len(processes)]
    
    # Start election
    print("Starting the election...")
    processes[0].send_election_message()  # Process 1 starts the election

if __name__ == "__main__":
    main() 