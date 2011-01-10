#!/usr/bin/python2
# Some utility functions
import os
import sys
from opencv.cv import *
from opencv.highgui import  *

# makes directory, of not exists.
def mkdirne( path ):
	if not os.path.exists( path ):
		os.mkdir( path )
	else:
		# check if it is a dir. not file.
		if os.path.isdir( path ):
			return
		else:
			sys.exit( path + " already exists and it is not a directory :(" )



# display given image with given named window.
def show( wndname, img ):
	cvNamedWindow( wndname, 0 )
	cvShowImage( wndname, img )
	c = cvWaitKey( 0 )
	cvDestroyWindow( wndname )



def copySize( img, ch ):
	dst = cvCreateImage( cvSize(img.width,img.height), 8, ch )
	return dst



# generates outputName.
# for example...
# iput: /path/to/img.jpg, _gray
# output: ./out/img_gray.jpg
def outputName( full_path, suffix ):
	basename = os.path.basename( full_path )
	root, ext = os.path.splitext( basename )
	new_name = root + suffix + ext
	return os.path.join( "./out", new_name )



# converts given src_img go gray scale image.
def toGray( src_img ):
	gray = cvCreateImage( cvSize(src_img.width,src_img.height), 8, 1 )
	cvCvtColor( src_img, gray, CV_BGR2GRAY )
	return gray

