#Howto compile and install LIBSVM manually

# Howto compile and install LIBSVM manually #
  1. Download the latest source code from http://www.csie.ntu.edu.tw/~cjlin/libsvm/ .
  1. The author used libsvm-3.0.tar.gz.
```
tar zxvf libsvm-3.0.tar.gz
cd libsvm-3.0
make
```
  1. Upon success, you'll get three executable files: svm-scale, svm-train and svm-predict.
  1. If you have the administrative privileges on the system, copy them to /usr/bin directory.
  1. Otherwise...
```
mkdir -p ~/usr/bin
cp svm-predict svm-scale svm-train ~/usr/bin
```
  1. Add the following line to your $HOME/.bashrc file:
```
export PATH=$HOME/usr/bin:$PATH
```
  1. Open a new terminal window or "source ~/.bashrc" then you should be able to run svm-train from anywhere line below:
```
[jdj@ghoti3 ~]$ svm-train 
Usage: svm-train [options] training_set_file [model_file]
options:
-s svm_type : set type of SVM (default 0)
	0 -- C-SVC
	1 -- nu-SVC
	2 -- one-class SVM
	3 -- epsilon-SVR
	4 -- nu-SVR
-t kernel_type : set type of kernel function (default 2)
	0 -- linear: u'*v
	1 -- polynomial: (gamma*u'*v + coef0)^degree
	2 -- radial basis function: exp(-gamma*|u-v|^2)
	3 -- sigmoid: tanh(gamma*u'*v + coef0)
	4 -- precomputed kernel (kernel values in training_set_file)
-d degree : set degree in kernel function (default 3)
-g gamma : set gamma in kernel function (default 1/num_features)
-r coef0 : set coef0 in kernel function (default 0)
-c cost : set the parameter C of C-SVC, epsilon-SVR, and nu-SVR (default 1)
-n nu : set the parameter nu of nu-SVC, one-class SVM, and nu-SVR (default 0.5)
-p epsilon : set the epsilon in loss function of epsilon-SVR (default 0.1)
-m cachesize : set cache memory size in MB (default 100)
-e epsilon : set tolerance of termination criterion (default 0.001)
-h shrinking : whether to use the shrinking heuristics, 0 or 1 (default 1)
-b probability_estimates : whether to train a SVC or SVR model for probability estimates, 0 or 1 (default 0)
-wi weight : set the parameter C of class i to weight*C, for C-SVC (default 1)
-v n: n-fold cross validation mode
-q : quiet mode (no outputs)
```