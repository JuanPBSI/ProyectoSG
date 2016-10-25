#!/usr/bin/perl
use strict;
my $select = $ARGV[0];
my $cmd = 'nada';
if ($select == 0)
{
	$cmd = `wc -l cod_status.txt | cut -d" " -f 1 `;
}
elsif ($select == 1)
{
	$cmd = `cat mensajeSQL.txt | cut -d"|" -f 1 | sort | uniq -c`;
}
elsif ($select == 2)
{
	$cmd = `cat mensajeXSS.txt | cut -d"|" -f 1 | sort | uniq -c`;
}
elsif ($select == 3)
{
	$cmd = `cat mensajePATH.txt | cut -d"|" -f 1 | sort | uniq -c`;
}
elsif ($select == 4)
{
	$cmd = `cat mensajeSQL.txt | cut -d"|" -f 3 | sort | uniq -c`;
}
elsif ($select == 5)
{
	$cmd = `cat mensajeXSS.txt | cut -d"|" -f 3 | sort | uniq -c`;
}
elsif ($select == 6)
{
	$cmd = `cat mensajePATH.txt | cut -d"|" -f 3 | sort | uniq -c`;
}
elsif ($select == 7)
{
	$cmd = `cp Templates/* ./`;
}

chomp $cmd;
print $cmd;
