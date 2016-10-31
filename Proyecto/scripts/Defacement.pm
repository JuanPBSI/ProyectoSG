package Defacement;
use strict;


sub analizarDefacement{
    my $metodo=$_[0];
    my $codigo=$_[1];
    my $diagnostico=0;
    if($metodo =~/PUT/i || $metodo =~/DELETE/i ){
	if ($codigo =~/^20[0-8]$/){
	    $diagnostico=1;
	}else{
	    $diagnostico=2;
	}
    }
    return $diagnostico;
}
1;
