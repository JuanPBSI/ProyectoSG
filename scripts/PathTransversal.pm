package PathTransversal;
use strict;



#Esta subrutina solo checa que el recurso solicitado contenga alguna palabra definida en la lista negra
sub analizarPT{
    my $recurso=$_[0];
    my $tiempo=$_[1];
    my $codigoRespuesta=$_[2];
    my $listaNegra=$_[3]."PathTransversal_blacklist.txt";
    my $dirParsedApacheError=$_[4];
    my $log_ApacheError=$_[5];
    my $toleranciaError=$_[6];
    my $rutaURL;
    my $variablesURL;
    my $tiempoError;
    my $linea;
    my $url;
    my $contador=0;
    my $consulta;
    my $aux;
    my $flagLista=0;
    my $flagError=0;
    my $match;
    my $tiempoError;
    my $diagnostico=0;
    #Obteniendo variables de la URL
    # Ejemplo: /home/app.php?var1=a&?var2=b&?var3=c
    # Del ejemplo anterior se obtiene var1=a&?var2=b&?var3=c
    if($recurso =~ /.*\?(.*=.*)/ ){
        $variablesURL=$1;
        #Analizamos si alguna variable es sospechosa
        open (LISTA, "$listaNegra") or die "ERROR: No se encuentra la lista negra : $listaNegra";
        while (<LISTA>) {
    	    $linea=$_;
	    chop ($linea);          
	    # Verificando que alguna variable contenga una palabra de la lista negra
	    $match = 0;


	    #Se escapan los caracteres * . ? + ya que se usa grep y no los interpreta como caracter
	    $linea=~ s/\\/\\\\/g;
	    $linea=~ s/\//\\\//g;
	    $linea=~ s/\./\\\./g;
	    $linea=~ s/\?/\\\?/g;
	    $linea=~ s/\+/\\\+/g;

	    if($variablesURL =~ /.*$linea.*/){
		#print "[PT] Match con la palabra lista: ".$linea."\n";
		$flagLista=1;
		$match=1;
	    }
		#Verificando que exista un log de error de Apache las variables  $dirParsedApacheError y  $log_ApacheError estan declaradas en el script analizador, esto es valido
		# ya que llama a esta funcion
 	    
	    if($match == 1 && $log_ApacheError ne "-"  ){
 	        open my $logError, '<',  $dirParsedApacheError.$log_ApacheError or die "No se encuentra el log de error Apache cuyo nombre es: $dirParsedApacheError.$log_ApacheError";
  	        #Se cambia el formato de la marca de tiempo ya que en el log de access es distinta a la de error
#  	        $tiempo =~ m/([0-9]+)\/(.*)\/([0-9]+):(.*)/;
#		$tiempoError=$2." ".$1." ".$4. " ".$3;
	
                $tiempoError = "[";
                for( my $i = 1; $i <= $toleranciaError; $i = $i + 1 ){
                    $aux = utilerias::suma_segundo_hora($tiempo,$i);
                    $tiempoError =  $tiempoError . $aux;
                    if($i + 1 <= $toleranciaError){
                        $tiempoError =  $tiempoError . "|";
                    }
                }
                $tiempoError =  $tiempoError . "]";

 		 #Preparando el string que servira para hacer la consulta
		$consulta=".*" . $tiempoError . ".*";
		$consulta=$consulta . $linea . ".*";
		#print "\n Consulta: ". $consulta . "\n";
		my @lines =  grep /$consulta/i, <$logError>;
		#print "\n Perl PT Variable Grep: ".  @lines;
		if(@lines > 0){
		    $contador+=1;
		    $flagError=1;
		    #print "Contador: ".$contador."\n";
		}
	    }		
        }
	close(LISTA);
  

    #Si el recurso no contiene variables obtenemos la ruta solicitada, en este caso no se usa un diccionario ya que puede coincidir algún nombre de directorio que sea genuino
    #Ejemplo: /dir/dir1/../../../etc/passwd
    }elsif($url =~ /(\/.*\/.+)/ ){
        if($url =~ /.*\.\.\// ){
	    if($codigoRespuesta == 200){
   	        #print "PT por URL exitoso:  ". $tiempo. " ".$recurso."\n";
		$diagnostico=1;
	    }else{
 	        #print "PT por URL fallido:  ". $tiempo. " ".$recurso."\n";	
		$diagnostico=2;
	    }
	     
	}
    }
    if ($flagError == 1 ){
	#print "PT por Variables fallido:  ". $tiempo. " ".$recurso."\n";
	$diagnostico=1;
    }elsif ($flagLista == 1){
	#print "PT por Variables exitoso:  ". $tiempo. " ".$recurso."\n";
	$diagnostico=2;
    }
    return $diagnostico;
}

1;
