#!/usr/bin/perl
use strict;
#use warnings;

use scripts::XSS;
use scripts::PathTraversal;
use scripts::utilerias;
use scripts::Crawler;
use scripts::SQLi;
use scripts::Defacement;

#Variables para leer el archivo de configuracion
my $config_file= "./config.conf";
my %Config = ();
utilerias::read_config_file($config_file, \%Config);
my $toleranciaError=$Config{'toleranciaError'};
my $analizarXSS=$Config{'analizarXSS'};
my $analizarSQLi=$Config{'analizarSQLi'};
my $analizarCrawler=$Config{'analizarCrawler'};
my $analizarDefacement=$Config{'analizarDefacement'};
my $analizarPathTrasversal=$Config{'analizarPathTrasversal'};


#Datos para el crawler
my $frecPromPeticionSeg=$Config{'frecPromPeticionSeg'};
my $toleranciaSegundos=$Config{'toleranciaSegundos'};
my $duracionSeg=$Config{'duracionSeg'};

#En el archivo de configuracion usa el comodin  ~ en referencia al directorio HOME, Perl no puede interpretar la tilde como el directorio, para ello la sustituimos ~ por la variable de
#entorno de Perl  que contiene el directorio HOME del usuario

my $dirListas = "./listas/";
my $log_Apache = $ARGV[0] or die "Leer log de apache\n";
my $log_ApacheError = $ARGV[1];
my $log_postgres = $ARGV[2];
my $msj_actual = $ARGV[3];
my $dirActual = $ARGV[4];
my @arreglo;
my $dirApacheAccess = "./parsedLogs/".$dirActual."/AccessWaf/";
my $dirApacheError = "./parsedLogs/".$dirActual."/ErrorWeb/";

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
#Diego inicia
my @arrayHerramientas;
my $nombreHerramienta;
#Diego fin
my $recursoDecodificado;
my %hashCrawler;
my $crawler;
my $spideringBot;

my $cont_PATH = 0;
my $cont_XSS = 0;
my $cont_CRAW = 0;
my $cont_DEF = 0;
# para el SQLi
my $RegEX = ("ALTER |CREATE |DELETE |DROP |EXEC |INSERT INTO|MERGE |SELECT |UPDATE |UNION |OR |AND |ORDER BY|WHERE |HAVING ");
my $i=1;
my $cont_encuentros = 0;
my $cont_encuentros_ref = 0;
my $cont_encuentros_user = 0;
my $cont_encuentros_mail = 0;
my $cont_error = 0;
my $cont_200 = 0;
my $cont_error_en_base = 0;
my $cont_errores_postgres = 0;
my $filename3 = "SQLi_apache.txt";
open(my $new_error_apache, '>', $dirApacheAccess.$filename3) or die "Could not open file '$filename3' $!";

#$diagnostico = Crawler::analizarCrawling(\%ips,$dirListas,$frecPromPeticionSeg,$toleranciaSegundos,$duracionSeg);
# Abrimos el archivo de los logs
open(my $data_acces, '<', $dirApacheAccess.$log_Apache) or die "No se puede abrir el archivo: $dirApacheAccess$log_Apache\n";

open(my $new_msj_SQLi, '>>', "./mensajeSQL.html") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_XSS, '>>', "./mensajeXSS.html") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_PATH, '>>', "./mensajePATH.html") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_CRAW, '>>', "./mensajeCRAW.html") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_DEFC, '>>', "./mensajeDEFC.html") or die "Could not open file 'mensaje.txt' $!";

