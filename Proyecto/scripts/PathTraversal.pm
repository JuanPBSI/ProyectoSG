package PathTraversal;
use strict;



#Esta subrutina solo checa que el recurso solicitado contenga alguna palabra definida en la lista negra
sub analizarPT{
    my $recurso=$_[0];
    my $recursoDecodificado=$_[1];
    my $tiempo=$_[2];
    my $codigoRespuesta=$_[3];
    my $listaNegraVariable=$_[4]."PathTraversalVariable_blacklist.txt";
    my $listaNegraURL=$_[4]."PathTraversalURL_blacklist.txt";
    my $dirParsedApacheError=$_[5];
    my $log_ApacheError=$_[6];
    my $toleranciaError=$_[7];
    my $rutaURL;
    my $variablesURL;
    my $variablesURLDecodificadas;
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
    if($recursoDecodificado =~ /.*\?(.*=.*)/){
	$variablesURLDecodificadas=$1;
	$recurso =~ /.*\?(.*=.*)/;
        $variablesURL=$1;
        #Analizamos si alguna variable es sospechosa
        open (ListaVariable, "$listaNegraVariable") or die "ERROR: No se encuentra la lista negra : $listaNegraVariable";
        while (<ListaVariable>) {
    	    $linea=$_;
	    chop ($linea);          
	    # Verificando que alguna variable contenga una palabra de la lista negra
	    $match = 0;

	    #Se escapan los caracteres * . ? + ya que se evalua en una expresion regular y asi puedan ser  interpretados como caracter
	    if($linea  =~ /\\/){
		$linea=~ s/\\/\\\\/g;
	    }elsif($linea  =~ /\//){
	    	$linea=~ s/\//\\\//g;
	    }
	    $linea=~ s/\./\\\./g;
	    $linea=~ s/\?/\\\?/g;
	    $linea=~ s/\+/\\\+/g;
	    if( $variablesURLDecodificadas =~ /.*$linea.*/ || $variablesURL =~ /.*$linea.*/){
		#print "[PT] Match con la palabra lista: $linea\n";
		$flagLista=1;
		$match=1;
	    }
		#Verificando que exista un log de error de Apache las variables  $dirParsedApacheError y  $log_ApacheError estan declaradas en el script analizador, esto es valido
		# ya que llama a esta funcion
 	    
	    if($match == 1 && $log_ApacheError ne "-"  ){
 	        open my $logError, '<',  $dirParsedApacheError.$log_ApacheError or die "No se encuentra el log de error Apache cuyo nombre es: $dirParsedApacheError.$log_ApacheError";
	
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
		#print "\nConsulta: $consulta\n";
		my @lines =  grep /$consulta/i, <$logError>;
		#print "\nPerl PT Variable Grep: ".  @lines;
		if(@lines > 0){
		    $contador+=1;
		    $flagError=1;
		    #print "Contador: $contador\n";
		}
		last;
	    }		
        }
	close(ListaVariable);
  

    #Si el recurso no contiene variables obtenemos la ruta solicitada, en este caso se usa un diccionario para encontrar los caracteres ../ ..\ no hay nombres de directorios porque 
    #se puede dar el caso de que en el document root pongan directorios como /var/etc/home 
  
    #Ejemplo: /dir/dir1/../../../etc/passwd
#    }elsif($recurso =~ /(\/.*\/.+)/){
    }else{
        open (ListaURL, "$listaNegraURL") or die "ERROR: No se encuentra la lista negra : $listaNegraURL";
        while (<ListaURL>) {
            $linea=$_;
            chop ($linea);
	    #Escapando los caracteres * ? + / \ para que al momento de evaluarlo en la expresion regular los interprete como caracteres 	    
	    if($linea  =~ /\\/){
		$linea=~ s/\\/\\\\/g;
	    }elsif($linea  =~ /\//){
	    	$linea=~ s/\//\\\//g;
	    }
	    $linea=~ s/\./\\\./g;
	    $linea=~ s/\?/\\\?/g;
	    $linea=~ s/\+/\\\+/g;
            if($recurso =~ /.*$linea.*/ || $recursoDecodificado =~ /.*$linea.*/){
  	    #print "MATCH: $linea\n$recurso\n$recursoDecodificado\n";
	        if($codigoRespuesta == 200){
   	     #       print "PT por URL exitoso: $tiempo $recurso $recursoDecodificado\n";
  		    $diagnostico=1;
	        }else{
 	      #      print "PT por URL fallido: $tiempo $recurso $recursoDecodificado\n";	
		    $diagnostico=2;
 	        }
		last;
	    }
	}
	close(ListaURL);
    }
    if ($flagError == 1 ){
#	print "PT por Variables fallido:  $tiempo $recurso $recursoDecodificado\n";
	$diagnostico=1;
    }elsif ($flagLista == 1){
#	print "PT por Variables exitoso:  $tiempo $recurso $recursoDecodificado\n";
	$diagnostico=2;
    }
    return $diagnostico;
}

1;
