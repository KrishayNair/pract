import threading
import queue
import time
import random

class Process(threading.Thread):
    def __init__(self, process_id, token_queue, request_queues, max_requests):
        super().__init__()
        self.process_id = process_id
        self.token_queue = token_queue
        self.request_queues = request_queues
        self.has_token = False
        self.parent = None
        self.max_requests = max_requests
        self.requests_made = 0
        self.running = True
        
    def set_parent(self, parent_id):
        self.parent = parent_id
        
    def request_critical_section(self):
        if self.requests_made >= self.max_requests:
            self.running = False
            return
            
        print(f"Process {self.process_id} is requesting the critical section.")
        if not self.has_token and self.parent is not None:
            # Send request to parent
            self.request_queues[self.parent].put(self.process_id)
            # Wait for token
            self.token_queue.get()
            self.has_token = True
            print(f"Process {self.process_id} received the token.")
        
        print(f"Process {self.process_id} is entering the critical section.")
        time.sleep(1)  # Critical section
        print(f"Process {self.process_id} is releasing the critical section.")
        self.requests_made += 1
        
        # Pass token to next requesting process if any
        while not all(q.empty() for q in self.request_queues):
            for i, q in enumerate(self.request_queues):
                if not q.empty():
                    requester = q.get()
                    print(f"Process {self.process_id} is passing the token to Process {requester}.")
                    self.has_token = False
                    self.token_queue.put(True)
                    break
    
    def run(self):
        while self.running:
            # Randomly decide to request critical section
            if random.random() < 0.3:  # 30% chance to request
                self.request_critical_section()
            time.sleep(random.uniform(0.5, 2))

def main():
    num_processes = 5
    max_requests = 2  # Each process will make at most 2 requests
    token_queue = queue.Queue()
    request_queues = [queue.Queue() for _ in range(num_processes)]
    
    # Create processes
    processes = []
    for i in range(num_processes):
        p = Process(i + 1, token_queue, request_queues, max_requests)
        processes.append(p)
    
    # Set up tree structure (1 is root, has token initially)
    processes[0].has_token = True  # Process 1 has token
    processes[1].set_parent(1)     # Process 2's parent is 1
    processes[2].set_parent(1)     # Process 3's parent is 1
    processes[3].set_parent(2)     # Process 4's parent is 2
    processes[4].set_parent(2)     # Process 5's parent is 2
    
    # Start processes
    for p in processes:
        p.start()
    
    # Wait for all processes to finish
    for p in processes:
        p.join()
    
    print("Simulation completed.")

if __name__ == "__main__":
    main() 