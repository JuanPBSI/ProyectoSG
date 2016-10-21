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
    my $diagnostico=0;
    my $tamanioHash;
    my $frecPromPeticiones=$_[2];
    my $toleranciaSegundos=$_[3];
    my $duracionSeg=$_[4];
    my $tiempoEpochAnterior="-";
    my $tiempoAux;
    my $contador;
    
    foreach my $key ( keys %$ipHash ){
	$userAgentH = $$ipHash{$key};
#	print "\n==============================IP: $key\n";
        foreach my $key2 ( keys %$userAgentH ){
	    $tiempoHash =  $$userAgentH{$key2};
#           print "\nUser-Agent: $key2\n";
	    $tamanioHash = keys %$tiempoHash;
	    if( $tamanioHash >= $duracionSeg){
		foreach my $key3 ( sort keys %$tiempoHash ){
#		    if($tiempoEpochAnterior ne "-" && (str2time($key3) - $tiempoEpochAnterior =< $toleranciaSegundos)  ){
		
#		    }
	  	    $tiempoEpochAnterior= str2time($key3);
		    $recursosArray =  $$tiempoHash{$key3};
#	            print "\nFecha: $key3\n";
#		    foreach (@$recursosArray){
#		        print $_ ."\n";
#		    }
#		    print "\n\n\n";
	        }
            }
     	}
    }
    return $diagnostico;
}

1;
