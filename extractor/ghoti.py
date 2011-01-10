#!/usr/bin/python2
# by jdj
# Assuming OpenCV 1.0 + Python 2.6
# On Ubuntu, it has opencv and python interface as package.
# Unfortunately, there is no OpenCV 1.0 package on OpenSUSE :(
#
# for PIL library, see http://www.pythonware.com/library/pil/handbook/index.htm
import os
import sys
import math

from opencv.cv import *
from opencv.highgui import  *
import opencv.adaptors # must install python-numeric package (Ubuntu/Debian) first, and maybe python-numpy.

import Image # PIL image... the native python image library.

# my custom set of functions
from cvlib import *

###
### Global variables
###
OUT="./out"
TMP="./tmp"
COLOR_QUANTIZATION=8
PREFIX=""
VECTOR_FNAME="./vector.txt"
VECTOR_FP=None
DO_EQUALIZE=1 # set this to non-zero, to equalize gray scale version of input.



def extractFeature( fname, basename ):
	features = []

	# load the image file
	img = cvLoadImage( fname )
	if not img:
		exit( "Unable to load image " + fname )

	# prepare a gray scale version
	gray = toGray( img )
	if DO_EQUALIZE :
		gray2 = copySize( gray, 1 )
		cvEqualizeHist( gray, gray2 )
		gray = gray2
		#show( "gray2", gray )

	# make mask data: non-magenta area is considered "fish".
	global PREFIX
	PREFIX = TMP + "/" + basename
	mask_data = generateMask( img )

	# try color quantization
	pil = quantizeColor( img, COLOR_QUANTIZATION )
	#pil.save( PREFIX+".quan.png" )
	palette = getPalette( pil, COLOR_QUANTIZATION )
	features.extend( palette )

	color_ratio = getColorRatio( pil, mask_data, COLOR_QUANTIZATION )
	features.append( color_ratio )
	#print "\t", palette
	# with this palette, we can try dot-producting them,
	# or, error energy
	# I'd favor error energy because the value would get quadratically larger, as the
	# difference gets larger
	# I've tried a few with GNU Octave and error energy seems to do well.

	# we run entropy calculation on quantized image.
	# Afterall, we want to see the fish stripe pattern, not exact color!
	entropy = calcEntropy( gray, mask_data )
	features.append( entropy )

	# Try edge detection to extract pattern
	edge = getEdge( gray )
	#cvSaveImage( PREFIX+".edge.png", edge )
	edge_cnt = countEdge( edge, mask_data )
	features.append( edge_cnt )

	# try to detect lines.
	lines, line_storage = getLines( edge )
	#debugDrawLines( img, edge, lines )
	angle_count = countAngles( lines )
	features.extend( angle_count )

	strip_count = countStrips( img )
	features.append( strip_count )

	return features



# from mid-left, move to mid-right,
# counting color changes countered.
def countStrips( img ):
	pil = quantizeColor( img, 3 )
	#pil.show()
	width = pil.size[0]
	height = pil.size[1]
	mid = int(height/2)

	cnt = 0
	tail = pil.getpixel( (0,mid) ) # tail remembers the last head value
	for x in range(0,width):
		xy = (x,mid)
		head = pil.getpixel(xy)
		diff = head - tail # diff!
		tail = head # remember the last value of head

		if diff != 0 :
			# print "diff at ", xy
			cnt = cnt + 1

	#print cnt
	return cnt



# counts vertical, horizontal, diagonal lines and return them.
def countAngles( lines ):
	cnts = [0] * 3
	for line in lines:
		pt1 = line[0]
		pt2 = line[1]
		x = pt2.x - pt1.x
		y = pt2.y - pt1.y
		#angle = cvRound( abs( math.atan2( y, x )*180/(45*CV_PI) ) )
		# angle, in degrees is divided by 45 so that
		# 0, 45, 90 maps to 0, 1, 2!
		# -45 is "diagonal" that goes with 45.
		# that's why there is "abs" function.
		# the code below is the optimized version.
		angle = cvRound( abs( math.atan2( y, x ) ) )
		cnts[angle] = cnts[angle]+1
	return cnts



def debugDrawLines( img, edge, lines ):
	dst = cvCloneImage( img )
	edge2 = cvCreateImage( cvGetSize(edge), 8, 3 )
	cvConvertImage( edge, edge2 )
	for line in lines:
		cvLine( dst, line[0], line[1], CV_RGB(0,255,0), 3, 8 )
		cvLine( edge2, line[0], line[1], CV_RGB(0,255,0), 3, 8 )
	cvSaveImage( PREFIX + ".lines.png", dst )
	cvSaveImage( PREFIX + ".lines2.png", edge2 )



