package Defacement;
use strict;


sub analizarDefacement{
    my $metodo=$_[0];
    my $diagnostico=0;
    if($metodo =~/PUT/i || $metodo =~/DELETE/i ){
	$diagnostico=1;
    }
    return $diagnostico;
}
1;
