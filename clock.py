import threading
import queue
import random
import time

class Node(threading.Thread):
    def __init__(self, node_id, coordinator_queue, adjustment_queue):
        super().__init__()
        self.node_id = node_id
        self.coordinator_queue = coordinator_queue
        self.adjustment_queue = adjustment_queue
        # Generate random time between 1000 and 3000
        self.local_time = random.randint(1000, 3000)

    def run(self):
        # Send local time to coordinator
        self.coordinator_queue.put((self.node_id, self.local_time))
        
        # Wait for adjustment
        adjustment = self.adjustment_queue.get()
        adjusted_time = self.local_time + adjustment
        
        print(f"Node {self.node_id} adjusted time from {self.local_time} to {adjusted_time:.1f}")

class Coordinator(threading.Thread):
    def __init__(self, num_nodes, coordinator_queue, adjustment_queue):
        super().__init__()
        self.num_nodes = num_nodes
        self.coordinator_queue = coordinator_queue
        self.adjustment_queue = adjustment_queue

    def run(self):
        node_times = []
        total_time = 0
        
        # Collect times from all nodes
        for _ in range(self.num_nodes):
            node_id, local_time = self.coordinator_queue.get()
            node_times.append((node_id, local_time))
            total_time += local_time

        # Calculate average time
        average_time = total_time / self.num_nodes
        print(f"Coordinator calculated average time: {average_time:.1f}")

        # Calculate and send adjustments to each node
        for node_id, local_time in sorted(node_times):
            adjustment = average_time - local_time
            print(f"Coordinator sending adjustment {adjustment:.1f} to Node {node_id}")
            self.adjustment_queue.put(adjustment)

def main():
    num_nodes = 5
    coordinator_queue = queue.Queue()
    adjustment_queue = queue.Queue()

    # Create and start coordinator
    coordinator = Coordinator(num_nodes, coordinator_queue, adjustment_queue)
    coordinator.start()

    # Create and start nodes
    nodes = []
    for i in range(num_nodes):
        node = Node(i, coordinator_queue, adjustment_queue)
        nodes.append(node)
        node.start()

    # Wait for all threads to complete
    for node in nodes:
        node.join()
    coordinator.join()

if __name__ == "__main__":
    main() 