def getLines( edge_in ):
	edge = cvCloneImage( edge_in ) # probabilistic hough modifies input image.
	line_storage = cvCreateMemStorage(0);
	#lines = cvHoughLines2( edge, line_storage, CV_HOUGH_PROBABILISTIC, 2, CV_PI/180, 50, 50, 15 );
	lines = cvHoughLines2( edge, line_storage, CV_HOUGH_PROBABILISTIC, 2, CV_PI/4, 50, 50, 15 );
	# must return line_storage, otherwise storage will be freed and lines would not be accessible
	# to other functions.
	return lines, line_storage



def countEdge( edge, mask_data ):
	edge_data = toRaw( edge )
	cnt = 0
	for i in range(0,len(edge_data)-1):
		val = edge_data[i]
		if val != 0 and mask_data[i] != 0 :
			cnt = cnt + 1
		#elif val != 0 and mask_data[i] == 0 :
		#	print "not counting"
	
	masklen = math.sqrt( sum( mask_data )/255 )
	result = cnt/masklen
	print "\tCounting edges:", result
	return result



# OpenCV implementation of adaptor doesn't work for PIL2Ipl.
# I've implemented one in simple (and stupid) way.
def pil2ipl( input, flag=CV_LOAD_IMAGE_UNCHANGED ):
	input.save( "/dev/shm/conv.bmp" )
	ipl = cvLoadImage( "/dev/shm/conv.bmp", flag )
	return ipl



# pil_quan: image with quantized color, PIL image.
def getEdge( gray ):
	# remove the background before quantizing,
	# which might have similar intensity with the fish
	gray2 = cvCloneImage( gray )
	cvFloodFill( gray2, cvPoint(0,0), 0 )

	# quantize fish color to 2 colors
	pil2 = quantizeColor( gray2, 3 )
	thr = pil2ipl( pil2, CV_LOAD_IMAGE_GRAYSCALE )

	edge = cvCreateImage( cvGetSize(gray2), 8, 1  )
	cvCanny( thr, edge, 100, 150 )
	return edge



def getPalette( pil, num_colo ):
	palette = pil.getpalette()
	palette = trimPalette( palette, num_colo )

	# count each colors
	cnt = [0] * num_colo
	raw = list( pil.getdata() )
	for r in raw:
		cnt[r] = cnt[r]+1
	#print cnt

	# remove magenta. we don't want it.
	pal2 = []
	cnt2 = []
	for i in range( len(cnt) ):
		rgb = palette[ 3*i : 3*i+3 ]
		# jpg artifact :(
		# should not put EXACT value.
		if rgb[0] >= 253 and rgb[1] <= 2 and rgb[2] >= 253:
			# print "magenta detected"
			zzz=0 # useless code
		else:
			pal2.extend( rgb )
			cnt2.append( cnt[i] )

	# bubble sort the palette according to frequency,
	# after sorting, higher frequency comes at lower index.
	for i in range( len(cnt2) ):
		for j in range( i+1, len(cnt2) ):
			if cnt2[i] < cnt2[j]:
				cnt2[i], cnt2[j] = cnt2[j], cnt2[i]
				pal2[3*i+0], pal2[3*j+0] = pal2[3*j+0], pal2[3*i+0]
				pal2[3*i+1], pal2[3*j+1] = pal2[3*j+1], pal2[3*i+1]
				pal2[3*i+2], pal2[3*j+2] = pal2[3*j+2], pal2[3*i+2]

	# add "black" at the end, if less than 8 colors left.
	while len(pal2) < 24:
		pal2.append( 0 )

#	print len(cnt2), len(pal2)
#	print cnt2
#	print pal2
	
	return pal2



# image raw data to python list.
def toRaw( img ):
	raw = list( img.imageData )
	data = []
	for r in raw:
		data.append( ord( r ) )
	return data



###
### color ratio
###
def getColorRatio( pil, mask_data, num_colo ):
	# count quantized color frequency.
	# this process is very similar to calcEntropy
	histogram = [0] * num_colo
	data = list( pil.getdata() )
	for i in range( 0, len( data ) ):
		if mask_data[i] != 0:
			val = data[i]
			histogram[val] = histogram[val] + 1

	histogram.sort()
	M1 = histogram.pop() # MAX
	M2 = histogram.pop() # 2nd max
	r= float(M2)/float(M1) # we divide it thisway so the value lies in [0,1].
	print "\tCalculating color ratio:", r
	return r



