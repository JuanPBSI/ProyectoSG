#!/usr/bin/perl
use strict;
#use warnings;

# Variables para los logs de acceso de apache
my @ip_acces = ();
my @fecha_acces = ();
my @MetodoHTTP_acces = ();
my @Recurso_acces = ();
my @VersionHTTP_acces = ();
my @CodigoHTTP_acces = ();
my @Rec_size_acces = ();
my @HTTP_referer_acces = ();
my @UserAgent_acces = ();

# Variables para los logs de error de apache
my @fecha_error = ();
my @ip_error = ();
my @log_error = ();
my @msg_error = ();

# Obtenemos los archivos generados por el modulo de obtencion de archivos
my $log_Apache = $ARGV[0] or die "Leer log de apache\n";
my $log_Apache_error = $ARGV[1] or die "Leer log de error de apache\n";
my $log_Postgres = $ARGV[2] or die "Leer log de apache\n";

# Abrimos el archivo de los logs
open(my $data_acces, '<', $log_Apache) or die "No se puede abrir el archivo\n";
open(my $data_error, '<', $log_Apache_error) or die "No se puede abrir el archivo\n";
open(my $data_postgres, '<', $log_Postgres) or die "No se puede abrir el archivo\n";

# Creamos los nuevos archivos para los logs que guardara en el siguiente formato
# $variable1;$variable2;$variable3...

my $filename1 = 'acces.txt';
my $filename2 = 'error.txt';

open(my $new_acces, '>', $filename1) or die "Could not open file '$filename1' $!";
open(my $new_error, '>', $filename2) or die "Could not open file '$filename2' $!";

while (my $line1 = <$data_acces>)
{
	chomp $line1;

	# Parseamos el log de acceso apache
	my @log_apache_array = (split " " , $line1, 12);
	my @log_apache_array_aux = (split /\"/ , $line1);
	my $aux='';
	
	$aux = $log_apache_array[0];
	push @ip_acces, $aux;
	$aux = $log_apache_array[3];
	$aux =~ tr/\[//d;
	push @fecha_acces, $aux;
	$aux  = $log_apache_array[5];
	$aux =~ tr/\"//d;
	push @MetodoHTTP_acces, $aux;
	$aux  = $log_apache_array[6];
	push @Recurso_acces,$aux;
	$aux  = $log_apache_array[7];
	$aux =~ tr/\"//d;
	push @VersionHTTP_acces,$aux;
	$aux  = $log_apache_array[8];
	push @CodigoHTTP_acces,$aux;
	$aux = $log_apache_array[9];
	push @Rec_size_acces,$aux;
	$aux = $log_apache_array[10];
	$aux =~ tr/\"//d;
	push @HTTP_referer_acces,$aux;
	$aux = $log_apache_array_aux[5];
	push @UserAgent_acces,$aux;
	print $new_acces "$ip_acces[-1];$fecha_acces[-1];$MetodoHTTP_acces[-1];$Recurso_acces[-1];$VersionHTTP_acces[-1];$CodigoHTTP_acces[-1];$Rec_size_acces[-1];$HTTP_referer_acces[-1];$UserAgent_acces[-1]\n";
}

while (my $line2 = <$data_error>)
{
	chomp $line2;
	my @log_apache_error_array = (split /\]/ , $line2);
	my @log_apache_error_array_aux = (split /\:/ , $line2);
	my $aux='';

	my $aux = $log_apache_error_array[0];
	$aux =~ tr/\[//d;
	push @fecha_error,$aux;
	$aux = $log_apache_error_array[1];
	$aux =~ tr/\ [//d;
	push @log_error,$aux;
	$aux = $log_apache_error_array[2];
	$aux =~ tr/  \[client//d;
	push @ip_error,$aux;
	$aux = $log_apache_error_array[3];
	#$aux =~ tr/^._//d;
	push @msg_error,$aux;
	print $new_error "$fecha_error[-1];$log_error[-1];$ip_error[-1];$msg_error[-1]\n";
}

close $new_acces;
close $new_error;

#my $size_log_acces = `sort -t . -k 3,3n -k 4,4n $filename1 | cut -d";" -f 1 |  uniq -c`;
#print $size_log_acces;
#foreach my $i (0 .. $#UserAgent) {
  #print "$UserAgent[$i]\n";
#}