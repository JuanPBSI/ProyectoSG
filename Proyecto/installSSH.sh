#!/bin/bash
# Despues de ejecutar el script installServer.sh, se ejecuta este script con el usuario que se designo para esta aplicacion el cual se indico en el script anterior
#Lo que hace este script es agregar las llaves publicas en el repositorio de llaves autorizadas en los servidores web y postgres, con ello ya no se solicitara la contraseña de acceso
#cuando se requiera conectar por SSH a un servidor.
#Tambien se solicitan algunos datos que seran guardados en el archivo de configuracion (ip y usuario)

cp config.conf.bk config.conf
clear
echo "=== CONFIGURANDO LLAVES SSH  === "
echo
echo
echo
echo "[+] NOTA: Ejecutar script con el usuario designado para la conexión ssh, de lo contrario presiona CTRL + C para cancelar"
echo "[+] NOTA: Deja todos los valores por defecto y no introduzcas ninguna passphrase"
echo
echo

#Generando un par de llaves (publica/privada) para la conexion SSH, la llave publica es la que se comparte en el repositorio de llaves autorizadas en los servidores web y postgres
ssh-keygen -t rsa


####### CONFIGURANDO SERVIDOR APACHE #########

clear
echo "=== COPIAR LLAVE PUBLICA SERVIDOR APACHE ==="
echo
echo
echo
echo -n "[?]Ingresa la direccion IP del servidor APACHE: "
read ipApache
#Validando que la ip no este vacio
until [ ! -z "$ipApache" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR APACHE ==="
    echo
    echo
    echo
    echo -n "[X] Error: Ingresa la direccion IP del servidor APACHE "
    read ipApache
done

#Guardando la ip en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable ipApache
sed -i -e"s/ipApache =/ipApache = \x22$ipApache\x22/" ~/Proyecto/config.conf
echo
echo -n "[?]Ingresa cualquier USUARIO con permisos de lectura en el log de APACHE:  "
read usuarioApache
#Validando que el usuario no este vacio
until [ ! -z "$usuarioApache" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR APACHE ==="
    echo
    echo
    echo
    echo -n "[X]Error: Ingresa cualquier usuario con permisos de lectura en el log de APACHE:  "
    read usuarioApache
done


#Guardando el usuario en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable usuarioApache
sed -i -e"s/usuarioWeb =/usuarioWeb = \x22$usuarioApache\x22/" ~/Proyecto/config.conf
echo
echo -n "[+] NOTA: Probablemente pida alguna autorización, favor de decir yes a todas las preguntas y escribir la contraseña del servidor POSTGRES cuando lo solicite, si la contraseña es incorrecta, favor de cancelar el script y volverlo a ejecutar. Verifica la IP y el usuario"
echo
echo
#Se crea el directorio .ssh porque por defecto no existe y en ese directorio se va a encontrar el repositorio de llaves autorizadas.
ssh $usuarioApache@$ipApache mkdir -p .ssh
echo
#Ingresando la llave publica al repositorio de llaves autorizadas
cat ~/.ssh/id_rsa.pub | ssh $usuarioApache@$ipApache 'cat >> ~/.ssh/authorized_keys'
echo
ssh $usuarioApache@$ipApache "chmod 700 .ssh; chmod 640 ~/.ssh/authorized_keys"


############## CONFIGURANDO SERVIDOR BD #################



clear
echo "=== COPIAR LLAVE PUBLICA SERVIDOR POSTGRES ==="
echo
echo
echo
echo -n "[?]Ingresa la direccion IP del servidor POSTGRES:  "
read ipBD
#Validando que la ip no este vacio
until [ ! -z "$ipBD" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR POSTGRES ==="
    echo
    echo
    echo
    echo -n "[X] Error: Ingresa la direccion IP del servidor POSTGRES  "
    read ipBD
done

#Guardando la ip  en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable ipPostgres
sed -i -e"s/ipPostgres =/ipPostgres = \x22$ipBD\x22/" ~/Proyecto/config.conf

echo
echo -n "[?]Ingresa cualquier USUARIO con permisos de lectura en el log de POSTGRES:  "
read usuarioBD
#Validando que el usuario no este vacio
until [ ! -z "$usuarioBD" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR POSTGRES ==="
    echo
    echo
    echo
    echo -n "[X]Error: Ingresa cualquier usuario con permisos de lectura en el log de POSTGRES:"
    read usuarioBD
done


#Guardando el usuario en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable usuarioPostgres
sed -i -e"s/usuarioBD =/usuarioBD = \x22$usuarioBD\x22/" ~/Proyecto/config.conf
echo
echo -n "[+] NOTA: Probablemente pida alguna autorización, favor de decir yes a todas las preguntas y escribir la contraseña del servidor POSTGRES cuando lo solicite, si la contraseña es incorrecta, favor de cancelar el script y volverlo a ejecutar. Verifica la IP y el usuario"
echo
echo
#Se crea el directorio .ssh porque por defecto no existe y en ese directorio se va a encontrar el repositorio de llaves autorizadas.
ssh $usuarioBD@$ipBD mkdir -p .ssh
echo
#Ingresando la llave publica al repositorio de llaves autorizadas
cat ~/.ssh/id_rsa.pub | ssh $usuarioBD@$ipBD 'cat >> ~/.ssh/authorized_keys'
echo
ssh $usuarioBD@$ipBD "chmod 700 .ssh; chmod 640 ~/.ssh/authorized_keys"




############## CONFIGURANDO SERVIDOR WAF #################



clear
echo "=== COPIAR LLAVE PUBLICA SERVIDOR WAF ==="
echo
echo
echo
echo -n "[?]Ingresa la direccion IP del servidor WAF:  "
read ipWAF
#Validando que la ip no este vacio
until [ ! -z "$ipWAF" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR WAF ==="
    echo
    echo
    echo
    echo -n "[X] Error: Ingresa la direccion IP del servidor WAF "
    read ipWAF
done

#Guardando la ip  en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable ipWaf
sed -i -e"s/ipWaf =/ipWaf = \x22$ipWAF\x22/"  ~/Proyecto/config.conf

echo
echo -n "[?]Ingresa cualquier USUARIO con permisos de lectura en el log de WAF y también para poder cambiar la fecha y hora:  "
read usuarioWAF
#Validando que el usuario no este vacio
until [ ! -z "$usuarioWAF" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR WAF ==="
    echo
    echo
    echo
    echo -n "[X]Error: Ingresa cualquier usuario con permisos de lectura en el log de WAF y también para poder cambiar la fecha y hora:"
    read usuarioWAF
done


#Guardando el usuario en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable usuarioPostgres
sed -i -e"s/usuarioWaf =/usuarioWaf = \x22$usuarioWAF\x22/"  ~/Proyecto/config.conf
echo
echo -n "[+] NOTA: Probablemente pida alguna autorización, favor de decir yes a todas las preguntas y escribir la contraseña del servidor WAF cuando lo solicite, si la contraseña es incorrecta, favor de cancelar el script y volverlo a ejecutar. Verifica la IP y el usuario"
echo
echo
#Se crea el directorio .ssh porque por defecto no existe y en ese directorio se va a encontrar el repositorio de llaves autorizadas.
ssh $usuarioWAF@$ipWAF mkdir -p .ssh
echo
#Ingresando la llave publica al repositorio de llaves autorizadas
cat ~/.ssh/id_rsa.pub | ssh $usuarioWAF@$ipWAF 'cat >> ~/.ssh/authorized_keys'
echo
ssh $usuarioWAF@$ipWAF "chmod 700 .ssh; chmod 640 ~/.ssh/authorized_keys"











############## SINCRONIZANDO FECHA Y HORA  #################



clear
echo "=== SINCRONIZANDO FECHA Y HORA ==="
echo
echo
echo
echo  "[?]¿Desea sincronizar la fecha y hora en todos los servidores (Web,Base de datos y Waf)? S/N "
echo -n "Seleccione una opcion: "
read opcion
until !([ "$opcion" != "S" ] &&  [ "$opcion" != "N" ] &&  [ "$opcion" != "s" ] &&  [ "$opcion" != "n" ]); do
    clear
    echo "=== SINCRONIZANDO FECHA Y HORA ==="
    echo
    echo
    echo
    echo "[X] Error: ¿Desea sincronizar la fecha y hora en todos los servidores (Web,Base de datos y Waf)? S/N "
    echo -n "Seleccione una opcion: "
    read opcion
done
    if [ "$opcion" = "S" ] || [ "$opcion" = "s" ]; then
	clear
	echo "=== SINCRONIZANDO FECHA Y HORA ==="
	echo
	echo
	echo
	echo  "-Presione 1 para ingresar la hora manualmente."
	echo  "-Presione 2 para que los servidores Apache y Postgres tengan la misma hora y fecha del servidor WAF."
	echo -n "Seleccione una opcion: "
	read opcionTiempo
	until !([ "$opcionTiempo" != "1" ] &&  [ "$opcionTiempo" != "2" ] ); do
	    clear
	    echo "=== SINCRONIZANDO FECHA Y HORA ==="
	    echo
	    echo
	    echo
	    echo -n "[X] Error:"
	    echo  "-Presione 1 para ingresar la hora manualmente."
	    echo  "-Presione 2 para que los servidores Apache y Postgres tengan la misma hora y fecha del servidor WAF."
	    echo -n "Seleccione una opcion: "
	    read opcionTiempo
	done
	if [ "$opcionTiempo" -eq "1" ]; then
	    clear
	    echo "=== SINCRONIZANDO FECHA Y HORA ==="
	    echo
	    echo
	    echo
	    echo  "[?] Ingrese la fecha bajo el siguiente formato: AnioMesDia Hora:Minuto:Segundo 20161102 06:10:00 \n"
   	    echo  "[+] NOTA: Después de ingresar la hora deberá escribir la contraseña de usuario $usuarioWAF del  servidor WAF, si la contraseña es incorrecta, favor de cancelar el script y volverlo a ejecutar."
 	    echo -n "Ingrese una hora: "
	    read hora
	    until [ ! -z "$hora" ]; do
		clear
	        echo "=== SINCRONIZANDO FECHA Y HORA ==="
            	echo
	        echo
        	echo
	        echo  "[X] Error: Ingrese la fecha bajo el siguiente formato: AnioMesDia Hora:Minuto:Segundo 20161102 06:10:00 \n"
		echo  "[+] NOTA: Después de ingresar la hora deberá escribir la contraseña de usuario $usuarioWAF del  servidor WAF, si la contraseña es incorrecta, favor de cancelar el script y volverlo a ejecutar."
		echo -n "Ingrese una hora: "
        	read hora
	    done
	    hora1=\"$hora\"
	    su -c "date --set=$hora1" -
	    ssh $usuarioApache@$ipApache "date --set=$hora1"
	    ssh $usuarioBD@$ipBD "date --set=$hora1"


	else
	    clear
	    echo "=== SINCRONIZANDO FECHA Y HORA ==="
	    echo
	    echo
	    echo
   	    echo  "[+] NOTA: Favor de escribir la contraseña de usuario $usuarioWAF del  servidor WAF, si la contraseña es incorrecta, favor de cancelar el script y volverlo a ejecutar."
	    hora=$(date "+%Y%m%d %H:%M:%S")
	    hora1=\"$hora\"
	    su -c "date --set=$hora1" -
	    ssh $usuarioApache@$ipApache "date --set=$hora1"
	    ssh $usuarioBD@$ipBD "date --set=$hora1"

	fi

    else
    	exit 1;
    fi

