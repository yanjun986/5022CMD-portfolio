import random
import time

from hash_table import HashTable
from product import Product

SIZES = [1_000, 5_000, 10_000, 50_000]   # number of products in each experiment
REPEATS = 1000                           # each search is repeated, then averaged


def array_search(array, pid):
    """Linear search: check every product from the start."""
    for p in array:
        if p.product_id == pid:
            return p
    return None


def time_hash_search(table, pid):
    """Average time (ns) for one hash table search."""
    start = time.perf_counter_ns()
    for _ in range(REPEATS):
        table.search(pid)
    end = time.perf_counter_ns()
    return (end - start) / REPEATS


def time_array_search(array, pid):
    """Average time (ns) for one array search."""
    start = time.perf_counter_ns()
    for _ in range(REPEATS):
        array_search(array, pid)
    end = time.perf_counter_ns()
    return (end - start) / REPEATS


def run_experiment(num_products):
    """Build both structures with the same products, then time 4 search cases."""
    ids = random.sample(range(100000, 999999), num_products)   # unique random IDs

    table = HashTable(11)        # starts small and grows automatically
    array = []

    # Put the SAME products into both structures.
    for i in range(num_products):
        p = Product(ids[i], f"Medicine {i + 1}", "Other", 10.00, 100, "2028-12-31", False)
        table.insert(p.product_id, p)
        array.append(p)          # add to the end of the list

    tests = [
        ("First product", ids[0]),                     # array best case
        ("Middle product", ids[num_products // 2]),    # array average case
        ("Last product", ids[-1]),                     # array worst case (found)
        ("Not found", 1),                              # array worst case (checks all)
    ]

    print(f"\n==== {num_products:,} products (hash table size {table.size:,}, "
          f"load factor {table.load_factor():.2f}) ====")
    print(f"{'Test case':<16}{'Hash Table (ns)':>18}{'Array (ns)':>18}{'Faster':>22}")
    print("-" * 74)
    for name, pid in tests:
        hash_time = time_hash_search(table, pid)
        array_time = time_array_search(array, pid)
        if hash_time < array_time:
            faster = f"Hash table ({array_time / hash_time:,.1f}x)"
        else:
            faster = f"Array ({hash_time / array_time:,.1f}x)"
        print(f"{name:<16}{hash_time:>18,.0f}{array_time:>18,.0f}{faster:>22}")


if __name__ == "__main__":
    random.seed(42)              # same IDs every run, so results can be repeated
    print("Search Performance: Hash Table vs Array")
    print(f"Each search repeated {REPEATS:,} times; times are the average for ONE search.")
    for n in SIZES:
        run_experiment(n)