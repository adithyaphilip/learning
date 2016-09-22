mul = []
mod = 10**9 + 7
def get_val(num, pos):
    print(pos +1, mul[pos], num)
    return (mul[pos] * int(num) + (pos+1) * int(num))%mod

def main():
    line = input()
    n = len(line)
    mul.extend([0]*n)
    mul[-1] = 0
    for i in range(2,n+1):
        mul[-i] = (mul[-i+1] * 10 + 10)%mod

    dsum = 0
    for i in range(n):
        dsum+=get_val(line[i],i)
        dsum%=mod

    print(dsum, mul)

main()