###
### calculate fish entropy, of non-mask area.
###
def calcEntropy( gray, mask_data ):
	# make array of intensity.
	"""
	THIS IS SLOW
	data = []
	for y in range(gray.height):
		for x in range(gray.width):
			p = cvGet2D( gray, y, x ) ; p = int( p[0] )
			m = cvGet2D( mask, y, x ) ; m = int( m[0] )
			if m != 0:
				data.append( p )
	Even with the toRaw conversion, it is A LOT faster.
	"""
	raw_data = toRaw( gray )
	data = []
	for i in range(0,len(raw_data)-1):
		val = raw_data[i]
		if mask_data[i] != 0:
			data.append( val )

	histogram = [0] * 256 # [0,0,0,...0], lengh==256
	for val in data:
		histogram[val] = histogram[val]+1
	
	# convert histogram to probability
	total = sum( histogram )
	prob = []
	for h in histogram:
		if h != 0:
			prob.append( float(h) / float( total )  )
	
	# now we have probability in prob. ready to calculate entropy
	entropy = 0
	for p in prob:
		entropy = entropy - p*math.log( p, 2 )

	#cvSaveImage( prefix+str((entropy))+".png", gray )
	print "\tCalculating entropy", entropy
	return entropy



###
### removes redundant palette
### Assumes RGB palette.
### Assumes the valid colors are at front, not at the back.
###
def trimPalette( pal, num ):
	# pop everything until only num*3 elements are left.
	length = num*3
	while( len( pal ) > length ):
		pal.pop()
	return pal

###
### quantizeColor
###
def quantizeColor( img, num_colo ):
	# I could have implemented this myself, but
	# that would be SLOW if written in python.
	# Quantization is already in python anyway.
	print "\tQuantizing color..."
	pil = opencv.adaptors.Ipl2PIL( img )
	pil = pil.convert( "P", colors=num_colo, palette=Image.ADAPTIVE )
	return pil



def get2D( img, y, x ):
	b = ord( img.imageData[ img.widthStep*y+3*x+0 ] )
	g = ord( img.imageData[ img.widthStep*y+3*x+1 ] )
	r = ord( img.imageData[ img.widthStep*y+3*x+2 ] )
	return [b,g,r]
#define CV_IMAGE_ELEM( image, elemtype, row, col )       \
#    (((elemtype*)((image)->imageData + (image)->widthStep*(row)))[(col)])



###
### let magenta (255,0,255) be zero.
###
def generateMask( img ):
	print "\tCreating binary image..."
	bin = cvCreateImage( cvGetSize(img), 8, 1 )

	data = toRaw( img )
	result = []
	for i in range( 0, len(data), 3 ):
		if data[i] == 255 and data[i+1] == 0 and data[i+2] == 255 :
			result.append( 0 )
		else:
			result.append( 255 )

	return result



###
### pick the largest blob
###
def largestBlob( bin_img ):
	print "\tFinding largest blob..."

	dst = cvCreateImage( cvGetSize(bin_img), 8, 3 );
	cvZero( dst );

	storage = cvCreateMemStorage(0);
	nb_contours, cont = cvFindContours( bin_img, storage, sizeof_CvContour, CV_RETR_CCOMP, CV_CHAIN_APPROX_SIMPLE );

	max = None
	area = 0

	# find the largest contour
	for c in cont.hrange():
		# draw around contour to see it
		#color = CV_RGB( 255, 0, 0 )
		#cvDrawContours( dst, c, color, color, -1, 1, 8 )

		rect = cvBoundingRect( c )
		_area = rect.width * rect.height
		if( _area > area ):
			max = c
			area = _area

	color = CV_RGB( 255, 255, 255 )
	cvDrawContours( dst, max, color, color, -1, CV_FILLED, 8 )

	return dst



###
### the main function
###

mkdirne( OUT )
mkdirne( TMP )

# make a list of files in input_dir
input_dir = "./in"
files=os.listdir( input_dir )
VECTOR_FP = open( VECTOR_FNAME, 'w' )

# for each files in the list...
for fname in files:
	# extract extension and run algorithm,
	# only if it is a picture.
	basename, extension = os.path.splitext( fname )
	extension = extension.lower() # lowercase the extension to make JPG/Jpg/jPg/etc -> to jpg.
	if extension == ".jpg" or \
		extension == ".jpeg" or \
		extension == ".bmp" or \
		extension == ".gif" or \
		extension == ".png":
			full_name = os.path.join( input_dir, fname )
			print "processing " + full_name
			features = extractFeature( full_name, basename )
			print>>VECTOR_FP, basename, features

VECTOR_FP.close()

