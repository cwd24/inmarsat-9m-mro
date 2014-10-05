#!/usr/local/bin/perl

# Compute the positions of satellites at the current time, as seen from
# a pre-programmed position. The TLE data are read from standard in, or
# from a file or files named on the command line.

use strict;
use warnings;

use Astro::Coord::ECI;

use Text::CSV;
use DateTime::Format::Strptime;

my $strp = DateTime::Format::Strptime->new(pattern => '%FT%T');

my $csv = Text::CSV->new ( { binary => 1 } )  # should set binary attribute.
                 or die "Cannot use CSV: ".Text::CSV->error_diag ();

open my $fh, "<:encoding(utf8)", "cpp-teme.csv" or die "cpp-teme.csv: $!";
$csv->getline( $fh ); # header
while ( my $row = $csv->getline( $fh ) ) {
        my $time = pop @$row;
	my $dt = $strp->parse_datetime($time);

	my $a = Astro::Coord::ECI->new;
	my $eci = $a->eci(@$row, $dt->epoch);
	print join ',', $time, $eci->ecef;
	print "\n";
}
close $fh;

