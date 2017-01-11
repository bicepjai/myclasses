import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import random

from sklearn import svm
from sklearn.cluster import KMeans

features_train = np.loadtxt("data/features.train")
features_test  = np.loadtxt("data/features.test")
R_train,C_train = features_train.shape
R_test,C_test = features_test.shape

print("==========================")
print("problem 11")
    
# plotting the points
r_xs = [1,0,0]
r_ys = [0,1,-1]
l_xs  = [-1,0,0,-2]
l_ys  = [0,2,-2,0]
#plt.plot(r_xs, r_ys, 'bs')
#plt.plot(l_xs, l_ys, 'rs')
#plt.axis([-3, 3, -3, 3])
#plt.show()


zr_xs = [ x2**2 - 2*x1 - 1 for (x1,x2) in [(1, 0), (0, 1), (0, -1)]]
zr_ys = [ x1**2 - 2*x2 + 1 for (x1,x2) in [(1, 0), (0, 1), (0, -1)]]
zl_xs  = [ x2**2 - 2*x1 - 1 for (x1,x2) in list(zip(l_xs,l_ys))]
zl_ys  = [ x1**2 - 2*x2 + 1 for (x1,x2) in list(zip(l_xs,l_ys))]
#plt.plot(zr_xs, zr_ys, 'bs')
#plt.plot(zl_xs, zl_ys, 'rs')
#plt.axis([-6, 6, -6, 6])
#plt.show()

print("==========================")
print("problem 13")

N = 100
f_x = lambda X: np.sign(X[:,1] - X[:,0] + 0.25*np.sin(np.pi*X[:,0]))
runs = 1000
C = 1
gamma = 1.5

nof_0_e_ins = 0
for run in range(runs):
    X_in = np.ones((N,2))
    X_in[:,0] = np.random.uniform(-1,1,N)
    X_in[:,1] = np.random.uniform(-1,1,N)
    Y_in = f_x(X_in)
    # Y_in.shape = (N,1)
    
    #svm rbf
    model_svm = svm.SVC(kernel='rbf',gamma=gamma, C=C)
    model_svm.fit(X_in,Y_in)
    # predicting SVM
    Y_svm_in = model_svm.predict(X_in)
    p_in_svm  = np.mean((Y_svm_in != Y_in).astype(int))
    
    if(p_in_svm == 0):
        nof_0_e_ins += 1

print("nof_0_e_ins %:",nof_0_e_ins*100/1000)

# hypothesis for problems 14 thru 18
f_x = lambda X: np.sign(X[:,1] - X[:,0] + 0.25*np.sin(np.pi*X[:,0]))

def kmeans_rbf_lloyd(X,Y,k,gamma):
    R,C = X.shape
    uks_idx = np.random.randint(R, size=k)
    uks = X[uks_idx]

    iters = 0
    converged = False
    while( not converged ):

        iters += 1
        
        # forming sks
        min_obj_l = []
        for i in range(k):
            wrt_uki = np.square(np.linalg.norm(uks[i] - X,axis=1))
            min_obj_l.append(wrt_uki)
        min_obj = np.column_stack(min_obj_l)
        sks = np.argmin(min_obj, axis=1)
        
        #check for empty cluster
        empty_cluster = []
        for i in range(k):
            if(len(sks[sks[:] == i]) == 0):
                empty_cluster.append(False)
            else:
                empty_cluster.append(True)
        if(not all(empty_cluster)):
            uks_idx = np.random.randint(R, size=k)
            uks = X[uks_idx]
            continue
        
        # forming uks
        uks_l = []
        for i in range(k):
            uks_l.append(np.mean(X[sks[:] == i],axis=0))

        # convergence check            
        prev_uks = uks
        uks = np.vstack(uks_l)
        converged = np.allclose(prev_uks,uks,1e-10)
        
        if(iters > 1000):
            print("iters exceeded 1000")
            break
    
    # print("iters",iters)
    
    # finding ws
    rdf_uki_l = [np.ones(R)]
    for i in range(k):
        wrt_uki = np.exp(-gamma*np.square(np.linalg.norm(uks[i] - X,axis=1)))
        rdf_uki_l.append(wrt_uki)
    phi = np.column_stack(rdf_uki_l)
    
    phi_dagger=np.dot(np.linalg.pinv(np.dot(phi.T,phi)),phi.T)
    w = np.dot(phi_dagger,Y)
    
    return uks,w

