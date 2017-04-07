from MKLpy.algorithms.EasyMKL1 import EasyMKL as easy
from MKLpy.algorithms import EasyMKL as old
from MKLpy.lists import HPK_generator
from sklearn.datasets import load_digits
import numpy as np
from sklearn.model_selection import train_test_split as tts
from numpy.testing    import assert_array_equal, assert_array_almost_equal, assert_equal
import sys
from sklearn.svm import SVC

data = load_digits()
X,Y = data.data,data.target
Y = [1 if y==Y[0] else -1 for y in Y]
Xtr,Xte,Ytr,Yte = tts(X,Y,train_size=200)
KL = HPK_generator(Xtr).make_a_list(10).to_array()
KLte = HPK_generator(Xtr,Xte).make_a_list(10).to_array()


clf_new = easy(lam=0,kernel='precomputed')
clf_old = old (lam=0,kernel='precomputed',tracenorm=False)
K_new = clf_new.arrange_kernel(KL,Ytr)
K_old = clf_old.arrange_kernel(KL,Ytr)

assert_array_almost_equal(K_new,K_old)


clf_new = easy(lam=0,kernel='precomputed').fit(KL,Ytr)
clf_old = old (lam=0,kernel='precomputed',tracenorm=False).fit(KL,Ytr)
y_new = clf_new.decision_function(KLte)
y_old = clf_old.decision_function(KLte)

assert_array_almost_equal(y_new,y_old)


#check with SVM
clf_new = easy(lam=0,base = SVC(C=10)).fit(KL,Ytr)
clf_old = easy(lam=0,kernel='precomputed',tracenorm=False)
y_new = clf_new.decision_function(KLte)
KK = clf_old.arrange_kernel(KL,Ytr)
clf = SVC(C=10,kernel='precomputed').fit(KK,Ytr)
KKte = clf_old.how_to(KLte,clf_old.weights)
y_old = clf.decision_function(KKte)

assert_array_almost_equal(y_new,y_old)


