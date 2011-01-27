#!/usr/bin/perl
###
### input text file for libsvm, using converts list.txt, types.csv.
###

###
### some configurations
###
my $USE_FEMALES = 1; # if 0, females are excluded.
my $USE_MALES = 1; # if 0, males are excluded.

###
### some predefined values.
###
# the integers are used as libsvm training classes. you must keep them unique!
use vars '%kind_class_map';
require "kmap.pl";

###
### implementation begins
###

sub max {
	my @data = @_;
	my $M = $data[0];
	foreach my $d (@data ) {
		if ( $d > $M ) {
			$M = $d
		}
	}
	return $M;
}

sub min {
	my @data = @_;
	my $m = $data[0];
	foreach my $d (@data ) {
		if ( $d < $m ) {
			$m = $d
		}
	}
	return $m;
}

sub HSV
{
	my $R = shift;
	my $G = shift;
	my $B = shift;
	my $var_R = ( $R / 255 );
	my $var_G = ( $G / 255 );
	my $var_B = ( $B / 255 );

	my $var_Min = min( $var_R, $var_G, $var_B );
	my $var_Max = max( $var_R, $var_G, $var_B );
	my $del_Max = $var_Max - $var_Min;

	my $H;
	my $S;
	my $V = $var_Max;

	if ( $del_Max == 0 )
	{
		$H = 0;
		$S = 0;
	}
	else
	{
		$S = $del_Max / $var_Max;

		my $del_R = ( ( ( $var_Max - $var_R ) / 6 ) + ( $del_Max / 2 ) ) / $del_Max;
		my $del_G = ( ( ( $var_Max - $var_G ) / 6 ) + ( $del_Max / 2 ) ) / $del_Max;
		my $del_B = ( ( ( $var_Max - $var_B ) / 6 ) + ( $del_Max / 2 ) ) / $del_Max;

		if ( $var_R == $var_Max ) {
			$H = $del_B - $del_G;
		}
		elsif ( $var_G == $var_Max ) {
			$H = ( 1 / 3 ) + $del_R - $del_B;
		}
		elsif ( $var_B == $var_Max ) {
			$H = ( 2 / 3 ) + $del_G - $del_R;
		}

		if ( $H < 0 ) {
			$H += 1
		}
		if ( $H > 1 ) {
			$H -= 1
		}
	}

	$H = int( $H*360+0.5 );
	$S = int( $S*100+0.5 );
	$V = int( $V*100+0.5 );

	return ( $R, $G, $B, $H, $S, $V );
	#return ( $R, $G, $G );
	#return ( $H, $S, $V );

}


sub emit
{
	my @vec = @_;

	# print the vector
	for( my $i = 0 ; $i <= $#vec ; ++$i ) {
		my $d = $vec[$i];
		my $j = $i + 1;
		print "$j:$d ";
	}
	print "\n";
}



sub exclude
{
	my @arr = @_;

	# f scores
	my @en = (
		1.50981210690695,
		1.60452801130772,
		1.83500101057865,
		2.90011046074693,
		2.07863292688626,
		1.77004970148283,
		1.0949556038474,
		1.32568709339806,
		1.53072521508579,
		2.39401718285506,
		2.05847037180318,
		1.47615548929553,
		1.14037561856449,
		1.12171829518137,
		1.42910355085241,
		0.186378797373588,
		1.57100605711816,
		1.37240623123178,
		1.13741242924635,
		0.940657657819389,
		0.938177804931876,
		0.599951552192062,
		1.17315574922372,
		0.95739311049547,
		0.659989159422676,
		0.377283088935723,
		0.748190152098377,
		0.130738237774085,
		0.381569113054925,
		0.744003257339335,
		0.0838461020547469,
		0.0344556804670454,
		0.0845386231010729,
		0.0737956939169396,
		0.08188901200001,
		0.0844852066204524,
		0.0848692925373007,
		0.021939199517398,
		0.086652912758584,
		0.0913884767361888,
		0.0844875533969461,
		0.0866416775356986,
		-1,
		-1,
		-1,
		-1,
		-1,
		-1,
		0.547026871224764,
		1.22936084400121,
		1.07034766836616,
		0.884047132748099,
		0.574622838389981,
		1.10664104020601,
		0.384361918976852
	);


	my @result;
	for( my $i = 0 ; $i <= $#arr ; ++$i ) {
		# use 3 colors
		if( $i < 6*3 ) {
			if( $i % 6 < 3 ) {
				# RGB
				push( @result, $arr[$i] );
			}
			elsif( $i % 6 >= 3 ) {
				# HSV
				push( @result, $arr[$i] );
			}
		}
		else {
			if( $i >= 48 ) {
				# non-color features
				if( $en[$i] >= 0.7 ) {
					push( @result, $arr[$i] );
				}
			}
		}
	}

	return @result;
}


###
### main
###

my $f = shift || die "usage: ./conv_to_svm.pl [vector from extractor] > [output name]\n";

open F, "<$f";

while( chomp( my $line = <F> ) ) {
	if( $line =~ /(\S+) \[(.+)\]/ ) {
		my $pic = $1;
		my $raw_data = $2;

		# convert pic(file name) to lbl,
		# then convert the label to kind and class.
		if( $pic !~ /^([^.]+)\./ ) {
			print STDERR "error parsing $pic\n";
			die "unable to get kind :(\n";
		}
		my $kind = $1;
		my $class = $kind_class_map{ $kind };

		if( $USE_FEMALES == 0 && $kind =~ /_f$/ ) {
			next;
		}
		if( $USE_MALES == 0 && $kind =~ /_m$/ ) {
			next;
		}

		my @data = split( /, /, $raw_data );

		#print "$pic, $lbl, $kind, $class\n";
		# we might not be able to retrieve class for some pics.
		if( ! $class ) {
			print STDERR "Warning: unable to get class type for $pic\n";
			print STDERR "\t$pic has kind of $kind\n";
			next;
		}

		# 0 ~ 23: RGB palette of 8 colors.
		# 24: color ratio: m1/m2 pixel count, where m1 is the most
		#     frequent color, m2 is the second most.
		# 25: entropy
		# 26: edge_cnt
		# 27:  0 deg line cnt
		# 28: 45 deg line cnt
		# 29: 90 deg line cnt
		# 30: strip count
		print "$class ";
		my @vec;
		for( my $i = 0 ; $i <= $#data ; ++$i ) {
			# if color
			if( $i <= 23 ) {
				if( $i % 3 == 0 ) {
					my @colos = HSV( $data[$i], $data[$i+1], $data[$i+2] );
					push( @vec, @colos );
				}
			}
			else {
				#next;
				push( @vec, $data[$i] );
			}
		}

		@vec = exclude( @vec ); # exclude some features
		emit( @vec ); # emit the vector
	}
}

close F;
