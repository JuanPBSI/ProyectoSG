package SQLi;
use strict;
# Esta parte del codigo se encarga de determinar si existieron ataques SQL que ameriten el envio de un mensaje por correo electronico
#---------------------------------------------------------------------------------------------------------------------
sub analizarSQLi
{
	my $linea = $_[0];
	my $time_stamp = $_[1];
	my $Recurso = $_[2];
	my $Respuesta = $_[3];
	my $Referer = $_[4];
	my $userAgent = $_[5];
	my $RegEX = $_[6];
	my $new_error_apache = $_[7];
	my $error_postgres = $_[8];

	my $cont_encuentros_mail = 0;
	my $cont_encuentros = 0;
	my $cont_encuentros_ref = 0;
	my $cont_encuentros_user = 0;
	my $cont_error = 0;
	my $cont_200 = 0;
	my $cont_error_en_base = 0;
	my $i = 0;
	# Decodificamos la URI
	# decodifica($Recurso);
	# Primero buscamos las ocurrencias SQL en la URI del log de apache
	if(decode($Recurso) =~ /$RegEX/i)
	{
		print $new_error_apache decode($linea)."\n";
		$cont_encuentros++;
		if(($Respuesta =~ /4..\b/i) || ($Respuesta =~ /5..\b/i))
		{
			$cont_error++;
		}
		elsif($Respuesta =~ /2..\b/i)
		{
			$cont_200++;
			open(my $data_error_postgres, '<', $error_postgres) or die "No se puede abrir el archivo: $error_postgres\n";
			$cont_error_en_base += get_error_postgres($time_stamp,$Recurso,$data_error_postgres,$i);
			close($data_error_postgres);
			if ($cont_encuentros > 0 && $cont_200 > 0 && $cont_error_en_base == 0)
			{
				$cont_encuentros_mail++;
			}
		}
	}
	if(decode($Referer) =~ /$RegEX/i)
	{
		print $new_error_apache decode($linea)."\n";
		$cont_encuentros_ref++;
	}
	if(decode($userAgent) =~ /$RegEX/i)
	{
		print $new_error_apache decode($linea)."\n";
		$cont_encuentros_user++;
	}
	my @result = ($cont_encuentros, $cont_encuentros_ref, $cont_encuentros_user, $cont_error, $cont_200, $cont_error_en_base, $cont_encuentros_mail);
	return @result;
}
#---------------------------------------------------------------------------------------------------------------------
sub errorPostgres
{
	my $error_postgres = $_[0];
	my $cont_errores_postgres = `wc -l $error_postgres | cut -d" " -f 1`;
	chomp $cont_errores_postgres;
	return $cont_errores_postgres;
}
#---------------------------------------------------------------------------------------------------------------------
sub get_error_postgres
{
	my $time_stamp=$_[0];
	my $URI=$_[1];
	my $data_error_postgres=$_[2];
	my $cont=$_[3];
	my $puntos = 0;
	
	# Colocamos el time stamp de apache con en el mismo formato que el de postgres
	# |10/Oct/2016:11:17:41 ---> |2016-10-10 11:35:44
	$time_stamp =~ s/\//-/;
	$time_stamp =~ s/\//-/;
	$time_stamp =~ s/jan/01/i;
	$time_stamp =~ s/feb/02/i;
	$time_stamp =~ s/mar/03/i;
	$time_stamp =~ s/abr/04/i;
	$time_stamp =~ s/may/05/i;
	$time_stamp =~ s/jun/06/i;
	$time_stamp =~ s/jul/07/i;
	$time_stamp =~ s/ago/08/i;
	$time_stamp =~ s/sep/09/i;
	$time_stamp =~ s/oct/10/i;
	$time_stamp =~ s/nov/11/i;
	$time_stamp =~ s/dec/12/i;
	$time_stamp =~ s/:/ /;

	my $newURI = decode($URI);

	#print "$time_stamp;$newURI\n";
	#print "---------------------------------------------------------------------------------------------------------\n";

	while (my $linea = <$data_error_postgres>)
	{
		chomp $linea;
		my @log_postgres_columns = (split /\[/ , $linea);
		my $aux_postgres_column = $log_postgres_columns[0];
		
		# Obtenenmos la sentencia que genero el error
		my $stament_postgres = $log_postgres_columns[1];
		#$aux_postgres_column =~ s/.$/ /;
		#$time_stamp =~ s/.$/ /;
		$stament_postgres =~ s/"/|/;
		$stament_postgres =~ s/"[^"]+$//g;
		# Generamos una expresion regular para la sentencia que despues se buscara en la linea del log de apache
		# Escapamos todos los caracteres de la expresion regular nueva

		my @stament_postgres2 = (split /\|/ , $stament_postgres);
		my $regexp_stament = $stament_postgres2[1];
		$regexp_stament =~ s/\\/\\\\/g;
		$regexp_stament =~ s/\(/\\(/g;
		$regexp_stament =~ s/\)/\\)/g;
		$regexp_stament =~ s/\^/\\^/g;
		$regexp_stament =~ s/\+/\\+/g;
		$regexp_stament =~ s/\|/\\|/g;
		$regexp_stament =~ s/\[/\\[/g;
		$regexp_stament =~ s/\]/\\]/g;
		
		#print "$stament_postgres2[1]	:	$regexp_stament\n";
		if($aux_postgres_column =~ /$time_stamp/i)
		{
			if($newURI =~ /$regexp_stament/i)
			{
				#print "\[$cont\]	$aux_postgres_column|$time_stamp	:	$newURI	:	$regexp_stament\n";
				$puntos = 1;
				last;
			}
			else
			{
				$puntos = 0;
				#print "$newURI	:	$regexp_stament\n";
				#last;
			}
		}
	}
	return $puntos;
}
#---------------------------------------------------------------------------------------------------------------------
sub decode
{
	my $coded_string=$_[0];

	$coded_string=~ s/%20/ /ig;
	$coded_string=~ s/%22/"/ig;
	$coded_string=~ s/%25/%/ig;
	$coded_string=~ s/%27/'/ig;
	$coded_string=~ s/%28/(/ig;
	$coded_string=~ s/%29/)/ig;
	$coded_string=~ s/%2A/*/ig;
	$coded_string=~ s/%2B/+/ig;
	$coded_string=~ s/%2C/,/ig;
	$coded_string=~ s/%2f/\//ig;
	$coded_string=~ s/%3b/;/ig;
	$coded_string=~ s/%3d/=/ig;
	$coded_string=~ s/%7C/|/ig;

	return $coded_string;
}

1;
#print "$cont_encuentros ; $cont_error ; $cont_200 ; $cont_errores_postgres ; $cont_error_en_base\n";