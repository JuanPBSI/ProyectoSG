#!/usr/bin/perl
use strict;

my $cmd = `wc -l cod_status.txt | cut -d" " -f 1 `;
chomp $cmd;
print $cmd;