open(my $new_msj_SQLi2, '>', "./mensajeSQL.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_XSS2, '>', "./mensajeXSS.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_PATH2, '>', "./mensajePATH.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_CRAW2, '>', "./mensajeCRAW.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_DEFC2, '>', "./mensajeDEFC.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_crawler, '>', "./CrawlerData.txt") or die "Could not open file 'mensaje.txt' $!";

open(my $new_msj_SQLi3, '>>', "extra/mensajeSQL.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_XSS3, '>>', "extra/mensajeXSS.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_PATH3, '>>', "extra/mensajePATH.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_CRAW3, '>>', "extra/mensajeCRAW.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_DEFC3, '>>', "extra/mensajeDEFC.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_crawler2, '>>', "extra/CrawlerData.txt") or die "Could not open file 'mensaje.txt' $!";

open(my $status, '>>', "./cod_status.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $stauts2, '>', "./status_act.txt") or die "Could not open file 'status_act.txt' $!";
#print $new_msj "#####################################Mensaje: ".$msj_actual."######################################################\n";

my @Sqli;
my @XSS;
my @DEFC;
my @Path;
my @Craw;


#Diego Inicia
#Cargamos la lista de nombres de herramientas a un array

open(my $listaHerramientas, '<', $dirListas."herramientas.txt") or die "No se puede abrir el archivo: $dirApacheAccess herramientas.txt\n";
while (my $nHerramienta = <$listaHerramientas>)
{
    chomp $nHerramienta;
    push(@arrayHerramientas,$nHerramienta);
}
close $listaHerramientas;
#Diego fin
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
	my @arreglo2 = split (/<-->/, $line1);
	$arreglo2[3] =~ s/\</\&lt/;
	$arreglo2[3] =~ s/\>/\&gt/;
	#Checando que exista algun metodo
    #if ($arreglo[2] ne "-" && $arreglo[7] eq "-")
	if ($arreglo[2] ne "-" && $arreglo[7] eq "-")
	{
		$recurso=$arreglo[3];
	}
	# Detectando si esta el caracter nulo codificado
	# Detectando si hay un caracter codificado
	#if($recurso =~ /%[0-9|a-f|A-F][0-9|a-f|A-F]/)
	if($recurso =~ /%[0-9|a-f|A-F][0-9|a-f|A-F]/ || $recurso =~ /data:.*;base64,(.*)/i)
	{
		$recursoDecodificado=utilerias::urlDecoder($recurso);	    
	}
	else{
		$recursoDecodificado = $recurso
	}
	if($analizarPathTrasversal == 1)
	{
		#Si analizarPT devuelve 0, no encontro nada, si retorna 1 solo encontro un ataque PT en el access.log, si hay 2 encontro algo en el access.log y error.log
		$diagnostico_PATH = PathTraversal::analizarPT($recurso,$recursoDecodificado,$arreglo[1],$arreglo[5],$dirListas,$dirApacheError,$log_ApacheError,$toleranciaError);
	}
	if($diagnostico_PATH == 0 && $analizarXSS == 1)
	{
	    #Si analizarXSS devuelve 0, no encontro nada, si retorna 1 solo encontro un ataque XSS en el access.log, si hay 2 encontro algo en el access.log y error.log
		$diagnostico_XSS = XSS::analizarXSS($recursoDecodificado,$arreglo[1],$arreglo[5],$dirListas,$dirApacheError,$log_ApacheError,$toleranciaError);
		#print "Resultado XSS: $diagnostico_XSS\n";
		#print "Si el resultado es 0, no encontro nada, si es 1 solo encontro un ataque XSS en el access.log, si es 2 encontro algo en el access.log y error.log\n"
	}
	else
	{
		#Diego Inicia
		$nombreHerramienta = utilerias::detectarHerramienta($line1,\@arrayHerramientas);
		#Diego Fin
		$cont_PATH++;
		#print $new_msj "#-------------------------------PATH TRANSVERSAL----------------------------------#\n";
		#print $new_msj "IP:		$arreglo[3]		User-Agent:	$arreglo[8]\n";
		#print $new_msj "$arreglo[3]\n";
		#print $new_msj "#---------------------------------------------------------------------------------#\n";
		print $new_msj_PATH2  "$arreglo[0]|$arreglo[1]|$arreglo[8]|$dirActual\n";
		print $new_msj_PATH3  "$arreglo[0]|$arreglo[1]|$arreglo[8]|$dirActual\n";
		print $new_msj_PATH "			<tr>\n";
		print $new_msj_PATH '				<td style="width:8%;">'."$arreglo[0]</td>\n";
		print $new_msj_PATH '				<td style="width:8%;">'."$arreglo[1]</td>\n";
		print $new_msj_PATH '				<td style="width:4%;">'."$arreglo[2]</td>\n";
		#print $new_msj_PATH '				<td style="width:30%; text-align:left;">'."$recursoDecodificado</td>\n";
		print $new_msj_PATH '				<td style="width:30%; text-align:left;">'."$arreglo2[3]</td>\n";
		print $new_msj_PATH '				<td style="width:21%; text-align:left;">'."$arreglo[7]</td>\n";
		if(($arreglo[5] =~ /4..\b/i) || ($arreglo[5] =~ /5..\b/i))
		{
			print $new_msj_PATH '				<td style = "width:4%; color : red; font-weight: bold;">'."$arreglo[5]</td>\n";
		}
		elsif($arreglo[5] =~ /2..\b/i)
		{
			print $new_msj_PATH '				<td style = "width:4%; color : green; font-weight: bold;">'."$arreglo[5]</td>\n";
		}
		print $new_msj_PATH '				<td style="width:4%;">'."$arreglo[6]</td>\n";
		print $new_msj_PATH '				<td style="width:21%; text-align:left;" id="User-Agent">'."$arreglo[8]</td>\n";
		#Diego Inicia
		print $new_msj_PATH '				<td style="width:10%; text-align:left;" id="Herramienta Detectada">'."$nombreHerramienta</td>\n";
		#Diego Fin
		print $new_msj_PATH "			</tr>\n";
	}
	if($diagnostico_XSS == 0 && $diagnostico_PATH == 0)
	{
		my ($aux1, $aux2, $aux3, $aux4, $aux5, $aux6, $aux7) = SQLi::analizarSQLi($line1, $arreglo[1], $arreglo[3], $arreglo[5], $arreglo[7], $arreglo[8], $RegEX, $new_error_apache, $log_postgres);
		$cont_encuentros += $aux1;
		$cont_encuentros_ref += $aux2;
		$cont_encuentros_user += $aux3;
		$cont_error += $aux4;
		$cont_200 += $aux5;
		$cont_error_en_base += $aux6;
		$cont_encuentros_mail += $aux7;
		if ($aux1 != 0 or $aux2 !=0 or $aux3 !=0)
		{
			#Diego Inicia
			$nombreHerramienta = utilerias::detectarHerramienta($line1,\@arrayHerramientas);
			#Diego Fin
			$diagnostico_SQLi = 1;
			#print $new_msj "#-------------------------------SQL INJECTION-------------------------------------#\n";
			#print $new_msj "IP:		$arreglo[3]		User-Agent:	$arreglo[8]\n";
			#print $new_msj "$arreglo[3]\n";
			#print $new_msj "$arreglo[7]\n";
			#print $new_msj "#---------------------------------------------------------------------------------#\n";
			print $new_msj_SQLi2 "$arreglo[0]|$arreglo[1]|$arreglo[8]|$dirActual\n";
			print $new_msj_SQLi3 "$arreglo[0]|$arreglo[1]|$arreglo[8]|$dirActual\n";
			print $new_msj_SQLi "			<tr>\n";
			print $new_msj_SQLi '				<td style="width:8%;">'."$arreglo[0]</td>\n";
			print $new_msj_SQLi '				<td style="width:8%;">'."$arreglo[1]</td>\n";
			print $new_msj_SQLi '				<td style="width:4%;">'."$arreglo[2]</td>\n";
			print $new_msj_SQLi '				<td style="width:30%; text-align:left;">'."$arreglo2[3]</td>\n";
			print $new_msj_SQLi '				<td style="width:21%; text-align:left;">'."$arreglo[7]</td>\n";
			if(($arreglo[5] =~ /4..\b/i) || ($arreglo[5] =~ /5..\b/i))
			{
				print $new_msj_SQLi '				<td style = "width:4%; color : red; font-weight: bold;">'."$arreglo[5]</td>\n";
			}
			elsif($arreglo[5] =~ /2..\b/i)
			{
				print $new_msj_SQLi '				<td style = "width:4%; color : green; font-weight: bold;">'."$arreglo[5]</td>\n";
			}
			print $new_msj_SQLi '				<td style="width:4%;">'."$arreglo[6]</td>\n";
			if ($aux4 == 1)
			{
				print $new_msj_SQLi '				<td style = "width:4%; color : red; font-weight: bold;">'."SI</td>\n";
			}
			else
			{
				print $new_msj_SQLi '				<td style = "width:4%; color : green; font-weight: bold;">'."NO</td>\n";
			}
			print $new_msj_SQLi '				<td style="width:17%; text-align:left;">'."$arreglo[8]</td>\n";
			#Diego Inicia
			print $new_msj_SQLi '				<td style="width:10%; text-align:left;">'."$nombreHerramienta</td>\n";
			#Diego Fin
			print $new_msj_SQLi "			</tr>\n";
		}
		else
		{
			$diagnostico_SQLi = 0;
		}
	}
	elsif($diagnostico_XSS > 0)
	{
		#Diego Inicia
		$nombreHerramienta = utilerias::detectarHerramienta($line1,\@arrayHerramientas);
		#Diego Fin
		$cont_XSS++;
		#print $new_msj "#-------------------------------CROSS SITE SCRIPTING------------------------------#\n";
		#print $new_msj "IP:		$arreglo[3]		User-Agent:	$arreglo[8]\n";
		#print $new_msj "$arreglo[3]\n";
		#print $new_msj "#---------------------------------------------------------------------------------#\n";
		print $new_msj_XSS2  "$arreglo[0]|$arreglo[1]|$arreglo[8]|$dirActual\n";
		print $new_msj_XSS3  "$arreglo[0]|$arreglo[1]|$arreglo[8]|$dirActual\n";
		print $new_msj_XSS "			<tr>\n";
		print $new_msj_XSS '				<td style="width:8%;">'."$arreglo[0]</td>\n";
		print $new_msj_XSS '				<td style="width:8%;">'."$arreglo[1]</td>\n";
		print $new_msj_XSS '				<td style="width:4%;">'."$arreglo[2]</td>\n";
		print $new_msj_XSS '				<td style="width:30%; text-align:left;">'."$arreglo2[3]</td>\n";
		print $new_msj_XSS '				<td style="width:21%; text-align:left;">'."$arreglo[7]</td>\n";
		if(($arreglo[5] =~ /4..\b/i) || ($arreglo[5] =~ /5..\b/i))
		{
			print $new_msj_XSS '				<td style = "width:4%; color : red; font-weight: bold;">'."$arreglo[5]</td>\n";
		}
		elsif($arreglo[5] =~ /2..\b/i)
		{
			print $new_msj_XSS '				<td style = "width:4%; color : green; font-weight: bold;">'."$arreglo[5]</td>\n";
		}
		print $new_msj_XSS '				<td style="width:4%;">'."$arreglo[6]</td>\n";
		print $new_msj_XSS '				<td style="width:21%; text-align:left;">'."$arreglo[8]</td>\n";
		#Diego Inicia
		print $new_msj_XSS '				<td style="width:10%; text-align:left;">'."$nombreHerramienta</td>\n";
		#Diego Fin
		print $new_msj_XSS "			</tr>\n";
	}
	if($diagnostico_PATH == 0 && $analizarDefacement == 1 && $diagnostico_XSS == 0 && $diagnostico_SQLi == 0)
	{
	    $diagnostico_DEF = Defacement::analizarDefacement($arreglo[2],$arreglo[5]);
		if($diagnostico_DEF > 0)
		{
			$nombreHerramienta = utilerias::detectarHerramienta($line1,\@arrayHerramientas);
			$cont_DEF++;
			print $new_msj_DEFC2  "$arreglo[0]|$arreglo[1]|$arreglo[8]|$dirActual\n";
			print $new_msj_DEFC3  "$arreglo[0]|$arreglo[1]|$arreglo[8]|$dirActual\n";
			print $new_msj_DEFC "			<tr>\n";
			print $new_msj_DEFC '				<td style="width:10%;">'."$arreglo[2]</td>\n";
			print $new_msj_DEFC '				<td style="width:80%; text-align:left;">'."$arreglo2[3]</td>\n";
			if(($arreglo[5] =~ /4..\b/i) || ($arreglo[5] =~ /5..\b/i))
			{
				print $new_msj_DEFC '				<td style = "width:10%; color : red; font-weight: bold;">'."$arreglo[5]</td>\n";
			}
			elsif($arreglo[5] =~ /2..\b/i)
			{
				print $new_msj_DEFC '				<td style = "width:10%; color : green; font-weight: bold;">'."$arreglo[5]</td>\n";
			}
			#Diego Inicia
			print $new_msj_DEFC '				<td style = "width:10%; color : green; font-weight: bold;">'."$nombreHerramienta</td>\n";
			#Diego Fin
			print $new_msj_DEFC "			</tr>\n";
		}
	}

	if( ($analizarCrawler == 1) && ($diagnostico_PATH == 0 && $diagnostico_DEF == 0 && $diagnostico_XSS == 0 && $diagnostico_SQLi == 0) && (  ($recursoDecodificado ne "" &&  $recursoDecodificado =~/^[a-z0-9\.\-_\/#]*$/i ) || ($recursoDecodificado eq "" && $recurso =~ /^[a-z0-9\.\-_\/#]*$/i ) ) )
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
                        if($recursoDecodificado ne ""){
			#Diego Inicia
                            push(@$refSolicitudes,"[$recursoDecodificado][$arreglo[5]]");
			#Diego Fin
                        }else{
				#Diego Inicia
                            push(@$refSolicitudes,"[$recurso][$arreglo[5]]");
				#Diego Fin
                        }
            	}
				else
				{
	                #No existe la fecha
        	        my @solicitudes =();
                        if($recursoDecodificado ne ""){
			        #Diego Inicia
			    push(@$refSolicitudes,"[$recursoDecodificado][$arreglo[5]]");
			#Diego Fin

                        }else{
                            push(@$refSolicitudes,"[$recurso][$arreglo[5]]");
                        }
					$refTiempo= $ips{$arreglo[0]}{$arreglo[8]};
	       	        $$refTiempo{$arreglo[1]} = \@solicitudes;
				}
        	}
			else
			{
	            #No existe el User-Agent $arreglo[8]
        	    my @solicitudes =();
                        if($recursoDecodificado ne ""){
			 #Diego Inicia
                            push(@$refSolicitudes,"[$recursoDecodificado][$arreglo[5]]");
			#Diego Fin
                        }else{
			    #Diego Inicia
                            push(@$refSolicitudes,"[$recurso][$arreglo[5]]");
			#Diego Fin
                        }
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
                        if($recursoDecodificado ne ""){
			 #Diego Inicia
                            push(@$refSolicitudes,"[$recursoDecodificado][$arreglo[5]]");
			#Diego Fin
                        }else{
			 #Diego Inicia
                            push(@$refSolicitudes,"[$recurso][$arreglo[5]]");
			#Diego Fin
                        }
	        my %tiempo = ();
        	$tiempo{$arreglo[1]} = \@solicitudes;
	        my %userAgent= ();
	        $userAgent{$arreglo[8]} = \%tiempo;
        	$ips{$arreglo[0]} = \%userAgent;
		}
	}
}

#print $new_msj "#####################################Mensaje: ".$msj_actual." END #################################################\n";

close $data_acces;

if($analizarCrawler == 1 )
{
    %hashCrawler= %{Crawler::analizarCrawling(\%ips,$dirListas,$frecPromPeticionSeg,$toleranciaSegundos,$duracionSeg)};
	if(keys %hashCrawler > 0)
	{
		$cont_CRAW++;
	}
    foreach my $ipUserAgent(keys %hashCrawler)
	{
		print $new_msj_CRAW2  "$ipUserAgent|$dirActual\n";
		print $new_msj_CRAW3  "$ipUserAgent|$dirActual\n";
		print $new_msj_CRAW '		<thead>';
		print $new_msj_CRAW '		<tr>';
		print $new_msj_CRAW '			<th style="background:#BB9100; width:90%;" >'.$ipUserAgent.'</th>';
		print $new_msj_CRAW '			<th style="background:#BB9100; width:10%;" > </th>';
		print $new_msj_CRAW '		</tr>';
		print $new_msj_CRAW '		<tr>';
		print $new_msj_CRAW '			<th style="width:90%;" >Recurso</th>';
		print $new_msj_CRAW '			<th style="width:10%;" >Codigo</th>';
		print $new_msj_CRAW '		</tr>';
		print $new_msj_CRAW '		</thead>';
		print $new_msj_CRAW '		<tbody>';
		my %recursosDistintos = %{$hashCrawler{$ipUserAgent}};
        foreach my $recurso(keys %recursosDistintos)
		{
			if ( not (($recurso eq '') or ($recurso eq ' ')) )
			{
				#Diego Inicia
				print $new_crawler2 "$recurso $recursosDistintos{$recurso}.\n";
				#Diego Fin
				print $new_msj_CRAW "			<tr>\n";
				#Diego Inicia
				print $new_msj_CRAW '				<td style="width:90%; text-align:left;">'."$recurso</td>\n";
				if(($recursosDistintos{$recurso} =~ /4..\b/i) || ($recursosDistintos{$recurso} =~ /5..\b/i))
				{
					print $new_msj_CRAW '				<td style = "width:10%; color : red; font-weight: bold;">'."$recursosDistintos{$recurso}</td>\n";
				}
				elsif($recursosDistintos{$recurso} =~ /2..\b/i)
				{
					print $new_msj_CRAW '				<td style = "width:10%; color : green; font-weight: bold;">'."$recursosDistintos{$recurso}</td>\n";
				}
				else
				{
					print $new_msj_CRAW '				<td style = "width:10%; color : black; font-weight: bold;">'."$recursosDistintos{$recurso}</td>\n";
				}
				#Diego Fin
				print $new_msj_CRAW "			</tr>\n";
			}
        }
    }
}

my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$cont_errores_postgres = SQLi::errorPostgres($log_postgres);
#print $status "$cont_PATH;$cont_XSS;$cont_encuentros;$cont_error;$cont_200;$cont_errores_postgres;$cont_error_en_base\n";
if (($cont_PATH + $cont_XSS + $cont_encuentros + $cont_encuentros_ref + $cont_encuentros_user + $cont_DEF + $cont_CRAW + $cont_encuentros_mail) > 0 ) 
{
	print $status "\[$mday\/$mon\/$year $hour:$min:$sec\];$cont_PATH;$cont_XSS;$cont_encuentros;$cont_encuentros_ref;$cont_encuentros_user;$cont_DEF;$cont_CRAW;$cont_encuentros_mail\n";
}
my $sum = $cont_encuentros + $cont_encuentros_ref + $cont_encuentros_user;
print $stauts2 "$cont_PATH;$cont_XSS;$cont_encuentros;$cont_encuentros_ref;$cont_encuentros_user;$cont_DEF;$cont_CRAW;$cont_encuentros_mail";
print "Salida PATH: \[$cont_PATH\], XSS: \[$cont_XSS\], SQLi: \[$sum\], Defacement: \[$cont_DEF\], Crawler: \[$cont_CRAW\]\n";
