#!/usr/bin/perl
use strict;
#use warnings;

use scripts::XSS;
use scripts::PathTransversal;
use scripts::utilerias;
use scripts::Crawler;
use scripts::SQLi;


#Variables para leer el archivo de configuracion
my $config_file = $ENV{HOME}."/Proyecto/herramienta.conf";
my %Config = ();
utilerias::read_config_file($config_file, \%Config);
my $dirParsedApache = $Config{'parsedLogAccess'};
my $dirParsedApacheError = $Config{'parsedLogError'};
my $dirParsedPostgres = $Config{'parsedLogPostgres'};
my $dirListas = $Config{'rutaListas'};
my $toleranciaError = $Config{'toleranciaError'};

#Datos para el crawler
my $frecPromPeticionSeg=$Config{'frecPromPeticionSeg'};
my $toleranciaSegundos=$Config{'toleranciaSegundos'};
my $duracionSeg=$Config{'duracionSeg'};

my $recurso;
my $nullFlag=0;
my $diagnostico_PATH = 0;
my $diagnostico_XSS = 0;
my $diagnostico_SQLi = 0;
my $diagnostico_CRAW = 0;
my $diagnostico_DEF = 0;
my %ips;
my $refUserAgent;
my $refTiempo;
my $refSolicitudes;

#En el archivo de configuracion usa el comodin  ~ en referencia al directorio HOME, Perl no puede interpretar la tilde como el directorio, para ello la sustituimos ~ por la variable de
#entorno de Perl  que contiene el directorio HOME del usuario

$dirParsedApache =~ s/^~(\w*)/$ENV{HOME}/e;
$dirParsedApacheError =~ s/^~(\w*)/$ENV{HOME}/e;
$dirParsedPostgres =~ s/^~(\w*)/$ENV{HOME}/e;
$dirListas =~ s/^~(\w*)/$ENV{HOME}/e;


my $log_Apache = $ARGV[0] or die "Leer log de apache\n";
my $log_ApacheError = $ARGV[1];
my $log_postgres = $ARGV[2];
my $msj_actual = $ARGV[3];
my $rutaAccess=$dirParsedApache.$log_Apache;
my @arreglo;

my $cont_PATH = 0;
my $cont_XSS = 0;
# para el SQLi
my $RegEX = ("ALTER |CREATE |DELETE |DROP |EXEC |INSERT INTO|MERGE |SELECT |UPDATE |UNION |OR |AND |ORDER BY|WHERE |HAVING ");
my $i=1;
my $cont_encuentros = 0;
my $cont_error = 0;
my $cont_200 = 0;
my $cont_error_en_base = 0;
my $cont_errores_postgres = 0;
my $filename3 = "SQLi_apache.txt";
open(my $new_error_apache, '>', $dirParsedApache.$filename3) or die "Could not open file '$filename3' $!";

#$diagnostico = Crawler::analizarCrawling(\%ips,$dirListas,$frecPromPeticionSeg,$toleranciaSegundos,$duracionSeg);
# Abrimos el archivo de los logs
open(my $data_acces, '<', $rutaAccess) or die "No se puede abrir el archivo $rutaAccess\n";

open(my $new_msj, '>>', $ENV{HOME}."/Proyecto/mensaje.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $status, '>>', $ENV{HOME}."/Proyecto/cod_status.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $stauts2, '>', $ENV{HOME}."/Proyecto/status_act.txt") or die "Could not open file 'status_act.txt' $!";
print $new_msj "#####################################Mensaje: ".$msj_actual."######################################################\n";

