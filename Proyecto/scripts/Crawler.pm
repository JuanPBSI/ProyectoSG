package Crawler;
use strict;
use scripts::utilerias;
use Date::Parse;


sub analizarCrawling{
    my $ipHash = $_[0];
    my $userAgentH;
    my $tiempoHash;
    my $recursosArray;
    my $listaSpidering=$_[1]."spidering_blacklist.txt";
    my $listaUserAgent=$_[1]."userAgent_whitelist.txt";
    my $tamanioHash;
    my $frecPromPeticiones=$_[2];
    my $toleranciaSegundos=$_[3];
    my $duracionSeg=$_[4];
    my %hashResultados;
    my $tiempoEpochAnterior = 0;
    my $linea;
    my $contadorLapso = 0;
    my $sumatoriaFrec = 0;
    my $numTotalPeticiones = 0;
    my %recursosDistintos = ();
    my $numRecursosDistintos = 0;
    my $recurso;
    my $promedio = 0;
    my $flagSpidering=0;	
    my $limite;
    my @spideringBot;
    my @crawler;
    my $tiempoInicio;
    my $tiempoFin;
    my $llave;
    #Iterando sobre las IP's
    foreach my $ip ( keys %$ipHash ){
	$userAgentH = $$ipHash{$ip};
	#Iterando sobre los User-Agent usados por la misma IP
        foreach my $userAgent ( keys %$userAgentH ){
	    $tiempoHash =  $$userAgentH{$userAgent};
	    $tamanioHash = keys %$tiempoHash;
	    if( $tamanioHash >= $duracionSeg){
		$tiempoInicio="";
		#Iterando sobre el hash de tiempos de la actividad que hubo desde el User-Agent y la misma IP
		foreach my $tiempo ( sort keys %$tiempoHash ){
		    $recursosArray =  $$tiempoHash{$tiempo};
		    #Checando cuanto tiempo transcurrió de una petición a otra, si sobrepasa de la tolerancia se reinician los conteos los cuales se hacen en el else
		    if(  (str2time($tiempo) - $tiempoEpochAnterior <= $toleranciaSegundos)  || ($contadorLapso == 0) ){
			$contadorLapso = $contadorLapso + 1;
			$sumatoriaFrec = $sumatoriaFrec	+ @$recursosArray;
			if($tiempoInicio eq ""){
			    $tiempoInicio=$tiempo;
			}
                   	foreach (@$recursosArray){
			    $recurso=$_;
			    if(! exists $recursosDistintos{$recurso}){
 			        $recursosDistintos{$recurso}=$recurso;
			    }
        	        }
			
			
		    }else{
			#Se analiza la información generada en el if anterior  para determinar si es un crawler, un DOS o un spidering-bot de un buscador.
			if($contadorLapso >= $duracionSeg){
		        #Se checa si el ataque de crawling no fue continuo, es decir que NO se haya tenido un comportamiento anomalo desde la primer petición hasta la última
			    $promedio= $sumatoriaFrec/$contadorLapso;
			    #Verificando si hubieron muchas peticiones
			    if($promedio >=$frecPromPeticiones){

				#Checando que se trate de algun spidering-bot por medio del User Agent se analiza si hace match con algo de la lista negra
				#Usamos last en el while para salirnos del ciclo una vez que haya una coincidencia con la lista negra y ahorrar tiempo de ejecucion
				open (LISTA, "$listaSpidering") or die "ERROR: No se encuentra la lista negra: $listaSpidering";
			        while (<LISTA>) {
			            $linea=$_;
			            chop ($linea);
				    if($linea eq $userAgent){
					$flagSpidering=1;
				 	last;
				    }				    
				}
				#Usamos last  para salirnos del ciclo foreach que itera sobre el hash de los tiempos una vez que se detecta un comportamiento raro para ahorrar tiempo de ejecucion
				if($flagSpidering == 1){
				    $llave = "[Spidering-Bot] [$ip] [$userAgent] [$tiempoInicio - $tiempo]";
				    $hashResultados{$llave} = \%recursosDistintos;
				    last;
				}else{
				    $numRecursosDistintos = keys %recursosDistintos; 
				    if( $numRecursosDistintos > 1){
				        $llave = "[Crawler] [$ip] [$userAgent] [$tiempoInicio - $tiempo]";
				        $hashResultados{$llave} = \%recursosDistintos;
					last;
				    }
				}
			    }
			}
			#No hubo un comportamiento de un crawler
			$tiempoEpochAnterior = 0;
			$contadorLapso = 0;
			$sumatoriaFrec = 0;
			$numTotalPeticiones = 0;
			$numRecursosDistintos = 0;
			$tiempoInicio="";	
			my %recursosDistintos=();		
		    }
	  	    $tiempoEpochAnterior= str2time($tiempo);
		    $tiempoFin=$tiempo;
	        }
     		#Se busca el comportamiento de un crawler, se realiza un analisis profundo para determinar si es un crawler, un DOS o un spidering-bot de un buscador.
		if($contadorLapso >= $duracionSeg ){
		#En este punto hay un ataque que fué continuo, es decir que se tuvo un comportamiento anomalo desde la primer petición hasta la última
		    $promedio= $sumatoriaFrec/$contadorLapso;
                    #Verificando si hubieron muchas peticiones
                    if($promedio >=$frecPromPeticiones){

			#Checando que se trate de algun spidering-bot por medio del User Agent se analiza si hace match con algo de la lista negra
			open (LISTA, "$listaSpidering") or die "ERROR: No se encuentra la lista negra: $listaSpidering";
                        while (<LISTA>) {
                            $linea=$_;
                            chop ($linea);
                            if($linea eq $userAgent){
                                $flagSpidering=1;
                                last;
                             }
                        }
                        if($flagSpidering == 1){
				    $llave = "[Spidering-Bot] [$ip] [$userAgent] [$tiempoInicio - $tiempoFin]";
				    $hashResultados{$llave} = \%recursosDistintos;
                        }else{
                            $numRecursosDistintos = keys %recursosDistintos;
                            if( $numRecursosDistintos > 1){
				$llave = "[Crawler] [$ip] [$userAgent] [$tiempoInicio - $tiempoFin]";
			        $hashResultados{$llave} = \%recursosDistintos;
                            }
                        }
                    }
		}
                #No hubo un comportamiento de un crawler
	        $tiempoEpochAnterior = 0;
                $contadorLapso = 0;
                $sumatoriaFrec = 0;
                $numTotalPeticiones = 0;
	        $numRecursosDistintos = 0;
		$tiempoInicio="";                
            	my %recursosDistintos=();		
	    }
     	}
    }
    return \%hashResultados;
}

1;
