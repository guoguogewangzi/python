import mxmul
nrow ,nk,ncol = 5,3, 5
A = [[y for y in range(nk)] for x in range(nrow)]
B = [[y for y in range(ncol)]  for x in range(nk)]
C = mxmul.mxmul(A,B,nrow,nk,ncol)

print(C)
