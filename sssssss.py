n = int(input())
w = len(" ".join(map(str, list(range(n,0,-1))+list(range(2,n+1)))))
for i in range(1,n+1):
    s = list(map(str, range(1,i+1)))
    print(" ".join(s[1:][::-1]+s).center(w))
