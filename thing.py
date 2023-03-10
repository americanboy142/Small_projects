# gram schmidt
# A = [a0,a1,...,a(n-1)]
# U[0] = a[0]
# e[0] = U[0]/two_norm(U[0])
# U[1] = a[1]-(a[1]*e[0])*e[0]
# e[1] = U[1]/two_norm(U[1])
# ...
# U[i] = a[i]-(a[i]*e[0])*e[0]-...-(a[i]*e[i-1])*e[i-1]
# e[i] = U[i]/two_norm(U[i])

# Gram_Schmidt(A)
# a is a column of A
# U is a vector
# e is a vector
# needs:
#   1) U_current = float
#      i) U on the ith iteration
#      ii) reset to 0 after each iteration
#   2) e_current = list
#      i) e on the ith iteration
#      ii) reset to [] after each iteration
#   3) e_stored
#      i) full list of columns of Q
#      ii) append with each e_current
#   4) Q
#      i) temp_matrix transposed
#   5) a_current
#      i) ith column of A
#      ii) reset to [] after each iteration
# output = Q = MAtrix => [e[0],e[1],...,e[n]]


# QR
# A = [a[0],a[1],...,a[n]] = [e[0],e[1],...,e[n]] * [[a[0]*e[0] , a[1]*e[0] ,..., a[n]*e[0]], 
#                                                    [[0]       , a[1]e[1] ,...,  a[n]e[1]],
#                                                    [[0]       ,     [0]  ,...,  a[n]e[2]]
#                                       * 0's till a[i][i]   
# QR(Q)
# Q matrix with columns e[i]
# output = (Q,R)
# Q from GS
# R = second matrix   
  
import numpy as np

def two_norm(U):
    return (sum(U[i]**2 for i in range(len(U))))**(1/2)

'''
U_partial
this caluculates each -(a[i]*e[k])*e[k]
Used to return ^, given a single e[k] and the a[i]
3/11/2023
'''
def U_partial(a_current,e_stored):
    multy = np.multiply(a_current,e_stored)
    summ = sum(multy)
    summ *= e_stored
    return(-summ)


def Gram_Schmidt(A,itteration = 0, e_stored = []):
    '''
    set each vector that needs to be reset each iteration
    np array and list
    list if it needs to be in the form [[v0],[v1],...[vn]]
    rest set as numpy array for vectorized calculations
    3/11/2023
    '''
    U_current = np.zeros(len(A))
    e_current = np.array([])
    a_current = np.array([])
    U_partial_vec = []
    
    '''
    stop condition
    3/11/2023
    '''
    if itteration == len(A):
        return np.transpose(e_stored)
    
    else:
        '''
        sets a[i] and the current column of A being used
        3/11/2023
        '''
        a_current = A[:,itteration]
        
        '''
        just skips for U1 since it equals a1 by def
        3/11/2023
        '''
        if itteration > 0:
            '''
            loops through the built columns of Q
            3/11/2023
            '''
            for e in e_stored:
                U_partial_vec.append(U_partial(a_current,e))
            for i in range(itteration):
                U_partial_np = np.array([])
                U_partial_np = np.append(U_partial_np,U_partial_vec[i])
                U_current += U_partial_np
        '''
        adds the a[i] to caculated U
        3/11/2023
        '''
        U_current += a_current

        two_norm_U = two_norm(U_current)

        '''
        normalizes U with two norm
        3/11/2023
        '''
        for i in range(len(U_current)):
            e_current = np.append(e_current,U_current[i]/two_norm_U)

        e_stored.append(e_current)

        return Gram_Schmidt(A , itteration + 1, e_stored)

'''
multiplies a which is row vector and e which is column vector
uses item by item multiply then sums
3/11/2023
'''
def QR_multiply(a,e):
    multiply = np.multiply(a,e)
    summ = sum(multiply)
    return summ


def QR(A,Q = [],itteration = 0,R = np.array([])):
    '''
    returns a zero matrix of size A
    on first itteration
    solves for Q using gram_schmidt
    3/11/2023
    '''
    if itteration == 0:
        Q = Gram_Schmidt(A)
        R = np.zeros((len(A),len(A)))
    '''
    stop condition
    3/11/2023
    '''
    if itteration == len(A):
        return (Q,R)
    else:
        '''
        sets the each item of R after r[ii] = to a[i]*e[j]
        3/11/2023
        '''
        for col in range(len(A)-itteration):
            R[itteration][col+itteration] = QR_multiply(A[:,col+itteration],Q[:,itteration])
        return QR(A,Q,itteration+1,R)

'''
function calls, formating, and testing
3/11/2023
'''
matrix = np.array([[1,1,0],[1,0,1],[0,1,1]])
np_Q,np_R = np.linalg.qr(matrix)

Q,R = QR(matrix)

print("My Q:\n",Q.round(3))
print("Numpy Q:\n", np_Q.round(3))

print("My R:\n",R.round(3))
print("Numpy R:\n", np_R.round(3))

# check
thing = np.matmul(Q,R)
print("My calculated Q x R:\n",thing.round(2))
deal = np.matmul(np_Q,np_R)
print("Numpy calculated Q x R:\n",deal.round(2))
                   