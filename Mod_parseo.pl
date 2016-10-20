#!/usr/bin/perl
use strict;
#use warnings;

#Funcion para leer archivo de configuracion


sub parse_config_file {
    my ($config_line, $Name, $Value, $Config);
    my ($File, $Config) = @_;
    open (CONFIG, "$File") or die "ERROR: Config file not found : $File";
    while (<CONFIG>) {
        $config_line=$_;
        chop ($config_line);          # Remove trailling \n
        $config_line =~ s/^\s*//;     # Remove spaces at the start of the line
        $config_line =~ s/\s*$//;     # Remove spaces at the end of the line
        if ( ($config_line !~ /^#/) && ($config_line ne "") ){    # Ignore lines starting with # and blank lines
            ($Name, $Value) = split (/=/, $config_line);          # Split each line into name value pairs
            $$Config{$Name} = $Value;                             # Create a hash of the name value pairs
        }
    }
    close(CONFIG);
}

# Variables para los logs de acceso de apache
my @ip_acces = ();
my @fecha_acces = ();
my @MetodoHTTP_acces = ();
my @Recurso_acces = ();
my @VersionHTTP_acces = ();
my @CodigoHTTP_acces = ();
my @Rec_size_acces = ();
my @HTTP_referer_acces = ();
my @UserAgent_acces = ();

# Variables para los logs de error de apache
my @fecha_error = ();
my @ip_error = ();
my @log_error = ();
my @msg_error = ();


#Variables para leer el archivo de configuracion
my $config_file= $ENV{HOME}."/Proyecto/herramienta.conf";
my %Config = ();
parse_config_file ($config_file, \%Config);
my $dirApache=$Config{'directorioAccess'};
my $dirApacheError=$Config{'directorioError'};
my $dirPostgres=$Config{'directorioPostgres'};
my $dirParsedApache=$Config{'parsedLogAccess'};
my $dirParsedApacheError=$Config{'parsedLogError'};
my $dirParsedPostgres=$Config{'parsedLogPostgres'};

#En el archivo de configuracion usa el comodin  ~ en referencia al directorio HOME, Perl no puede interpretar la tilde como el directorio, para ello la sustituimos ~ por la variable de
#entorno de Perl  que contiene el directorio HOME del usuario

$dirApache =~ s/^~(\w*)/$ENV{HOME}/e;
$dirApacheError =~ s/^~(\w*)/$ENV{HOME}/e;
$dirPostgres =~ s/^~(\w*)/$ENV{HOME}/e;
$dirParsedApache =~ s/^~(\w*)/$ENV{HOME}/e;
$dirParsedApacheError =~ s/^~(\w*)/$ENV{HOME}/e;
$dirParsedPostgres =~ s/^~(\w*)/$ENV{HOME}/e;



# Checando si se mando como argumento el log de Access de Apache
# Obtenemos los archivos generados por el modulo de obtencion de archivos
if ($ARGV[0] ne "-")
{
    my $log_Apache = $ARGV[0] or die "Leer log de apache\n";
    my $rutaAccess=$dirApache.$log_Apache;

	# Abrimos el archivo de los logs
    open(my $data_acces, '<', $rutaAccess) or die "No se puede abrir el archivo $rutaAccess\n";
    my $filename1 = $dirParsedApache.$log_Apache;
    open(my $new_acces, '>', $filename1) or die "Could not open file '$filename1' $!";
    while (my $line1 = <$data_acces>)
    {
        chomp $line1;

		# Parseamos el log de acceso apache
		my @log_apache_array = (split " " , $line1, 12);
		my @log_apache_array_aux = (split /\"/ , $line1);
		my $aux='';
		
		$aux = $log_apache_array[0];
		push @ip_acces, $aux;
		$aux = $log_apache_array[3];
		$aux =~ tr/\[//d;
		push @fecha_acces, $aux;
		$aux  = $log_apache_array[5];
		$aux =~ tr/\"//d;
		push @MetodoHTTP_acces, $aux;
		$aux  = $log_apache_array[6];
		push @Recurso_acces,$aux;
		$aux  = $log_apache_array[7];
		$aux =~ tr/\"//d;
		push @VersionHTTP_acces,$aux;
		$aux  = $log_apache_array[8];
		push @CodigoHTTP_acces,$aux;
		$aux = $log_apache_array[9];
		push @Rec_size_acces,$aux;
		$aux = $log_apache_array[10];
		$aux =~ tr/\"//d;
		push @HTTP_referer_acces,$aux;
		$aux = $log_apache_array_aux[5];
		push @UserAgent_acces,$aux;
		print $new_acces "$ip_acces[-1]<-->$fecha_acces[-1]<-->$MetodoHTTP_acces[-1]<-->$Recurso_acces[-1]<-->$VersionHTTP_acces[-1]<-->$CodigoHTTP_acces[-1]<-->$Rec_size_acces[-1]<-->$HTTP_referer_acces[-1]<-->$UserAgent_acces[-1]\n";
    }
    close $new_acces;
    close $data_acces;
}


# Checando si se mando como argumento el log de error de Apache
if ($ARGV[1] ne "-")
{
    my $log_Apache_error = $ARGV[1] or die "Leer log de error de apache\n";
    my $rutaError=$dirApacheError.$log_Apache_error;
	# Abrimos el archivo de los logs
    open(my $data_error, '<', $rutaError) or die "No se puede abrir el archivo $rutaError\n";
    my $filename2 = $dirParsedApacheError.$log_Apache_error;
    open(my $new_error, '>', $filename2) or die "Could not open file '$filename2' $!";
	#Parseando log de Error

    while (my $line2 = <$data_error>)
    {
		chomp $line2;
		my @log_apache_error_array = (split /\]/ , $line2);
		my @log_apache_error_array_aux = (split /\:/ , $line2);
		my $aux='';

		my $aux = $log_apache_error_array[0];
		$aux =~ tr/\[//d;
		push @fecha_error,$aux;
		$aux = $log_apache_error_array[1];
		$aux =~ tr/\ [//d;
		push @log_error,$aux;
		$aux = $log_apache_error_array[2];
		$aux =~ tr/  \[client//d;
		push @ip_error,$aux;
		$aux = $log_apache_error_array[3];
		#$aux =~ tr/^._//d;
		push @msg_error,$aux;
		print $new_error "$fecha_error[-1]<-->$log_error[-1]<-->$ip_error[-1]<-->$msg_error[-1]\n";
    } 
close $new_error;
}


# Variables para los logs de postgres
my @fecha_postgres = ();
my @hora_postgres = ();
my @error_postgres = ();

## Checando si se mando como argumento el log de Postgres
if ($ARGV[2] ne "-")
{
	my $log_postgres = $ARGV[2] or die "Leer log de apache\n";
    my $rutaPostgres=$dirPostgres.$log_postgres;

	# Abrimos el archivo de los logs
    open(my $data_postgres, '<', $rutaPostgres) or die "No se puede abrir el archivo $rutaPostgres\n";
    my $filename3 = $dirParsedPostgres.$log_postgres;
    open(my $new_postgres, '>', $filename3) or die "Could not open file '$filename3' $!";
	
    while (my $line = <$data_postgres>)
	{
		chomp $line;
		my @log_postgres = (split / / , $line, 5);
		my @log_postgres_aux = (split /:/ , $line);
		my $aux='';

		if ($line =~ /ERROR:/)
		{
			my $aux = $log_postgres[0];
			push @fecha_postgres,$aux;
			my $aux = $log_postgres[1];
			push @hora_postgres,$aux;
			my $aux = $log_postgres[4];
			push @error_postgres,$aux;
			print $new_postgres "|$fecha_postgres[-1] $hora_postgres[-1]\[$error_postgres[-1]\n";
		}
	}
}

