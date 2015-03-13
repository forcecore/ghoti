# Do I have to be a Linux expert? #
This installation document assumes that you are familiar with the following:
  * Basic Linux commands such as tar (for Archiving/Unarchiving), cp, mv, etc.
  * Environment variables (Knowing what $HOME is would be sufficient)
  * Howto install/remove packages in your Linux environment

# Preparing Linux Machine #
The extractor WAS designed to be run on both Windows and Linux. However, setting up Python, OpenCV, Gnuplot, etc is a quite painful job to be done on Windows. We gave up support on Windows, although not impossible. If you don't have an up-to-date Linux environment available, we suggest using WUBI installer to run Ubuntu Linux on your Windows PC.

## Selecting Linux Distribution ##
There are many distributions of Linux available. The author is using Arch Linux, and this document is based on Ubuntu Linux(10.10) which is compatible with Debian Linux, because Ubuntu is popular and easy to use. It is also easier to follow this installation instruction on Ubuntu/Debian.
  * **Throughout the manual, we denote Ubuntu/Mint and other Debian based distributions as "Debian"**.

## WUBI ##
WUBI can install Ubuntu Linux as a /file/ on your Windows machine: no need to partition your hard disks! Please refer [WubiGuide](https://wiki.ubuntu.com/WubiGuide) for details.

## Virtualization ##
Virtualization softwares such as Virtual Box/VMWare and others allows Linux OS to be run in parallel with Windows OS. Linux is run as an APPLICATION, allowing you to run Linux along with your other favorite programs on Windows. However, this requires some computing power. If you happen to have Dual Core PC with 2GB RAM or more, it should be enough. Both Virtual Box and VMWare have free versions.



# Preparing Environment #
Once you have a Linux up and running, you need to prepare environment for our programs to run.


## Development Environment ##
  * On Debian, **build-essential** package is enough.
  * On Arch Linux, **base-devel** is enough.


## Mercurial ##
  * To _check out_ the project files, you need to install **mercurial** package (on both Arch and Debian).


## Python 2 ##
This is where the problem begins. The extractor program uses Python 2 whereas some Linux distributions use Python 3 as their default Python interpretor. You might need to compile and manually install Python 2.6/2.7 in the future.


### For Arch Linux ###
Arch Linux currently uses Python 3 as its default Python interpretor. To run the extractor, **Python2** package is required. PIL(**python-imaging**), Numeric(**python-numeric**) packages are also required. python-numeric is available in AUR.


### For Debian ###
  * Install **python-imaging** for PIL, **python-numeric** for Numeric.
  * As of 2011-01-11, Python 2 is the default Python interpretor for Debian.
  * However, scripts from ghoti requires that Python 2 is /usr/bin/python2.
  * If you have administrative privileges on the Linux machine, do:
```
# ln -s /usr/bin/python /usr/bin/python2
```
  * or, if you haven't, you need to modify the first line in the scripts:
```
#!/usr/bin/python2
```
  * to:
```
#!/usr/bin/python
```
  * or in some scripts,
```
#!/usr/bin/env python2
```
  * to
```
#!/usr/bin/env python
```



## OpenCV 1.0 ##
Like Python 2, OpenCV is another problem. At the time of development, OpenCV 2.0 was not mature enough, hence we decided to use OpenCV 1.0 instead. It is likely that in the future, OpenCV 1.0 should be compiled manually, and it is already true for Arch Linux.


### Arch Linux ###
  * On Arch Linux, OpenCV 2.2 is the default provided by the packages. Please refer [Compiling\_OpenCV](Compiling_OpenCV.md) to install OpenCV 1.0 manually.


### Debian ###
  * On Debian, as of 2011-01-11, OpenCV packages would be OpenCV 1.0: install **python-opencv** package.
  * Otherwise, see [Compiling\_OpenCV](Compiling_OpenCV.md) to manually compile OpenCV 1.0.


## LIBSVM ##
We used LIBSVM (http://www.csie.ntu.edu.tw/~cjlin/libsvm/) for SVM, rather than implementing them by ourselves. LIBSVM should be installed to do the training/prediction with the extracted vectors.
  * On Arch Linux, **libsvm** is available from the AUR.
    * As of 2011-01-11, it is broken. See [Compiling\_LIBSVM](Compiling_LIBSVM.md) to manually compile and install LIBSVM.
  * On Debian, install **libsvm-tools**.



# Installation #
  1. Download the newest version of Ghoti program:
```
hg clone https://ghoti.googlecode.com/hg/ ghoti 
```
  1. A new directory "ghoti" will be created.
  1. Now, type
```
cd ghoti
pwd
```
  1. You'll see something like this printed on screen:
```
jdj@ghoti3:~/ghoti$ pwd
/home/jdj/ghoti
```
  1. From now on, when we say $GHOTI, it should be replaced with /home/jdj/ghoti.
  1. jdj is author's ID on the Linux machine, so it would be different from yours.

# Running the Extractor #
  1. Download [sample](http://code.google.com/p/ghoti/downloads/detail?name=sample_set.zip) images so that the Extractor can be run.
  1. Move all the pictures into $GHOTI/extractor/in directory, or you may use _[soft links](http://en.wikipedia.org/wiki/Symbolic_link)_.
  1. cd to $GHOTI/extractor
  1. Try running the extractor with following command:
```
./ghoti.py
```
  1. If you are running Debian and installed all the packages mentioned above, you would see no error.
  1. You might see an error message complaining about OpenCV:
```
[jdj@ghoti3 extractor]$ ./ghoti.py 
Traceback (most recent call last):
  File "./ghoti.py", line 12, in <module>
    from opencv.cv import *
ImportError: No module named opencv.cv
```
  1. To fix this, edit $GHOTI/extractor/path.sh:
```
#!/bin/bash
# usage: source this script...
# e.g $ source path.sh
CWD=`pwd`
export PYTHONPATH=$CWD:/usr/lib/python2.7:$HOME/usr/opencv/lib/python2.7/site-packages
```
  1. The directories are separated by colons. Make sure that directories /usr/lib/python2.7 and $HOME/usr/opencv/lib/python2.7/site-packages are correct. For your configuration, it might be $HOME/usr/opencv/lib/python2.6/site-packages or alike.
  1. Source the path.sh
```
source path.sh
```
  1. If you don't want to do the "source path.sh" every time, you can add the following line to your $HOME/.bashrc:
```
source $GHOTI/extractor/path.sh
```
  1. After this, ghoti.py should run, or emit some other error, on PIL.
```
[jdj@ghoti3 extractor]$ ./ghoti.py 
Traceback (most recent call last):
  File "./ghoti.py", line 14, in <module>
    import opencv.adaptors # must install python-numeric package (Ubuntu/Debian) first, and maybe python-numpy.
  File "/home/jdj/usr/opencv/lib/python2.7/site-packages/opencv/adaptors.py", line 64, in <module>
    import PIL
ImportError: No module named PIL
```
  1. On Arch Linux and Debian, install package **python-imaging**.
  1. Another error is that you would need python-numeric. On Arch linux, you need **python-numeric** from AUR and on Debian, it is also called **python-numeric**.
```
[jdj@ghoti3 extractor]$ ./ghoti.py 
Traceback (most recent call last):
  File "./ghoti.py", line 14, in <module>
    import opencv.adaptors # must install python-numeric package (Ubuntu/Debian) first, and maybe python-numpy.
  File "/home/jdj/usr/opencv/lib/python2.7/site-packages/opencv/adaptors.py", line 64, in <module>
    import PIL
ImportError: No module named PIL
```
  1. Finally, if everything was done correctly, you should have your copy of Extractor working:
```
[jdj@ghoti3 extractor]$ ./ghoti.py 
processing ./in/tm_m.08-0183.jpg
	Creating binary image...
	Quantizing color...
	Calculating color ratio: 0.36865172038
	Calculating entropy 4.48076069686
	Quantizing color...
	Counting edges: 37.0989268842
	Quantizing color...
processing ./in/tg_m.08-0467.jpg
...
```
  1. The files in "in" directory will be processed and the vectors will be saved as "vector.txt".
  1. It is possible to invoke ghoti.py with one optional parameter:
```
[jdj@ghoti3 extractor]$ ./ghoti.py paper_set
or
[jdj@ghoti3 extractor]$ ./ghoti.py list.txt
```
    * If the parameter points to a directory, ghoti.py will scan the directory recursively and process the image files inside it.
    * If the parameter is a file, ghoti.py will read the content into a list and process the list.
    * The content of the list file (list.txt in the example) may look lile this:
```
paper_set/tm_f/08-0292.jpg
paper_set/tm_f/08-0032.jpg
paper_set/tm_f/08-0699.jpg
paper_set/tm_f/08-0272.jpg
paper_set/tm_f/08-0551.jpg
paper_set/tm_f/08-0611.jpg
paper_set/tm_f/08-0286.jpg
paper_set/tm_f/08-0066.jpg
paper_set/tm_f/08-0618.jpg
paper_set/tm_f/08-0581.jpg
```
  1. Note that "vector.txt" is APPENDED if you run ghoti.py multiple times!
  1. The vectors in vector.txt should look like this:
```
tm_m.08-0183 [115, 105, 111, 88, 81, 90, 106, 89, 93, 141, 136, 139, 255, 3, 250, 255, 0, 250, 152, 42, 149, 0, 0, 0, 0.3686517203798848, 4.48076069686116, 37.09892688419668, 330, 29, 14, 70]
tg_m.08-0467 [91, 74, 77, 102, 83, 85, 122, 98, 94, 255, 2, 250, 255, 0, 251, 143, 42, 136, 0, 0, 0, 0, 0, 0, 0.5611215592408959, 4.072968398993078, 6.303819299756639, 25, 0, 1, 110]
tg_m.08-0579 [76, 55, 57, 84, 61, 61, 100, 75, 67, 255, 2, 251, 98, 41, 87, 255, 0, 251, 0, 0, 0, 0, 0, 0, 0.8184807786939353, 4.560172513171992, 7.348531159638663, 26, 0, 1, 60]
tg_f.08-0944 [143, 119, 106, 160, 135, 120, 185, 151, 129, 255, 0, 251, 163, 62, 151, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5586887714214016, 4.411012052629912, 39.0173012581922, 426, 5, 9, 94]
```

# Running the Classifier #
With extracted vector.txt, we can perform the cichlid classification experiment.
  1. Copy vector.txt to $GHOTI/train
  1. If you intend to different name than vector.txt, modify the line in Makefile:
```
c=32768.0
g=0.00048828125
vector=vector.txt
test_sz=12
```
  1. Change vector.txt to what ever input vector name you want. Other c, g, test\_sz are experiment parameters, which is to be explained shortly.
  1. Modify test\_sz appropriately. When test\_sz is 12, it means that random 12 vectors will be the test vector and the rest are used for training the SVM.
  1. Now we need to adjust kernel parameters c and g. To do this easily, run
```
make easy
```
  1. which would run easy.py (from LIBSVM).
  1. If you encounter this error:
```
[jdj@ghoti3 train]$ make easy
#./easy.py y
./easy_nogui.py cychlid test
Traceback (most recent call last):
  File "./easy_nogui.py", line 28, in <module>
    assert os.path.exists(svmscale_exe),"svm-scale executable not found"
AssertionError: svm-scale executable not found
make: *** [easy] Error 1
```
  1. You haven't installed LIBSVM. Or, you didn't have administrative privileges to the Linux system and might have installed LIBSVM in your $HOME/usr/bin, as our [Compiling\_LIBSVM](Compiling_LIBSVM.md) has suggested. To walkaround this problem, modify easy.py or easy\_nogui.py line 15:
    * from
```
if not is_win32:
    svmscale_exe = "/usr/bin/svm-scale"
    svmtrain_exe = "/usr/bin/svm-train"
    svmpredict_exe = "/usr/bin/svm-predict"
    grid_py = "./grid.py"
    gnuplot_exe = "/bin/cat"
```
    * to
```
if not is_win32:
    svmscale_exe = "/home/jdj/usr/bin/svm-scale"
    svmtrain_exe = "/home/jdj/usr/bin/svm-train"
    svmpredict_exe = "/home/jdj/usr/bin/svm-predict"
    grid_py = "./grid.py"
    gnuplot_exe = "/bin/cat"
```
    * You need to modify /home/jdj as your $HOME variable:
```
[jdj@ghoti3 train]$ echo $HOME
/home/jdj
```
  1. If successful, you should see this output from make easy:
```
[jdj@ghoti3 train]$ make easy
#./easy.py y
./easy_nogui.py cychlid test
Scaling training data...
Cross validation...
Best c=32768.0, g=0.00048828125 CV rate=54.6296
Training...
Output model: cychlid.model
Scaling testing data...
Testing...
Accuracy = 50% (6/12) (classification)
Output prediction: test.predict
```
  1. Copy these c and g values to the Makefile. They are Kernel parameters for the SVM.
  1. by now, "make mix" (make test/training set), "make train" (train the SVM), "make predict" (make prediction) commands should work:
```
[jdj@ghoti3 train]$ make predict
svm-predict test cychlid.model test.predict
Accuracy = 75% (9/12) (classification)
```
  1. However, to make confusion table, "make mix" and "make train" should be run multiple times. To do that, we made 10\_confusion.sh script:
  1. Upon termination, 10\_confusion.sh will emit the confusion table in CSV format:
```
[jdj@ghoti3 train]$ ./10_confusion.sh 
./conv_to_svm.pl vector.txt > x
svm-scale -s scale_factor x > y
# subset, random on, all:y, sel test_sz, test_sz to test, rest to cychlid.
# subset.py is from LIBSVM scripts.
....
optimization finished, #iter = 9
nu = 0.002269
obj = -669.167019, rho = -0.152127
nSV = 3, nBSV = 0
Total nSV = 92
,Actual
Predicted,mv_f,pf_f,toc_m,pe_m,tm_f,tg_m,gm_f,pg_f,tg_f,toc_f,lf_m,tm_m
mv_f,89,15,0,0,0,0,0,10,0,6,0,0 
pf_f,0,71,0,0,0,0,0,0,0,0,0,0 
toc_m,0,0,43,0,0,1,0,10,0,9,0,0 
pe_m,0,0,1,44,0,11,25,1,0,5,0,8 
tm_f,0,3,0,4,32,8,13,0,0,6,0,10 
tg_m,0,0,1,3,19,36,27,2,22,10,2,11 
gm_f,0,8,9,32,9,9,16,0,0,17,0,0 
pg_f,2,0,9,6,10,1,0,40,15,4,0,0 
tg_f,0,7,0,0,0,17,0,26,69,1,0,0 
toc_f,12,0,34,0,18,9,17,8,0,18,0,0 
lf_m,0,0,0,0,0,0,0,0,0,0,89,13 
tm_m,0,0,0,10,14,20,0,0,0,0,17,56 
Sum,103,104,97,99,102,112,98,97,106,76,108,98
Accuracy(%),86.41,68.27,44.33,44.44,31.37,32.14,16.33,41.24,65.09,23.68,82.41,57.14
predictions made: 1200
overall accuracy: 50.25%
```
  1. This is it. To tune some experimental parameters, you need to modify conv\_to\_svm.pl script, which is the vector "preprocessor" mentioned in the paper. See [Tuning](Tuning.md) for details.