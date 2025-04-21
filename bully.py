import random
import time
import threading
from typing import List

class Node:
    def __init__(self, node_id: int, total_nodes: int):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.is_leader = False
        self.is_active = True
        self.election_in_progress = False

    def start_election(self):
        if not self.is_active:
            print(f"Node {self.node_id} is inactive.")
            return
            
        print(f"Node {self.node_id} started the election.")
        # Notify all nodes with higher IDs
        for i in range(self.node_id + 1, self.total_nodes):
            print(f"Node {self.node_id} sends 'election' message to Node {i}.")
            
        time.sleep(1)  # Fixed delay for better readability
        self.election_response()

    def election_response(self):
        if self.election_in_progress:
            return
            
        self.election_in_progress = True
        higher_nodes = list(range(self.node_id + 1, self.total_nodes))
        
        if higher_nodes:
            print(f"Node {self.node_id} receives election message. Sending reply.")
            time.sleep(1)  # Fixed delay for better readability
            next_node = higher_nodes[0]  # Always choose next higher node for consistent output
            print(f"Node {self.node_id} started new election as higher node responds.")
            Node(next_node, self.total_nodes).start_election()
        else:
            print(f"Node {self.node_id} wins the election and becomes the leader.")
            self.is_leader = True
            for i in range(self.total_nodes):
                if i != self.node_id:
                    print(f"Node {self.node_id} sends 'victory' message to Node {i}.")
            Election.stop_election()

    def crash(self):
        self.is_active = False
        print(f"Node {self.node_id} crashed and is inactive.")

    def recover(self):
        self.is_active = True
        print(f"Node {self.node_id} recovered and is active.")

class Election:
    leader_elected = False
    lock = threading.Lock()

    @classmethod
    def stop_election(cls):
        with cls.lock:
            cls.leader_elected = True

    @classmethod
    def is_leader_elected(cls) -> bool:
        with cls.lock:
            return cls.leader_elected

    @staticmethod
    def election_process(nodes: List[Node]):
        # Start with Node 0 for consistent output
        nodes[0].start_election()
        while not Election.is_leader_elected():
            time.sleep(1)

def main():
    total_nodes = 5
    nodes = [Node(i, total_nodes) for i in range(total_nodes)]
    
    # Start election process in a separate thread
    election_thread = threading.Thread(target=Election.election_process, args=(nodes,))
    election_thread.start()
    
    # Wait for election to complete
    election_thread.join()

if __name__ == "__main__":
    main() 