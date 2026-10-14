def fibonacci(n):
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(10))   # should print 55
print(fibonacci(30))   # should print 832040