import time
import threading

list_of_results = []  # Global list to store results from threads

def count_to_five():
    for count in range(1, 6):
        print(count)

        with threading.Lock():  # Ensure thread-safe access to the global list
            list_of_results.append(count)  # Store the count in the global list
        
        time.sleep(1)  # Pause for 1 second between counts


def main():
    t1 = threading.Thread(target=count_to_five)
    t1.daemon = True  # Set the thread as a daemon thread
    t2 = threading.Thread(target=count_to_five)
    t2.daemon = True  # Set the thread as a daemon thread

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Results are : {list_of_results}")
    print("Exiting the MAIN thread")

if __name__ == "__main__":
    main()