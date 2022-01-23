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
##
##

#######################################
# #       Importar Librerías        # #
#######################################
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


# result = client.read_holding_registers(0x0107,1,unit=1)

#######################################
# #            FUNCIONES            # #
#######################################

class SerialConnection:
    client = None
    DEBUG = False

    def __init__ (self, debug=True, port='/dev/ttyUSB0', baudrate=9600,
                  timeout=0.5, method='rtu'):

        self.client = ModbusClient(method=method, port=port,
                                   baudrate=baudrate, timeout=timeout)

        self.DEBUG = debug

    def connect (self):
        """
        Abre la conexión con el dispositivo.
        :return:
        """
        return self.client.connect()

    def close (self):
        """
        Cierra la conexión con el dispositivo.
        :return:
        """
        return self.client.close()

    def read_register (self, register, bits=2, type=None):
        """
        Lee un registro y devuelve su resultado.
        :param register:
        :return:
        """
        self.connect()
        response = self.client.read_holding_registers(register, bits, unit=1)
        self.close()

        if response.isError() and self.DEBUG:
            print("Error: " + str(response.function_code))
        elif self.DEBUG and response.registers:
            msg = "Registro: {}, Valor: {}".format(register, response.registers[0])
            print(msg)

        value = response.registers[0] if response.registers else None

        if value and type == 'string':
            return str(value)
        elif value and type == 'int':
            return int(value)
        elif value and type == 'float':
            return float(value)

        return value

    def read_registers (self, registers, bits=2):
        """
        Lee una lista de registros y devuelve sus resultados en el mismo orden.
        :param registers:
        :return:
        """
        results = {}

        for register in registers:
            #TODO → Utilizar atributos del diccionario (type, bits, address)
            results.append(self.read_register(register, bits))

        return results