def kernel_vs_regular(N, runs, K, gamma):
    kernel_beat_regular = 0
    p_ins_kernel = []
    p_ins_regular = []
    p_outs_kernel = []
    p_outs_regular = []

    for run in range(runs):
    
        # seperable data points
        X_in = np.ones((N,2))
        X_in[:,0] = np.random.uniform(-1,1,N)
        X_in[:,1] = np.random.uniform(-1,1,N)
        Y_in = f_x(X_in)    
        while(np.all(Y_in==1) or np.all(Y_in==-1)):
            X_in = np.ones((N,2))
            X_in[:,0] = np.random.uniform(-1,1,N)
            X_in[:,1] = np.random.uniform(-1,1,N)
            Y_in = f_x(X_in)

        X_out = np.ones((N,2))
        X_out[:,0] = np.random.uniform(-1,1,N)
        X_out[:,1] = np.random.uniform(-1,1,N)
        Y_out = f_x(X_out) 
        
        # k means clustering rbf lloyds regular form
        uks,w = kmeans_rbf_lloyd(X_in,Y_in,K,gamma)
        # predicting kmeans Ein
        hx_sum = np.zeros(N)
        for i in range(K):
            hx_uki_wi = w[i+1] * np.exp(-gamma*np.linalg.norm(uks[i] - X_in,axis=1))
            hx_sum  = hx_sum + hx_uki_wi
        g_of_xin = np.sign(hx_sum + w[0]*np.ones(N))
        p_in_kmeans  = np.mean((g_of_xin != Y_in).astype(int))
        p_ins_regular.append(p_in_kmeans)
        
        # predicting kmeans Eout
        hx_sum = np.zeros(N)
        for i in range(K):
            hx_uki_wi = w[i+1] * np.exp(-gamma*np.linalg.norm(uks[i] - X_out,axis=1))
            hx_sum  = hx_sum + hx_uki_wi
        g_of_xout = np.sign(hx_sum + w[0]*np.ones(N))
        p_out_kmeans  = np.mean((g_of_xout != Y_out).astype(int))
        p_outs_regular.append(p_out_kmeans)

        #svm rbf kernel form
        model_svm = svm.SVC(kernel='rbf',gamma=gamma, C=C)
        model_svm.fit(X_in,Y_in)
        # predicting SVM Ein
        Y_svm_in = model_svm.predict(X_in)
        p_in_svm  = np.mean((Y_svm_in != Y_in).astype(int))
        p_ins_kernel.append(p_in_svm)

        # predicting SVM Eout
        Y_svm_out = model_svm.predict(X_out)
        p_out_svm  = np.mean((Y_svm_out != Y_out).astype(int))
        p_outs_kernel.append(p_out_svm)

        if(p_in_kmeans > p_in_svm):
            kernel_beat_regular += 1
        
        #print("p_in_svm_rbf:",p_in_svm,"p_in_kmeans:",p_in_kmeans)
        #print("p_out_svm_rbf:",p_out_svm,"p_out_kmeans:",p_out_kmeans)
    
    print("kernel_beat_regular",kernel_beat_regular)
    return p_ins_regular,p_outs_regular,p_ins_kernel,p_outs_kernel


print("==========================")
print("problem 14")

N = 100
runs = 100
K = 9
gamma = 1.5
p_ins_regular,p_outs_regular,p_ins_kernel,p_outs_kernel = kernel_vs_regular(N, runs, K, gamma)

print("==========================")
print("problem 15")
N = 100
runs = 100
K = 12
gamma = 1.5
p_ins_regular,p_outs_regular,p_ins_kernel,p_outs_kernel = kernel_vs_regular(N, runs, K, gamma)

print("==========================")
print("problem 16")
N = 100
runs = 100
K = 9
gamma = 1.5

print("K",K)
p_ins_regular,p_outs_regular,p_ins_kernel,p_outs_kernel = kernel_vs_regular(N, runs, K, gamma)
print("p_ins_regular",np.mean(p_ins_regular))
print("p_outs_regular",np.mean(p_outs_regular))
print("p_ins_kernel",np.mean(p_ins_kernel))
print("p_outs_kernel",np.mean(p_outs_kernel))

K = 12
print("K",K)
p_ins_regular,p_outs_regular,p_ins_kernel,p_outs_kernel = kernel_vs_regular(N, runs, K, gamma)
print("p_ins_regular",np.mean(p_ins_regular))
print("p_outs_regular",np.mean(p_outs_regular))
print("p_ins_kernel",np.mean(p_ins_kernel))
print("p_outs_kernel",np.mean(p_outs_kernel))

print("==========================")
print("problem 17")
N = 100
runs = 100
K = 9
gamma = 1.5
print("gamma",gamma)
p_ins_regular,p_outs_regular,p_ins_kernel,p_outs_kernel = kernel_vs_regular(N, runs, K, gamma)
print("p_ins_regular",np.mean(p_ins_regular))
print("p_outs_regular",np.mean(p_outs_regular))
print("p_ins_kernel",np.mean(p_ins_kernel))
print("p_outs_kernel",np.mean(p_outs_kernel))

gamma = 2
print("gamma",gamma)
p_ins_regular,p_outs_regular,p_ins_kernel,p_outs_kernel = kernel_vs_regular(N, runs, K, gamma)
print("p_ins_regular",np.mean(p_ins_regular))
print("p_outs_regular",np.mean(p_outs_regular))
print("p_ins_kernel",np.mean(p_ins_kernel))
print("p_outs_kernel",np.mean(p_outs_kernel))

print("==========================")
print("problem 18")
N = 100
runs = 100
K = 9
gamma = 1.5

p_ins_regular,p_outs_regular,p_ins_kernel,p_outs_kernel = kernel_vs_regular(N, runs, K, gamma)
print("Ein=0 in p_ins_regular",sum(p == 0.0 for p in p_ins_regular))

