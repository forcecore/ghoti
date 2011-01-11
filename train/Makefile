c=32768.0
g=0.00048828125
vector=vector.txt
test_sz=12

all: data mix train predict

data:
	./conv_to_svm.pl $(vector) > x
	svm-scale -s scale_factor x > y

mix:
	# subset, random on, all:y, sel test_sz, test_sz to test, rest to cychlid.
	# subset.py is from LIBSVM scripts.
	./subset.py -s 1 y $(test_sz) test cychlid

easy:
	#./easy.py y
	./easy_nogui.py cychlid test

train:
	svm-train -c $c -g $g cychlid

predict:
	svm-predict test cychlid.model test.predict
