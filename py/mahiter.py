class fib:
    def __init__(self, n):
        self.n = n
        self.a = 0
        self.b = 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.a <= self.n:
            t = self.a
            self.a = self.b
            self.b = self.b + t
            return t
        raise StopIteration
for i in fib(30):
    print(i)
