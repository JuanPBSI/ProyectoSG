#!/usr/bin/perl
use strict;
my $select = $ARGV[0];
my $cont = $ARGV[1];
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
	$cmd = `cat mensajeCRAW.txt | cut -d"[" -f 3 | cut -d "]" -f 1 | sort | uniq -c`;
}
elsif ($select == 5)
{
	$cmd = `cat mensajeDEFC.txt | cut -d"|" -f 1 | sort | uniq -c`;
}
elsif ($select == 6)
{
	$cmd = `cat mensajeSQL.txt | cut -d"|" -f 3 | sort | uniq -c`;
}
elsif ($select == 7)
{
	$cmd = `cat mensajeXSS.txt | cut -d"|" -f 3 | sort | uniq -c`;
}
elsif ($select == 8)
{
	$cmd = `cat mensajePATH.txt | cut -d"|" -f 3 | sort | uniq -c`;
}
elsif ($select == 10)
{
	$cmd = `cat mensajeDEFC.txt | cut -d"|" -f 3 | sort | uniq -c`;
}
elsif ($select == 11)
{
	$cmd = `cp Templates/* ./`;
}
elsif ($select == 12)
{
	$cmd = `awk "NR==$cont" cod_status.txt`;
}
elsif ($select == 13)
{
	$cmd = `grep -i "sql" ModSecReport.log | cut -d"[" -f 3 | cut -d"]" -f 1 | sort | uniq -c`;
}
elsif ($select == 14)
{
	$cmd = `grep -i "xss" ModSecReport.log | cut -d"[" -f 3 | cut -d"]" -f 1 | sort | uniq -c`;
}
elsif ($select == 15)
{
	$cmd = `grep -i "sql" ModSec.log | cut -d"[" -f 3 | cut -d"]" -f 1 | sort | uniq -c`;
}
elsif ($select == 16)
{
	$cmd = `grep -i "xss" ModSec.log | cut -d"[" -f 3 | cut -d"]" -f 1 | sort | uniq -c`;
}
elsif ($select == 17)
{
	$cmd = `cat extra/mensajeSQL.txt | cut -d"|" -f 1 | sort | uniq -c`;
}
elsif ($select == 18)
{
	$cmd = `cat extra/mensajeXSS.txt | cut -d"|" -f 1 | sort | uniq -c`;
}
elsif ($select == 19)
{
	$cmd = `cat extra/mensajePATH.txt | cut -d"|" -f 1 | sort | uniq -c`;

}
elsif ($select == 20)
{
	$cmd = `cat extra/mensajeCRAW.txt | cut -d"[" -f 3 | cut -d "]" -f 1 | sort | uniq -c`;
}
elsif ($select == 21)
{
	$cmd = `cat extra/mensajeDEFC.txt | cut -d"|" -f 1 | sort | uniq -c`;
}
elsif ($select == 22)
{
	$cmd = `grep -i "traversal" ModSec.log | cut -d"[" -f 3 | cut -d"]" -f 1 | sort | uniq -c`;
}
elsif ($select == 23)
{
	$cmd = `grep -i "traversal" ModSecReport.log | cut -d"[" -f 3 | cut -d"]" -f 1 | sort | uniq -c`;
}
chomp $cmd;
print $cmd;
