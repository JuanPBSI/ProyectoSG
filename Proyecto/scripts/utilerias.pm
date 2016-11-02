package utilerias;

use strict;
use Encode;
use URI::Encode;
use MIME::Base64;
use Date::Parse;

sub urlDecoder{
    my $url =  $_[0];
#### Decodificando URL %Hexadecimal
    #Se hace un while para atacer la doble codificación
    while($url =~ /%[0-9|a-f][0-9|a-f]/i){
	my $uri = URI::Encode->new( { encode_reserved => 0 } );
	$url = $uri->decode($url);
    }
	$url =~ s/\+/ /ig;
#### Decodificando BASE64
     #usamos /i para case INSENSITIVE
    if($url =~ /data:.*;base64,(.*)/i){
        my $b64 = decode_base64($1);
        $url =~ s/$1/$b64/e;
    }
    return $url;
}


sub read_config_file {
    my ($config_line, $Name, $Value, $Config);
    my ($File, $Config) = @_;
    open (CONFIG, "$File") or die "ERROR: No se encuentra el archivo de configuracion: $File";
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

sub suma_segundo_hora{

#Se ingresa cualquier formato de la marca de tiempo y devuelve el siguiente formato:
#Wed Oct 12 01:45:27 2016

my $tiempo=$_[0];
my $tolerancia=$_[1];

#Pasando a fecha a EPOC
my $unix_time = str2time($tiempo);
$unix_time = $unix_time + $tolerancia;
my $fecha = localtime($unix_time);
return $fecha;
}

1;
