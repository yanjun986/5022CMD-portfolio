def fibonacci(n):
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    print("=== TEST: known Fibonacci values ===")
    for n, expected in [(0, 0), (1, 1), (2, 1), (10, 55), (30, 832040)]:
        result = fibonacci(n)
        status = "OK" if result == expected else "WRONG"
        print(f"  fibonacci({n:>2}) = {result:>7,}  (expected {expected:,})  {status}")