#Howto compile and install OpenCV 1.0 manually

# OpenCV 1.0 manual installation #
  1. From [OpenCV Project Page](http://sourceforge.net/projects/opencvlibrary/), navigate to and download OpenCV 1.0: http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/1.0/opencv-1.0.0.tar.gz/download.
  1. Unarchive OpenCV. A new directory (folder, in Windows terms) will be created.
```
tar zxvf opencv-1.0.0.tar.gz
```
  1. Configure OpenCV with following command:
```
cd opencv-1.0.0
./configure \
    --prefix=$HOME/usr/opencv \
    --with-swig \
    --with-python \
    --with-ffpmeg
```
  1. On Arch Linux, OpenCV might try bind to Python 3, which will result in following error:
```
configure: Checking for necessary tools to build python wrappers
checking for python... /usr/bin/python
checking for python version...   File "<string>", line 1
    import sys; print sys.version[:3]
                        ^
SyntaxError: invalid syntax

checking for python platform...   File "<string>", line 1
    import sys; print sys.platform
                        ^
SyntaxError: invalid syntax

checking for python script directory... ${prefix}/lib/python/site-packages
checking for python extension module directory... ${exec_prefix}/lib/python/site-packages
  File "<string>", line 1
    import sys; print sys.prefix
                        ^
SyntaxError: invalid syntax
configure: error: Python Prefix is not known
```
  1. If that's the case, try this command for configuration:
```
PYTHON=/usr/bin/python2 ./configure \
    --prefix=$HOME/usr/opencv \
    --with-swig \
    --with-python \
    --with-ffpmeg
```
  1. Upon success, you should see something like this:
```

Wrappers for other languages =========================================
    SWIG                      
    Python                    yes

Additional build settings ============================================
    Build demo apps           yes

Now run make ...
```
  1. If not, please consult OpenCV manual.
  1. In cxcore/include/cxmisc.h, line 133, there is #elif, which should be #else:
```
#ifdef __GNUC__
    #undef alloca
    #define alloca __builtin_alloca
#elif defined WIN32 || defined WIN64
    #if defined _MSC_VER || defined __BORLANDC__
        #include <malloc.h>
    #endif
#elif defined HAVE_ALLOCA_H
    #include <alloca.h>
#elif defined HAVE_ALLOCA
    #include <stdlib.h>
#elif
    #error
#endif
```
  1. Change the last #elif to #else like this:
```
#else
    #error
#endif
```
  1. type "make" command without quotes to compile the OpenCV library.
```
make
```
  1. After a long compile process, it will be finally done:
```
Making all in docs
make[2]: Entering directory `/home/jdj/ghoti/opencv/opencv-1.0.0/docs'
make[2]: Nothing to be done for `all'.
make[2]: Leaving directory `/home/jdj/ghoti/opencv/opencv-1.0.0/docs'
make[2]: Entering directory `/home/jdj/ghoti/opencv/opencv-1.0.0'
make[2]: Leaving directory `/home/jdj/ghoti/opencv/opencv-1.0.0'
make[1]: Leaving directory `/home/jdj/ghoti/opencv/opencv-1.0.0'
```
  1. type make install command to do the installation.
```
make install
```
  1. When done, in your home directory, you should have usr directory created.
  1. From the usr directory, move to opencv then lib directory , and you should have these files:
```
libcvaux.la
libcvaux.so
libcvaux.so.1
libcvaux.so.1.0.0
libcvhaartraining.a
libcv.la
libcv.so
libcv.so.1
libcv.so.1.0.0
libcxcore.la
libcxcore.so
libcxcore.so.1
libcxcore.so.1.0.0
libhighgui.la
libhighgui.so
libhighgui.so.1
libhighgui.so.1.0.0
libml.la
libml.so
libml.so.1
libml.so.1.0.0
pkgconfig
python2.7
```
  1. Another important files are the files in usr/opencv/lib/python2.7/site-packages/opencv directory:
```
adaptors.py
adaptors.pyc
adaptors.pyo
_cv.la
cv.py
cv.pyc
cv.pyo
_cv.so
_highgui.la
highgui.py
highgui.pyc
highgui.pyo
_highgui.so
__init__.py
__init__.pyc
__init__.pyo
matlab_syntax.py
matlab_syntax.pyc
matlab_syntax.pyo
```
  1. You are done!