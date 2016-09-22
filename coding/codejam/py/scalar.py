for _ in range(int(input())):
    n = int(input()) 
    print("Case #",_+1,": ",sum([x*y for x,y in zip(sorted((map(int, input().split()))), sorted((map(int, input().split())), reverse=True))]), sep="")
        
