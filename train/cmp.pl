#!/usr/bin/perl
# This script compares prediction result to see see the predictions
# were correct and generates confusion matrix.

use strict;
# the integers are used as libsvm training classes. you must keep them unique!
use vars '%class_kind_map';
require "kmap.pl";


sub read_mtx
{
	# input
	my $en = shift;
	my $mtx = shift;
	my $prefix = shift;
	my $lo = shift;
	my $hi = shift;

	for( my $i = $lo ; $i <= $hi ; ++$i ) {
		my $fname = $prefix . "." . $i;
		open F, "<$fname";
		open G, "<$fname.predict";

		while( chomp( my $line1 = <F> ) ) {
			chomp( my $line2 = <G> );

			if( $line1 !~ /^([0-9]+)/ ) {
				die "Parsing Error :(\n";
			}
			my $cat1 = $1;

			if( $line2 !~ /^([0-9]+)/ ) {
				die "Parsing Error :(\n";
			}
			my $cat2 = $1;

			# set enabled flag
			$en->{$cat1} = 1;
			$en->{$cat2} = 1;

			# keep counter
			++$mtx->[$cat1][$cat2];
		}

		close F;
		close G;
	}
}



sub print_mtx
{
	my $en = shift;  # ptr
	my $mtx = shift; # ptr

	# show matrix in latex forma
	my @heads = keys %$en;
	foreach( @heads ) {
		$_ = $class_kind_map{ $_ };
	}
	unshift @heads, "Predicted";
	my $head = join ",", @heads;
	print ",Actual\n";
	print $head, "\n";

	foreach my $i (keys %$en) {
		my @row;
		push @row, $class_kind_map{ $i };

		foreach my $j (keys %$en) {
			my $val = 0;
			if( defined $mtx->[$j][$i] ) {
				$val = $mtx->[$j][$i];
			}
			push @row, $val;
		}

		my $str = join ",", @row;
		print $str, " \n";
	}
}



# parse commandline arg and return vars
sub read_param
{
	my $prefix = shift;
	if( $prefix eq "" ) {
		print STDERR "Confusion matrix generator.\n";
		print STDERR "This script compares test vectors and its prediction\n";
		print STDERR "from libsvm. Provide input test vector file name as input.\n";
		print STDERR "usage: ./cmp.pl test 1 10\n";
		print STDERR "       will process files test.1 through test.10.\n";
		exit 1;
	}
	my $lo = shift;
	my $hi = shift;

	return ($prefix,$lo,$hi);
}



sub calc_sums
{
	my $en = shift;  # actually, pointer.
	my $mtx = shift; # actually, pointer.

	my @sums;

	foreach my $i (keys %$en) {
		my $sum = 0;
		foreach my $j (keys %$en) {
			my $val = 0;
			if( defined $mtx->[$i][$j] ) {
				$val = $mtx->[$i][$j];
			}
			$sum += $val;
		}
		@sums[$i] = $sum;
	}

	return @sums;
}



sub print_1d
{
	my $en = shift;  # ptr
	my $arr = shift; # ptr

	my @row;
	foreach my $i (keys %$en) {
		push @row, $arr->[$i];
	}

	my $str = join ",", @row;
	print $str, "\n";
}



sub round
{
	my $var = shift;
	$var *= 100;
	$var += 0.5;
	$var = int($var);
	$var /= 100;
	return $var;
}

sub calc_accus
{
	my $en = shift;  # actually, pointer.
	my $mtx = shift; # actually, pointer.
	my $sums = shift; # actually, pointer.

	my @accus;
	my $total_right = 0;
	my $total_cnt = 0;

	foreach my $i (keys %$en) {
		my $val = 0;
		if( defined $mtx->[$i][$i] ) {
			$val = $mtx->[$i][$i];
		}

		$total_cnt += $sums->[$i];
		$total_right += $val;

		my $accu = 100;
		if( $sums->[$i] != 0 ) {
			$accu = round( 100 * $val / $sums->[$i] );
		}
		@accus[$i] = $accu;
	}

	return ($total_cnt, $total_right, @accus);
}



###
### main
###

# data
my %en; # enabled specie?
my @mtx; # 2d matrix data [actual][predicted]

(my $prefix, my $lo, my $hi) = read_param( @ARGV );

read_mtx( \%en, \@mtx, $prefix, $lo, $hi );
print_mtx( \%en, \@mtx );

my @sums = calc_sums( \%en, \@mtx );
print "Sum,";
print_1d( \%en, \@sums );

(my $total_cnt, my $total_right, my @accus) = calc_accus( \%en, \@mtx, \@sums );
print "Accuracy(%),";
print_1d( \%en, \@accus );

print "predictions made: $total_cnt\n";
print "overall accuracy: ", round(100*$total_right/$total_cnt), "%\n";
