#!/bin/bash
# Despues de ejecutar el script installServer.sh, se ejecuta este script con el usuario que se designo para esta aplicacion el cual se indico en el script anterior
#Lo que hace este script es agregar las llaves publicas en el repositorio de llaves autorizadas en los servidores web y postgres, con ello ya no se solicitara la contraseña de acceso
#cuando se requiera conectar por SSH a un servidor.
#Tambien se solicitan algunos datos que seran guardados en el archivo de configuracion (ip y usuario)


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
read ip
#Validando que la ip no este vacio
until [ ! -z "$ip" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR APACHE ==="
    echo
    echo
    echo
    echo -n "[X] Error: Ingresa la direccion IP del servidor APACHE "
    read ip
done

#Guardando la ip en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable ipApache
sed -i -e"s/ipApache =/ipApache = \x22$ip\x22/" config.conf
echo
echo -n "[?]Ingresa cualquier USUARIO con permisos de lectura en el log de APACHE:  "
read usuario
#Validando que el usuario no este vacio
until [ ! -z "$usuario" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR APACHE ==="
    echo
    echo
    echo
    echo -n "[X]Error: Ingresa cualquier usuario con permisos de lectura en el log de APACHE:  "
    read usuario
done


#Guardando el usuario en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable usuarioApache
sed -i -e"s/usuarioWeb =/usuarioWeb = \x22$usuario\x22/" config.conf
echo
echo -n "[+] NOTA: Probablemente pida alguna autorización, favor de decir yes a todas las preguntas y escribir la contraseña del servidor POSTGRES cuando lo solicite, si la contraseña es incorrecta, favor de cancelar el script y volverlo a ejecutar. Verifica la IP y el usuario"
echo
echo
#Se crea el directorio .ssh porque por defecto no existe y en ese directorio se va a encontrar el repositorio de llaves autorizadas.
ssh $usuario@$ip mkdir -p .ssh
echo
#Ingresando la llave publica al repositorio de llaves autorizadas
cat ~/.ssh/id_rsa.pub | ssh $usuario@$ip 'cat >> ~/.ssh/authorized_keys'
echo
ssh $usuario@$ip "chmod 700 .ssh; chmod 640 ~/.ssh/authorized_keys"


############## CONFIGURANDO SERVIDOR BD #################



clear
echo "=== COPIAR LLAVE PUBLICA SERVIDOR POSTGRES ==="
echo
echo
echo
echo -n "[?]Ingresa la direccion IP del servidor POSTGRES:  "
read ip
#Validando que la ip no este vacio
until [ ! -z "$ip" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR POSTGRES ==="
    echo
    echo
    echo
    echo -n "[X] Error: Ingresa la direccion IP del servidor POSTGRES  "
    read ip
done

#Guardando la ip  en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable ipPostgres
sed -i -e"s/ipPostgres =/ipPostgres = \x22$ip\x22/" config.conf

echo
echo -n "[?]Ingresa cualquier USUARIO con permisos de lectura en el log de POSTGRES:  "
read usuario
#Validando que el usuario no este vacio
until [ ! -z "$usuario" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR POSTGRES ==="
    echo
    echo
    echo
    echo -n "[X]Error: Ingresa cualquier usuario con permisos de lectura en el log de POSTGRES:"
    read usuario
done


#Guardando el usuario en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable usuarioPostgres
sed -i -e"s/usuarioBD =/usuarioBD = \x22$usuario\x22/" config.conf
echo
echo -n "[+] NOTA: Probablemente pida alguna autorización, favor de decir yes a todas las preguntas y escribir la contraseña del servidor POSTGRES cuando lo solicite, si la contraseña es incorrecta, favor de cancelar el script y volverlo a ejecutar. Verifica la IP y el usuario"
echo
echo
#Se crea el directorio .ssh porque por defecto no existe y en ese directorio se va a encontrar el repositorio de llaves autorizadas.
ssh $usuario@$ip mkdir -p .ssh
echo
#Ingresando la llave publica al repositorio de llaves autorizadas
cat ~/.ssh/id_rsa.pub | ssh $usuario@$ip 'cat >> ~/.ssh/authorized_keys'
echo
ssh $usuario@$ip "chmod 700 .ssh; chmod 640 ~/.ssh/authorized_keys"




############## CONFIGURANDO SERVIDOR WAF #################



clear
echo "=== COPIAR LLAVE PUBLICA SERVIDOR WAF ==="
echo
echo
echo
echo -n "[?]Ingresa la direccion IP del servidor WAF:  "
read ip
#Validando que la ip no este vacio
until [ ! -z "$ip" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR WAF ==="
    echo
    echo
    echo
    echo -n "[X] Error: Ingresa la direccion IP del servidor WAF "
    read ip
done

#Guardando la ip  en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable ipWaf
sed -i -e"s/ipWaf =/ipWaf = \x22$ip\x22/"  config.conf

echo
echo -n "[?]Ingresa cualquier USUARIO con permisos de lectura en el log de WAF:  "
read usuario
#Validando que el usuario no este vacio
until [ ! -z "$usuario" ]; do
    clear
    echo "=== COPIAR LLAVE PUBLICA SERVIDOR WAF ==="
    echo
    echo
    echo
    echo -n "[X]Error: Ingresa cualquier usuario con permisos de lectura en el log de WAF:"
    read usuario
done


#Guardando el usuario en el archivo de configuracion, por defecto en el archivo no tiene un valor la variable usuarioPostgres
sed -i -e"s/usuarioWaf =/usuarioWaf = \x22$usuario\x22/"  config.conf
echo
echo -n "[+] NOTA: Probablemente pida alguna autorización, favor de decir yes a todas las preguntas y escribir la contraseña del servidor WAF cuando lo solicite, si la contraseña es incorrecta, favor de cancelar el script y volverlo a ejecutar. Verifica la IP y el usuario"
echo
echo
#Se crea el directorio .ssh porque por defecto no existe y en ese directorio se va a encontrar el repositorio de llaves autorizadas.
ssh $usuario@$ip mkdir -p .ssh
echo
#Ingresando la llave publica al repositorio de llaves autorizadas
cat ~/.ssh/id_rsa.pub | ssh $usuario@$ip 'cat >> ~/.ssh/authorized_keys'
echo
ssh $usuario@$ip "chmod 700 .ssh; chmod 640 ~/.ssh/authorized_keys"
