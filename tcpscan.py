import threading
import concurrent.futures
import socket 
import random
import sys
import time

start_num = 1
end_num = 1024
ports = list(range(start_num, end_num + 1))
random.shuffle(ports)

target_host = 'localhost'

lock = threading.Lock()
task_count = 0

def tcp_scan(host, port, thread_ids):
    global task_count
    with lock:
        thread_id = threading.get_ident()
        thread_ids.add(thread_id)
        task_count += 1
        task_number = task_count
    time.sleep(0.5)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return task_number, thread_id, port, True
        else:
            return task_number, thread_id, port, False
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()
    except socket.error:
        print("Couldn't connect to server.")
        sys.exit()

def main():
    num_threads = 10
    thread_ids = set()
    open_ports = []
    closed_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(tcp_scan, target_host, port, thread_ids) for port in ports]
        for future in concurrent.futures.as_completed(futures):
            task_number, thread_id, port, is_open = future.result()
            if is_open:
                open_ports.append(port)
            else:
                closed_ports.append(port)
            print(f"Task number {task_number}, Thread ID: {thread_id} has finished scanning port {port}.")

    print("\nUsed thread IDs:")
    print(', '.join(map(str, thread_ids)))

    print(f"\nTotal used thread IDs: {len(thread_ids)}")

    print("\nOpen ports:")
    print(', '.join(map(str, open_ports)))

    print("\nClosed ports:")
    print(', '.join(map(str, closed_ports)))

    print(f"\nTotal open ports: {len(open_ports)}")
    print(f"Total closed ports: {len(closed_ports)}")

if __name__ == "__main__":
    main()
