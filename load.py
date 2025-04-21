import psutil
import threading
import time

def monitor_system_resources():
    num_cpus = psutil.cpu_count(logical=True)
    cpu_load = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    free_memory = memory.available / (1024 ** 2)  # in MB
    total_memory = memory.total / (1024 ** 2)  # in MB
    print(f"Available CPUs: {num_cpus}")
    print(f"CPU Load: {cpu_load:.1f}%")
    print(f"Free Memory: {free_memory:.2f} MB")
    print(f"Total Memory: {total_memory:.2f} MB")

class Task:
    def execute(self):
        time.sleep(1)  # Reduced from 5 to 1 second for quicker demonstration
        print(f"Task Executed on Thread: {threading.current_thread().name}")

class Worker(threading.Thread):
    def __init__(self, task):
        super().__init__()
        self.task = task
    
    def run(self):
        self.task.execute()

class TaskScheduler:
    def __init__(self, num_of_threads):
        self.num_of_threads = num_of_threads
        self.threads = []
    
    def schedule_task(self, task):
        worker = Worker(task)
        self.threads.append(worker)
        worker.start()
    
    def wait_for_completion(self):
        for thread in self.threads:
            thread.join()

class LoadBalancer:
    def __init__(self, num_of_threads):
        self.task_scheduler = TaskScheduler(num_of_threads)
    
    def distribute_tasks(self, tasks):
        for task in tasks:
            self.task_scheduler.schedule_task(task)
    
    def wait_for_all_tasks(self):
        self.task_scheduler.wait_for_completion()

def main():
    print("System Resources Before Task Scheduling:")
    monitor_system_resources()
    
    tasks = [Task() for _ in range(10)]
    load_balancer = LoadBalancer(num_of_threads=10)
    
    print("\nDistributing tasks...")
    load_balancer.distribute_tasks(tasks)
    load_balancer.wait_for_all_tasks()
    
    print("\nSystem Resources After Task Scheduling:")
    monitor_system_resources()

if __name__ == "__main__":
    main() 