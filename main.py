#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# @author     Raúl Caro Pastorino
# @email      dev@fryntiz.es
# @web        https://fryntiz.es
# @gitlab     https://gitlab.com/fryntiz
# @github     https://github.com/fryntiz
# @twitter    https://twitter.com/fryntiz
# @telegram   https://t.me/fryntiz

# Create Date: 2022
# Project Name:
# Description:
#
# Dependencies:
#
# Revision 0.01 - File Created
# Additional Comments:

# @copyright  Copyright © 2022 Raúl Caro Pastorino
# @license    https://wwww.gnu.org/licenses/gpl.txt

# Copyright (C) 2022  Raúl Caro Pastorino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Guía de estilos aplicada: PEP8

#######################################
# #           Descripción           # #
#######################################
## Obtiene la información del controlador solar, la almacena en base de datos
## e intenta posteriormente subir la información a la nube.
##
## Almacenarla en base de datos implica poder trabajar sin depender de internet
## por si es el caso (como en mi situación) que por la noche quedan los
## routers y modem desconectados. De esta forma aunque no sea en tiempo real
## puedo observar esos datos y almacenarlos en la nube.
##

#######################################
# #       Importar Librerías        # #
#######################################
from Models.SolarControllers.RenogyRoverLi import RenogyRoverLi
# from Models.ApiConnection import ApiConnection
# from Models.DbConnection import DbConnection
from dotenv import load_dotenv
import os
import datetime
import time

# Cargo archivos de configuración desde .env sobreescribiendo variables locales.
load_dotenv(override=True)

#######################################
# #             Variables           # #
#######################################

sleep = time.sleep

# Debug
DEBUG = os.getenv("DEBUG") == "True"

# Puerto de la interfaz serial
PORT = os.getenv("PORT")

# Abro conexión con la base de datos instanciando el modelo que la representa.
# dbconnection = Dbconnection()

# Parámetros para acceder a la API.
# apiconnection = Apiconnection()

# Controlador solar
solar_controller = RenogyRoverLi(debug=DEBUG, port=PORT)


#######################################
# #            FUNCIONES            # #
#######################################


def loop ():
    # Contador de lecturas desde la última subida a la API
    n_lecturas = 0

    while True:
        n_lecturas = n_lecturas + 1

        if DEBUG:
            print('Lecturas de sensores desde la última subida: ' + str(
                n_lecturas))

        # Guardo el momento que inicia lectura.
        marca_inicio = datetime.datetime.now(tz=None)

        # Leyendo controlador solar
        datas = solar_controller.get_all_datas()

        if DEBUG:
            print('Datos obtenidos: ' + str(datas))

        # Almacena en la base de datos.
        # save_to_db(dbconnection)

        if n_lecturas == 1:
            n_lecturas = 0

            try:
                pass
                # upload_data_to_api(apiconnection, dbconnection)
            except():
                if DEBUG:
                    print('Error al subir datos a la api')

        # Muestro tiempo en realizarse la lectura de datos.
        if DEBUG:
            print('Inicio: ', str(marca_inicio))
        marca_fin = datetime.datetime.now(tz=None)

        if DEBUG:
            print('Fin: ', str(marca_fin))

        tiempo_ejecucion = marca_fin - marca_inicio

        if DEBUG:
            print('Tiempo de ejecución: ', str(tiempo_ejecucion))

        # Pausa entre cada lectura
        sleep(30)

    # Acciones tras terminar con error
    # dbconnection.close_connection()


def main ():
    print('Iniciando Aplicación')

    # Pauso 6 segundos para dar margen a la interfaz si estuviera preparándose.
    sleep(6)

    try:
        loop()
    except Exception as e:
        print('Ha ocurrido un error en la aplicación:', e.__class__.__name__)
        sleep(300)
        main()
    exit(0)


if __name__ == "__main__":
    main()

# sudo apt install python3-dotenv python3-serial python3-pyserial
