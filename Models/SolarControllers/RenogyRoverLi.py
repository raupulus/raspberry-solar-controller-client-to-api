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
## Modelo que representa a un controlador de placas solares Renogy Rover Li
##

#######################################
# #       Importar Librerías        # #
#######################################

from Models.SolarControllers.AbstractModel import AbstractModel
from Models.SerialConnection import SerialConnection
import time

#######################################
# #             Variables           # #
#######################################

sleep = time.sleep


#######################################
# #            FUNCIONES            # #
#######################################


class RenogyRoverLi(AbstractModel):
    serial = None
    DEBUG = False

    tablename = 'renogy_rover_li'

    sectionMap = {
        'model': {
            'bytes': 8,
            'address': 0x12,
            'type': 'string',
        },
        'system_voltage_current': {
            'bytes': 1,
            'address': 0xa,
            'type': 'float',
        },
        'system_intensity_current': {
            'bytes': 1,
            'address': 0xa,
            'type': 'float',
        },
        'hardware': {
            'bytes': 4,
            'address': 0x14,
            'type': 'string',
        },
        'version': {
            'bytes': 4,
            'address': 0x14,
            'type': 'string',
        },
        'serial_number': {
            'bytes': 2,
            'address': 0x18,
            'type': 'string',
        },
        'battery_percentage': {
            'bytes': 1,
            'address': 0x100,
            'type': 'float',
        },
        'battery_voltage': {
            'bytes': 1,
            'address': 0x101,
            'type': 'float',
        },
        'battery_temperature': {
            'bytes': 1,
            'address': 0x103,
            'type': 'float',
        },
    }

    def __init__ (self, debug=False, port='/dev/ttyUSB0'):
        print('Modelo RenogyRoverLi instanciado')
        self.DEBUG = debug
        self.serial = SerialConnection(port=port, debug=debug, baudrate=9600,
                                       method='rtu', timeout=0.5)

    def get_system_voltage_current (self):
        """
        Devuelve el voltaje actual de consumo en el sistema
        """
        scheme = self.sectionMap['system_voltage_current']

        while True:
            if self.DEBUG:
                print('Leyendo voltaje actual de sistema')

            try:
                response = self.serial.read_register(scheme['address'],
                                                     scheme['bytes'],
                                                     scheme['type'])

                voltage = response >> 8

                return voltage
            except Exception as e:
                if self.DEBUG:
                    print('Error al leer voltaje actual de sistema')
                    print(e)

                sleep(5)

        return None

    def get_system_intensity_current (self):
        """
        Devuelve el consumo en amperios actual de consumo en el sistema
        """
        scheme = self.sectionMap['system_intensity_current']

        while True:
            try:
                if self.DEBUG:
                    print('Leyendo intensidad actual de sistema')

                response = self.serial.read_register(scheme['address'],
                                                     scheme['bytes'],
                                                     scheme['type'])

                amps = response & 0x00ff

                return amps
            except Exception as e:
                if self.DEBUG:
                    print('Error al leer intensidad actual de sistema')
                    print(e)

                sleep(5)

        return None

    def get_hardware (self):
        """
        Devuelve la información para la versión del hardware
        :return:
        """
        if self.DEBUG:
            print('Leyendo hardware')

        scheme = self.sectionMap['hardware']

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        if response:
            major = response[2] & 0x00ff
            minor = response[3] >> 8
            patch = response[3] & 0x00ff

            return 'V{}.{}.{}'.format(major, minor, patch)

        return None

    def get_version (self):
        """
        Devuelve la información sobre la versión del software
        """
        if self.DEBUG:
            print('Leyendo versión')

        scheme = self.sectionMap['version']

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        if response:
            major = response[0] & 0x00ff
            minor = response[1] >> 8
            patch = response[1] & 0x00ff

            return 'V{}.{}.{}'.format(major, minor, patch)

        return None

    def get_serial_number (self):
        """
        Devuelve el número de serie del controlador
        """
        if self.DEBUG:
            print('Leyendo número de serie')

        scheme = self.sectionMap['serial_number']

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        return '{}{}'.format(response[0], response[1]) if response else None

    def get_battery_percentage (self):
        """
        Devuelve el porcentaje de la batería
        :return:
        """
        if self.DEBUG:
            print('Leyendo porcentaje de batería')

        scheme = self.sectionMap['battery_percentage']

        return self.serial.read_register(scheme['address'], scheme['bytes'],
                                         scheme['type'])

    def get_battery_voltage (self):
        """
        Devuelve el voltaje de la batería
        """
        if self.DEBUG:
            print('Leyendo voltaje de batería')

        scheme = self.sectionMap['battery_voltage']

        return self.serial.read_register(scheme['address'], scheme['bytes'],
                                         scheme['type'])

    def get_battery_temperature (self):
        """
        Devuelve la temperatura de la batería
        """
        scheme = self.sectionMap['battery_temperature']

        while True:
            try:
                if self.DEBUG:
                    print('Leyendo temperatura de batería')

                register = self.serial.read_register(scheme['address'],
                                                     scheme['bytes'],
                                                     scheme['type'])
                battery_temp_bits = register & 0x00ff
                temp_value = battery_temp_bits & 0x0ff
                sign = battery_temp_bits >> 7
                battery_temp = -(temp_value - 128) if sign == 1 else temp_value
                return battery_temp
            except Exception as e:
                print(e)
                print('Error al leer temperatura de batería')
                sleep(5)

        return None

    def controller_info (self):
        """
        Devuelve información del controlador de carga solar.
        :return:
        """
        # TODO → Devolver modelo, versión, número de serie, etc.
        datas = {
            'hardware': self.get_hardware(),
            'version': self.get_version(),
            'serial_number': self.get_serial_number(),
        }

        return datas

    def get_all_datas (self):
        datas = {
            'system_voltage_current': self.get_system_voltage_current(),
            'system_intensity_current': self.get_system_intensity_current(),
            'battery_voltage': self.get_battery_voltage(),
            'battery_temperature': self.get_battery_temperature(),
            'battery_percentage': self.get_battery_percentage(),
        }

        return datas

    def tablemodel (self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """
        pass

    def debug (self):
        """
        Función para depurar funcionamiento del modelo proyectando datos por
        consola.
        """
        pass
