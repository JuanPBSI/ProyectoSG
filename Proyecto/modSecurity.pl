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

foreach my $id(keys %alertas){
    print "ID: $id $alertas{$id}\n\n";
}
