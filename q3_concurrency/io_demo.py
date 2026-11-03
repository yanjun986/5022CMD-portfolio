"""
Each task simulates an I/O-bound job, such as downloading a file, by waiting
with time.sleep(). While a thread is waiting it releases the GIL, so the other
threads can run, and the waiting times overlap.
"""
import threading
import time

TASKS = 5          # number of "downloads"
WAIT = 1.0         # seconds each download spends waiting


def download(task_id):
    """Pretend to download a file: just wait, like waiting for a network reply."""
    time.sleep(WAIT)


def run_without_threads():
    """All downloads one after another."""
    start = time.perf_counter_ns()
    for i in range(TASKS):
        download(i)
    return time.perf_counter_ns() - start


def run_with_threads():
    """One thread per download, all waiting at the same time."""
    threads = [threading.Thread(target=download, args=(i,)) for i in range(TASKS)]
    start = time.perf_counter_ns()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter_ns() - start


def main():
    print(f"I/O-bound demo: {TASKS} downloads that each wait {WAIT:.1f} s\n")
    without = run_without_threads()
    with_threads = run_with_threads()
    print(f"  WITHOUT threads : {without:>15,} ns ({without / 1e9:.2f} s)")
    print(f"  WITH threads    : {with_threads:>15,} ns ({with_threads / 1e9:.2f} s)")
    print(f"  Multithreading was {without / with_threads:.1f}x faster for this I/O-bound task.")


if __name__ == "__main__":
    main()