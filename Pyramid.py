n=int(input("Enter Number: "))
w=len(" ".join([str(i)for i in list(range(n,0,-1))+list(range(2,n+1))]))
for i in range(1,n+1):print(" ".join([str(j)for j in list(range(i,0,-1))+list(range(2,i+1))]).center(w))
