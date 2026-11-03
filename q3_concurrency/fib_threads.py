"""
Q3: calculate fibonacci(35), fibonacci(38) and fibonacci(40)
  (A) WITH multithreading - one thread per number
  (B) WITHOUT multithreading - one after another
Each is repeated for several rounds and timed in nanoseconds.
"""
import statistics
import sys
import threading
import time

from fib import fibonacci

NUMBERS = (35, 38, 40)
ROUNDS = 10
EXPECTED = {35: 9227465, 38: 39088169, 40: 102334155}   # used to check every answer


def worker(n, results, times, lock):
    """Runs inside one thread: calculate fibonacci(n) and record when it started and ended."""
    start = time.perf_counter_ns()
    value = fibonacci(n)
    end = time.perf_counter_ns()
    # Several threads write to the same dictionaries. The lock lets only one
    # thread write at a time, so no result is lost or half-written.
    with lock:
        results[n] = value
        times[n] = (start, end)


def run_with_threads():
    """One round: 3 threads, one per number. Returns (time in ns, results)."""
    results, times, lock = {}, {}, threading.Lock()
    threads = [threading.Thread(target=worker, args=(n, results, times, lock)) for n in NUMBERS]
    for t in threads:
        t.start()                 # all 3 threads begin
    for t in threads:
        t.join()                  # wait until every thread has finished
    first_start = min(start for start, _ in times.values())
    last_end = max(end for _, end in times.values())
    return last_end - first_start, results      # T = last thread finished - first thread started


def run_without_threads():
    """One round: the same 3 numbers, one after another, in the main thread."""
    start = time.perf_counter_ns()
    results = {n: fibonacci(n) for n in NUMBERS}
    end = time.perf_counter_ns()
    return end - start, results


def print_table(title, times):
    """Print each round's time, then the total, average and median."""
    print(f"\n{title}")
    print(f"{'Round':>6} | {'Time taken T (ns)':>20} | {'T (seconds)':>11}")
    print("-" * 45)
    for r, t in enumerate(times, start=1):
        print(f"{r:>6} | {t:>20,} | {t / 1e9:>11.3f}")
    average = sum(times) / len(times)
    median = statistics.median(times)
    print("-" * 45)
    print(f"{'Total':>6} | {sum(times):>20,} | {sum(times) / 1e9:>11.3f}")
    print(f"{'Avg':>6} | {average:>20,.0f} | {average / 1e9:>11.3f}")
    print(f"{'Median':>6} | {median:>20,.0f} | {median / 1e9:>11.3f}")
    return average, median


def main():
    gil = getattr(sys, "_is_gil_enabled", lambda: True)()
    print(f"Python {sys.version.split()[0]} | GIL enabled: {gil}")
    print(f"Calculating fibonacci{NUMBERS} for {ROUNDS} rounds each (this takes a few minutes)")
    print("Each round runs (A) then (B) back to back, so any slowdown of the")
    print("computer affects both experiments equally.\n")

    with_threads, without_threads = [], []
    for r in range(1, ROUNDS + 1):
        for run_one_round, store in ((run_with_threads, with_threads),
                                     (run_without_threads, without_threads)):
            t, results = run_one_round()
            if results != EXPECTED:
                print("  WARNING: a Fibonacci result was wrong!")
            store.append(t)
        print(f"  Round {r:>2}: with threads {with_threads[-1] / 1e9:.3f} s | "
              f"without threads {without_threads[-1] / 1e9:.3f} s")

    avg_a, med_a = print_table("(A) WITH multithreading (3 threads)", with_threads)
    avg_b, med_b = print_table("(B) WITHOUT multithreading", without_threads)

    print("\n=== SUMMARY ===")
    print(f"  Average WITH threads    : {avg_a:>16,.0f} ns ({avg_a / 1e9:.3f} s)")
    print(f"  Average WITHOUT threads : {avg_b:>16,.0f} ns ({avg_b / 1e9:.3f} s)")
    print(f"  Median  WITH threads    : {med_a:>16,.0f} ns ({med_a / 1e9:.3f} s)")
    print(f"  Median  WITHOUT threads : {med_b:>16,.0f} ns ({med_b / 1e9:.3f} s)")
    diff = (avg_a - avg_b) / avg_b * 100
    print(f"  On average, multithreading was {abs(diff):.1f}% {'slower' if diff > 0 else 'faster'}.")


if __name__ == "__main__":
    main()