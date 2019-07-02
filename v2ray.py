#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import commands

def open_port(port):
    cmd =[ "iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport $1 -j ACCEPT",
            "iptables -I INPUT -m state --state NEW -m udp -p udp --dport $1 -j ACCEPT",
            "ip6tables -I INPUT -m state --state NEW -m tcp -p tcp --dport $1 -j ACCEPT",
            "ip6tables -I INPUT -m state --state NEW -m udp -p udp --dport $1 -j ACCEPT"]

    for x in cmd:
        x = x.replace("$1",str(port))
        commands.getoutput(x)

def start():
    os.system("""supervisorctl start v2ray.fun""")

def stop():
    os.system("""supervisorctl stop v2ray.fun""")

def write(data):
    data_file = open("/usr/local/V2ray.Fun/panel.config", "w")
    data_file.write(json.dumps(data,indent=2))
    data_file.close()

if __name__ == '__main__':
    data_file = open("/usr/local/V2ray.Fun/panel.config","r")
    data = json.loads(data_file.read())
    data_file.close()
    print("Bienvenido a V2ray panel - OFC BY DANKELTHAHER\n")
    print("nombre de usuario actual del panel：" + str(data['username']))
    print("Contrasena actual del panel：" + str(data['password']))
    print("Puerto del panel actual：" + str(data['port']))
    print("Por favor ingrese la funcion de seleccion de numeros：\n")
    print("1. Inicio del Panel")
    print("2. Detener el Panel")
    print("3. Reiniciar el panel")
    print("4. Restablecer el nombre de usuario y la contrasena del panel")
    print("5. Establecer estado del Panel SSL")
    print("6. Configuracion del puerto del panel")
    choice = str(input("\nSeleccione una opcion："))

    if choice == "1":
        start()
        open_port(data['port'])
        print("Inicio exitoso!")

    elif choice == "2":
        stop()
        print("detencion exitosa！")

    elif choice == "3":
        stop()
        start()
        open_port(data['port'])
        print("El reinicio es exitoso!")
    elif choice == "4":
        new_username = str(raw_input("Por favor ingrese un nuevo nombre de usuario："))
        new_password = str(raw_input("Por favor ingrese una nueva contrasena："))
        data['username'] = new_username
        data['password'] = new_password
        write(data)
        stop()
        start()
        print("La contrasena del nombre de usuario se establecio correctamente!！")
    elif choice == "5":
        print("Sugerencia: la funcionalidad SSL del panel solo funcionara si la función V2ray TLS esta habilitada en el panel\n")
        print("1. Abrir la función SSL del panel")
        print("2. Desactivar la funcionalidad SSL del panel")
        ssl_choice = str(input("seleccione una opcion："))

        if ssl_choice == "1":
            data['use_ssl'] = "on"
            write(data)
            stop()
            start()
            print("Panel SSL está activado!")
        else:
            data['use_ssl'] = "off"
            write(data)
            stop()
            start()
            print("Panel SSL esta desactivado!")
    elif choice == "6":
        new_port = input("Por favor ingrese un nuevo puerto de panel：")
        data['port'] = int(new_port)
        write(data)
        stop()
        start()
        open_port(data['port'])
        print("El puerto del panel ha sido modificado!")
        
