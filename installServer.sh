#!/bin/bash

#Este script lo unico que hace es asignar un usuario para que la aplicación sea ejecutada por el, dicho usuario puede ser uno que ya exista o se crea uno nuevo,
#posteriormente se crean varios directorios de trabajo y se copian los archivos necesarios  para la ejecutar la aplicación, dichos archivos se copian en el directorio home del usuario designado
#con los permisos adecuados.
clear
echo "=== INSTALAR SERVER ==="
echo
echo
echo
echo "[+] NOTA: Ejecutar script como root, de lo contrario habran errores"
echo
echo "Favor de ingresar un nombre de USUARIO del sistema, si no existe se creará uno nuevo"
read usuario

#Validando que el usuario no este vacio
until [ ! -z "$usuario" ]; do
    clear
    echo "=== INSTALAR  SERVER ==="
    echo
    echo
    echo
    echo "[X] Error: Ingresa un nombre de USUARIO"
    read usuario
done

echo "Creando usuario ....."
adduser $usuario
echo "Copiando archivos necesarios ....."
cp -R Proyecto/ /home/$usuario/
chown -R $usuario:$usuario /home/$usuario/Proyecto
chmod -R 755 /home/$usuario/Proyecto

echo "=== Se instalaran los paquetes correspondientes: es necesariio tener conexión a internet ==="
apt-get update
{ # try
	apt-get install openssh-server python-pip  build-essential libssl-dev libffi-dev python-dev python-pandas python-reportlab python-numpy python-matplotlib -y
} || { # catch
	echo "[+] Hubo un error en la instalación vuelva a ejecutar el script para intentar de nuevo....."
	exit
}
clear
echo "=== INSTALAR SERVER ==="echo
echo
echo
echo "[+] NOTA: Posiblemente pida alguna autorizacion, escribir yes en todas las solicitudes:"
export PERL_MM_USE_DEFAULT=1
{ # try
	pip install pysftp

} || { # catch
	echo "Error al intentar instalar pysftp reitentando....."
	pip install pysftp
}
{ # try
	pip install pysftp
} || { # catch
	echo "[ERROR] No se pudo instalar pysftp vuelva a ejecutar el script para intentar de nuevo....."
	exit
}
{ # try
	pip install spur
} || { # catch
	echo "Error al intentar instalar Spur reitentando....."
	pip install spur
}
{ # try
	pip install spur
} || { # catch
	echo "[ERROR] No se pudo instalar spur vuelva a ejecutar el script para intentar de nuevo....."
	exit
}
pip install termcolor
cpan MIME::Base64
cpan URI::Encode
cpan Date::Parse
{ # try
	chmod 755 /etc/modsecurity/modsecurity.conf
} || { # catch
	echo "[ERROR] No se encontró en archivo de configuración de ModSecurity....."
	exit
}
# Necesario para crear las imagenes fuera de un ambiente grafico
sed -i -e 's/backend      : TkAgg/backend      : Agg/g' /etc/matplotlibrc
clear
echo "=== INSTALAR SERVER ==="
echo
echo
echo
echo "[+] NOTA: Ejecuta los siguientes comandos para instalar las llaves:"
echo "su $usuario"
echo "sh /home/$usuario/Proyecto/installSSH.sh"
