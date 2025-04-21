import threading
import time
from threading import Lock

class RicartAgrawala(threading.Thread):
    def __init__(self, process_id, num_processes):
        super().__init__()
        self.process_id = process_id
        self.num_processes = num_processes
        self.timestamp = 0
        self.lock = Lock()
        
    def request_critical_section(self):
        with self.lock:
            # Set timestamp for this request
            self.timestamp = int(time.time() * 1000000)  # Microsecond precision
            print(f"Process {self.process_id} requesting critical section at {self.timestamp}")
            
            # Send request to all other processes
            for i in range(self.num_processes):
                if i != self.process_id:
                    self.send_request(i)
            
            # Wait for replies from all other processes
            for i in range(self.num_processes):
                if i != self.process_id:
                    self.wait_for_reply(i)
            
            # Enter critical section
            self.enter_critical_section()
    
    def send_request(self, receiver_id):
        print(f"Process {self.process_id} sent request to Process {receiver_id}")
        
    def wait_for_reply(self, sender_id):
        print(f"Process {self.process_id} received reply from Process {sender_id}")
        
    def enter_critical_section(self):
        print(f"Process {self.process_id} entered critical section.")
        time.sleep(1)  # Simulate work in critical section
        self.leave_critical_section()
        
    def leave_critical_section(self):
        print(f"Process {self.process_id} leaving critical section.")
        
    def run(self):
        self.request_critical_section()

def main():
    num_processes = 3
    processes = []
    
    # Create processes
    for i in range(num_processes):
        process = RicartAgrawala(i, num_processes)
        processes.append(process)
    
    # Start processes
    for process in processes:
        process.start()
        time.sleep(0.5)  # Small delay between process starts for clearer output
    
    # Wait for all processes to complete
    for process in processes:
        process.join()

if __name__ == "__main__":
    main() 