class StackOverflowError(Exception):
    def __str__(self):
        return "Stack Overflow"
class StackUnderflowError(Exception):
    pass
class MyStack:
    def __init__(self, lim):
        self.lim = lim
        self.l = []
    def pop(self):
        if len(self.l)==0: raise StackUnderflowError
        return self.l.pop()
    def push(self, i):
        if len(self.l)==self.lim: raise StackOverflowError
        self.l.append(i)
ms = MyStack(2)
ms.push(1)
ms.push(2)
print(ms.pop())
print(ms.pop())
print(ms.pop())
