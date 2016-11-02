#!/usr/bin/perl
use strict;
use scripts::utilerias;


#Variables para leer el archivo de configuracion

#my $config_file= $ENV{HOME}."/Proyecto/herramienta.conf";
#my %Config = ();
#utilerias::read_config_file($config_file, \%Config);
#my $dir=$Config{'parsedLogAccess'};

####
#
#	MODO DE EJECUCION:  perl scripts/modSecurity.pl ruta/error.log ruta/modsec_audit.log
#	[+] NOTA: No ejecutar dentro del directorio scripts, sino un directorio fuera de scripts (Proyecto)
####

open(my $new_msj_SQLi, '>>', "./mensajeSQLmod.html") or die "Could not open file 'mensajeSQLmod.html' $!";
open(my $new_msj_XSS, '>>', "./mensajeXSSmod.html") or die "Could not open file 'mensajeXSSmod.html' $!";
open(my $new_msj_PATH, '>>', "./mensajePATHmod.html") or die "Could not open file 'mensajePATHmod.html' $!";

open(my $new_msj_SQLi3, '>>', "extra/mensajeSQLmod.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_XSS3, '>>', "extra/mensajeXSSmod.txt") or die "Could not open file 'mensaje.txt' $!";
open(my $new_msj_PATH3, '>>', "extra/mensajePATHmod.txt") or die "Could not open file 'mensaje.txt' $!";


my $logErrorPath = $ARGV[0] or die "Leer log de apache\n";
my $logAuditPath = $ARGV[1];
my $fecha;
my $ip;
my $mensaje;
my $hostname;
my $uri;
my $uniqueId;
my %alertas;
my $idTraza;
my $flagInicioTraza;
my $idTraza;
my $flagCoincideId;
my $flagBloqueB;
my $recurso;
my $userAgent;
# Abrimos el archivo error.log de apache
open(my $logError, '<', $logErrorPath) or die "No se puede abrir el archivo $logErrorPath\n";
open(my $ModSec, '>', "./ModSec.log") or die "Could not open file 'ModSec.log' $!";
open(my $ModSecReport, '>>', "./ModSecReport.log") or die "Could not open file 'ModSecReport.log' $!";
while (my $lineaError = <$logError>){
    chomp $lineaError;
#   Si se usa la expresion donde contiene las palabras "Inbound Anomaly Score Exceeded" significa que esun ataque y modsecurity da una conclusion, la expresion comentada solo da aquellos
#   posibles resultados sin llegar a una como conclusion, por ello se concatenan los mensajes
    if($lineaError =~ /\[(.*[0-9])\] .*\[client(.*[0-9])\] ModSecurity: .*\[msg \"Inbound Anomaly Score Exceeded \(.*\): (.*)\"\] \[hostname \"(.*)\"\] .*\[uri \"(.*)\"\] .*\[unique_id \"(.*)\"\]/){
#    if($lineaError =~ /\[(.*[0-9])\] .*\[client(.*[0-9])\] ModSecurity: .*\[msg \"(.*)\"\] \[data.*\[hostname \"(.*)\"\] .*\[uri \"(.*)\"\] .*\[unique_id \"(.*)\"\]/){
	$fecha=$1;
	$ip=$2;
	$mensaje=$3;
	$hostname=$4;
	$uri=$5;
	$uniqueId=$6;
	#Se hace una consulta en el AuditLog siempre y cuando no se haya consultado anteriormente, por ello se usa exists para ver si existe esa llave en el hash
	if(! exists $alertas{$uniqueId}){
	    open(my $logAudit, '<', $logAuditPath) or die "No se puede abrir el archivo $logAuditPath\n";	
  	    #Relacionando elevento en el AuditLog
 	    while (my $lineaAudit = <$logAudit>){
		#Buscamos el encabezado A
	        if( $lineaAudit =~/\-\-([0-9|A-F|a-f]*)\-A\-\-/ ){
		    $idTraza=$1;
		    $flagInicioTraza=1;
		    next;
		#Verificamos que el uniqueId del error log este en el audit log
		}elsif($flagInicioTraza == 1 && $lineaAudit =~ /.*$uniqueId.*$ip/ ){
		    $flagInicioTraza = 0;
		    $flagCoincideId = 1;
		    next;
		}
		#Verificamos que se inicia el bloque B para extraer la información que corresponda
		if( $flagCoincideId == 1 && $lineaAudit =~/\-\-$idTraza\-B\-\-/ ){
		    $flagBloqueB = 1;
		    next;
		}
		elsif($flagBloqueB == 1){
		    #Se termino el bloque B por lo tanto ya no se extrae mas informacion para ello se usa last, para terminar de leer el auditlog
		    if($lineaAudit =~/\-\-$idTraza\-[A-Z|a-z]\-\-/){
			$flagCoincideId = 0;
			$flagBloqueB = 0;
			$alertas{$uniqueId}="[$fecha] [$ip] [$userAgent] [$hostname] [$recurso] [$mensaje]";
			last;
		    }else{
			if($lineaAudit =~/.* (.*) HTTP.*/){
			    $recurso=$1;
			    next;
			}elsif($lineaAudit =~/User-Agent: (.*)/){
			    $userAgent=$1;
			    next;
			}
		    }
		}
	    }
	    close $logAudit;
#	}else{
	    #Si ya existe la id en el hash solo concatenamos el texto del campo de msg
#	    $alertas{$uniqueId} =~/\[(.*)\] \[(.*)\] \[(.*)\] \[(.*)\] \[(.*)\] \[(.*)\]/;
#	    $alertas{$uniqueId}="[$1] [$2] [$3] [$4] [$5] [$6 --> $mensaje]";
	}
    }    
}
close $logError;

my $cont_sql = 0;
my $cont_path = 0;
my $cont_xss = 0;
foreach my $id(keys %alertas){
    print $ModSec "ID: $id $alertas{$id}\n";
	print $ModSecReport "ID: $id $alertas{$id}\n";
	# Obtiene la informacion de modsecurity
	my $string = "ID: $id $alertas{$id}";
	my @parsed_fields = ($string =~ m/(?<=\[)[^]]+(?=\])/g);
	# identifica el tipo de ataque
	my $ifpath = ($parsed_fields[5] =~ m/path/ig);
	my $ifsql = ($parsed_fields[5] =~ m/sql/ig);
	my $ifxss = ($parsed_fields[5] =~ m/xss/ig);
	if ($ifpath)
	{
		$cont_path++;
		print $new_msj_PATH "			<tr>\n";
		print $new_msj_PATH '				<td style="width:10%;">'."$parsed_fields[1]</td>\n"	;
		print $new_msj_PATH '				<td style="width:15%;">'."$parsed_fields[0]</td>\n";
		print $new_msj_PATH '				<td style="width:50%; text-align:left;">'."$parsed_fields[4]</td>\n";
		print $new_msj_PATH '				<td style="width:25%; text-align:left;">'."$parsed_fields[2]</td>\n";
		print $new_msj_PATH "			</tr>\n";
	}
	if ($ifxss)
	{
		$cont_xss++;
		print $new_msj_XSS "			<tr>\n";
		print $new_msj_XSS '				<td style="width:10%;">'."$parsed_fields[1]</td>\n"	;
		print $new_msj_XSS '				<td style="width:15%;">'."$parsed_fields[0]</td>\n";
		print $new_msj_XSS '				<td style="width:50%; text-align:left;">'."$parsed_fields[4]</td>\n";
		print $new_msj_XSS '				<td style="width:25%; text-align:left;">'."$parsed_fields[2]</td>\n";
		print $new_msj_XSS "			</tr>\n";
	}
	if ($ifsql)
	{
		$cont_sql++;
		print $new_msj_SQLi "			<tr>\n";
		print $new_msj_SQLi '				<td style="width:10%;">'."$parsed_fields[1]</td>\n"	;
		print $new_msj_SQLi '				<td style="width:15%;">'."$parsed_fields[0]</td>\n";
		print $new_msj_SQLi '				<td style="width:50%; text-align:left;">'."$parsed_fields[4]</td>\n";
		print $new_msj_SQLi '				<td style="width:25%; text-align:left;">'."$parsed_fields[2]</td>\n";
		print $new_msj_SQLi "			</tr>\n";
	}
}
close($ModSec);
#my $detectModSec = `wc -l ModSec.log | cut -d" " -f 1`;
#chomp $detectModSec;
print "Detecciones ModSecurity --> PATH: \[$cont_path\], XSS: \[$cont_xss\], SQLi: \[$cont_sql\] Ver archivo: ModSec.log para mas información";