while (my $line1 = <$data_acces>)
{
    chomp $line1;
    # Obtenemos la informacion de la linea en un arreglo

    #$arreglo[0] = IP Cliente
    #$arreglo[1] = Fecha 05/Oct/2016:09:16:01
    #$arreglo[2] = Metodo HTTP
    #$arreglo[3] = Recurso
    #$arreglo[4] = Version HTTP
    #$arreglo[5] = Codigo de respuesta
    #$arreglo[6] = Tamanio de respuesta
    #$arreglo[7] = Referencia
    #$arreglo[8] = User-Agent

	@arreglo= split (/<-->/, $line1);
	# Checando que exista algun metodo
    if ($arreglo[2] ne "-")
	{
		$recurso=$arreglo[3];
	}
	# Detectando si esta el caracter nulo codificado
	if($recurso =~ /%00/)
	{
		$nullFlag=1;
	}
	# Detectando si hay un caracter codificado
	if($recurso =~ /%[0-9|a-f|A-F][0-9|a-f|A-F]/)
	{
		$recurso=utilerias::urlDecoder($recurso);		    
	}
	# Si analizarPT devuelve 0, no encontro nada, si retorna 1 solo encontro un ataque PT en el access.log, si hay 2 encontro algo en el access.log y error.log
	$diagnostico_PATH = PathTransversal::analizarPT($recurso,$arreglo[1],$arreglo[5],$dirListas,$dirParsedApacheError,$log_ApacheError,$toleranciaError);

	#print "Resultado Path Transversal: $diagnostico\n";
	#print "Si el resultado es 0, no encontro nada, si es 1 solo encontro un ataque PT en el access.log, si es 2 encontro algo en el access.log y error.log\n";

	if($diagnostico_PATH == 0)
	{
		#Si analizarXSS devuelve 0, no encontro nada, si retorna 1 solo encontro un ataque XSS en el access.log, si hay 2 encontro algo en el access.log y error.log
		$diagnostico_XSS = XSS::analizarXSS($recurso,$arreglo[1],$arreglo[5],$dirListas,$dirParsedApacheError,$log_ApacheError,$toleranciaError);
		#print "Resultado XSS: $diagnostico_XSS\n";
		#print "Si el resultado es 0, no encontro nada, si es 1 solo encontro un ataque XSS en el access.log, si es 2 encontro algo en el access.log y error.log\n"
	}
	else
	{
		$cont_PATH++;
		print $new_msj "#-------------------------------PATH TRANSVERSAL----------------------------------#\n";
		print $new_msj "IP:		$arreglo[3]		User-Agent:	$arreglo[8]\n";
		print $new_msj "$arreglo[3]\n";
		print $new_msj "#---------------------------------------------------------------------------------#\n";
	}
	if($diagnostico_XSS == 0)
	{
		my ($aux1, $aux2, $aux3, $aux4) = SQLi::analizarSQLi($line1, $arreglo[1], $arreglo[3], $arreglo[5], $arreglo[7], $arreglo[8], $RegEX, $new_error_apache, $dirParsedPostgres.$log_postgres);
		$cont_encuentros += $aux1;
		$cont_error += $aux2;
		$cont_200 += $aux3;
		$cont_error_en_base += $aux4;
		if ($aux1 != 0)
		{
			print $new_msj "#-------------------------------SQL INJECTION-------------------------------------#\n";
			print $new_msj "IP:		$arreglo[3]		User-Agent:	$arreglo[8]\n";
			print $new_msj "$arreglo[3]\n";
			print $new_msj "$arreglo[7]\n";
			print $new_msj "#---------------------------------------------------------------------------------#\n";
		}
	}
	else
	{
		$cont_XSS++;
		print $new_msj "#-------------------------------CROSS SITE SCRIPTING------------------------------#\n";
		print $new_msj "IP:		$arreglo[3]		User-Agent:	$arreglo[8]\n";
		print $new_msj "$arreglo[3]\n";
		print $new_msj "#---------------------------------------------------------------------------------#\n";
	}

    if($diagnostico_XSS == 0 && $arreglo[7] eq "-")
	{
	    #Checando que exista la ip $arreglo[0]
	    if( exists($ips{$arreglo[0]} ) )
		{

			#Checando que exista el User-Agent $arreglo[8]
			if( exists($ips{$arreglo[0]}{$arreglo[8]} ) )
			{

				#Checando que exista la fecha $arreglo[1]
				if( exists($ips{$arreglo[0]}{$arreglo[8]}{$arreglo[1]} ) )
				{
					$refSolicitudes = $ips{$arreglo[0]}{$arreglo[8]}{$arreglo[1]};
					push(@$refSolicitudes, $arreglo[3]." ".$arreglo[5]);
				}
				else
				{
					#No existe la fecha
					my @solicitudes =();
					push(@solicitudes,$arreglo[3]." ".$arreglo[5]);
					$refTiempo= $ips{$arreglo[0]}{$arreglo[8]};
					$$refTiempo{$arreglo[1]} = \@solicitudes;
				}
			}
			else
			{
				#No existe el User-Agent $arreglo[8]
				my @solicitudes =();
				push(@solicitudes,$arreglo[3]." ".$arreglo[5]);
				my %tiempo = ();
				$tiempo{$arreglo[1]} = \@solicitudes;
				$refUserAgent = $ips{$arreglo[0]};
				$$refUserAgent{$arreglo[8]} = \%tiempo;
			}
	    }
		else
		{
			#No existe la ip $arreglo[0]
			my @solicitudes = ();
			push(@solicitudes,$arreglo[3]." ".$arreglo[5]);
	        my %tiempo = ();
        	$tiempo{$arreglo[1]} = \@solicitudes;
	        my %userAgent= ();
	        $userAgent{$arreglo[8]} = \%tiempo;
        	$ips{$arreglo[0]} = \%userAgent;
		}
	}
}
$nullFlag=0;

print $new_msj "#####################################Mensaje: ".$msj_actual." END #################################################\n";

$cont_errores_postgres = SQLi::errorPostgres($dirParsedPostgres.$log_postgres);
print $status "$cont_PATH ; $cont_XSS ; $cont_encuentros ; $cont_error ; $cont_200 ; $cont_errores_postgres ; $cont_error_en_base\n";
print $stauts2 "$cont_PATH;$cont_XSS;$cont_encuentros";
print "$cont_PATH ; $cont_XSS ; $cont_encuentros\n";
close $data_acces;

