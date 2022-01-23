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
            'bytes': 2,
            'address': 0xa,
            'type': 'float',
        },
        'system_intensity_current': {
            'bytes': 2,
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
            'bytes': 4,
            'address': 0x18,
            'type': 'string',
        },
        'battery_percentage': {
            'bytes': 2,
            'address': 0x100,
            'type': 'float',
        },
        'battery_voltage': {
            'bytes': 2,
            'address': 0x101,
            'type': 'float',
        },
        'battery_temperature': {
            'bytes': 2,
            'address': 0x103,
            'type': 'float',
        },
        'controller_temperature': {
            'bytes': 2,
            'address': 0x103,
            'type': 'float',
        },
        'load_voltage': {
            'bytes': 2,
            'address': 0x104,
            'type': 'float',
        },
        'load_current': {
            'bytes': 2,
            'address': 0x105,
            'type': 'float',
        },
        'load_power': {
            'bytes': 2,
            'address': 0x106,
            'type': 'float',
        },
        'solar_voltage': {
            'bytes': 2,
            'address': 0x107,
            'type': 'float',
        },
        'solar_current': {
            'bytes': 2,
            'address': 0x108,
            'type': 'float',
        },
        'solar_power': {
            'bytes': 2,
            'address': 0x109,
            'type': 'float',
        },
    }

    def __init__ (self, debug=False, port='/dev/ttyUSB0'):
        self.DEBUG = debug
        self.serial = SerialConnection(port=port, debug=debug, baudrate=9600,
                                       method='rtu', timeout=0.5)

        if (debug):
            print('Modelo RenogyRoverLi instanciado')

    def get_system_voltage_current (self):
        """
        Devuelve el voltaje actual de consumo en el sistema
        0x000A
        [1] → 8 higher bits: max. voltage supported by the system (V)
        """
        scheme = self.sectionMap['system_voltage_current']

        while True:
            if self.DEBUG:
                print('Leyendo voltaje actual de sistema')

            try:
                response = self.serial.read_register(scheme['address'],
                                                     scheme['bytes'],
                                                     scheme['type'])

                voltage = response[0] >> 8

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
        0x000A
        lower bits: rated charging current (A)
        """
        scheme = self.sectionMap['system_intensity_current']

        while True:
            try:
                if self.DEBUG:
                    print('Leyendo intensidad actual de sistema')

                response = self.serial.read_register(scheme['address'],
                                                     scheme['bytes'],
                                                     scheme['type'])

                amps = response[0] & 0x00ff

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
        0x0016 y 0x0017 Hardware version 4 bytes

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
        0x0014 y 0x0015 Software version 4 bytes
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
        0x0018 y 0x0019 Serial number 4 bytes
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
        0x0100 Battery capacity SOC 2 bytes
        Current battery capacity value 0-100 (%)
        :return:
        """
        if self.DEBUG:
            print('Leyendo porcentaje de batería')

        scheme = self.sectionMap['battery_percentage']

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                         scheme['type'])

        return response[0] if response else None

    def get_battery_voltage (self):
        """
        Devuelve el voltaje de la batería
        0x0101 Battery voltage 2 bytes
        Battery voltage * 0.1 (V)
        """
        if self.DEBUG:
            print('Leyendo voltaje de batería')

        scheme = self.sectionMap['battery_voltage']

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        return float(response[0]) / 10 if response else None

    def get_battery_temperature (self):
        """
        Devuelve la temperatura de la batería en su exterior (sensor externo)
        0x0103 Battery temperature 2 bytes
        Actual temperature value (b7: sign bit; b0-b6: temperature value) (ºC)
        """
        scheme = self.sectionMap['battery_temperature']

        while True:
            try:
                if self.DEBUG:
                    print('Leyendo temperatura de batería')

                response = self.serial.read_register(scheme['address'],
                                                     scheme['bytes'],
                                                     scheme['type'])
                battery_temp_bits = response[0] & 0x00ff
                temp_value = battery_temp_bits & 0x0ff
                sign = battery_temp_bits >> 7

                return -(temp_value - 128) if sign == 1 else temp_value
            except Exception as e:
                print(e)
                print('Error al leer temperatura de batería')
                sleep(5)

        return None

    def get_controller_temperature(self):
        """
        Devuelve la temperatura del controlador de carga
        0x0103 Controller temperature 2 bytes
        Actual temperature value (b7: sign bit; b0-b6: temperature value) (ºC)
        """
        scheme = self.sectionMap['controller_temperature']

        if self.DEBUG:
            print('Leyendo temperatura del controlador solar')

        response = self.serial.read_register(scheme['address'],
                                             scheme['bytes'],
                                             scheme['type'])
        controller_temp_bits = response[0] >> 8
        temp_value = controller_temp_bits & 0x0ff
        sign = controller_temp_bits >> 7

        return -(temp_value - 128) if sign == 1 else temp_value

    def get_load_voltage(self):
        """
        Devuelve el voltaje de la carga actual
        0x0104 Load voltage 2 bytes
        Street light voltage * 0.1 (V)
        """
        scheme = self.sectionMap['load_voltage']

        if self.DEBUG:
            print('Leyendo voltaje para la carga actual de consumo')

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        return float(response[0]) / 10 if response else None

    def get_load_current(self):
        """
        Devuelve la intensidad de la carga actual
        0x0105 Load current 2 bytes
        Street light current * 0.01 (A)
        """
        scheme = self.sectionMap['load_current']

        if self.DEBUG:
            print('Leyendo intensidad para la carga actual de consumo')

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        return float(response[0]) / 100 if response else None

    def get_load_power(self):
        """
        Devuelve la intensidad de la carga actual
        0x0105 Load current 2 bytes
        Street light power (W)
        """
        scheme = self.sectionMap['load_power']

        if self.DEBUG:
            print('Leyendo potencia para la carga actual de consumo')

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        return response[0] if response else None

    def get_solar_voltage(self):
        """
        Devuelve la tensión del panel solar actualmente.
        0x0107 Solar panel voltage
        Solar panel voltage * 0.1 (V)
        """
        scheme = self.sectionMap['solar_voltage']

        if self.DEBUG:
            print('Leyendo voltaje del panel solar actualmente')

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        return float(response[0]) / 10 if response else None

    def get_solar_current(self):
        """
        Devuelve la intensidad del panel solar actualmente.
        0x0108 Solar panel current (to controller)
        Solar panel current * 0.01 (A)
        """
        scheme = self.sectionMap['solar_current']

        if self.DEBUG:
            print('Leyendo intensidad del panel solar actualmente')

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        return float(response[0]) / 100 if response else None

    def get_solar_power(self):
        """
        Devuelve la potencia del panel solar actualmente.
        0x0109 Solar charging power
        Solar charging power (W)
        """
        scheme = self.sectionMap['solar_power']

        if self.DEBUG:
            print('Leyendo potencia del panel solar actualmente')

        response = self.serial.read_register(scheme['address'], scheme['bytes'],
                                             scheme['type'])

        return response[0] if response else None

    def get_controller_info (self):
        """
        Devuelve información del controlador de carga solar.
        :return:
        """
        return {
            'hardware': self.get_hardware(),
            'version': self.get_version(),
            'serial_number': self.get_serial_number(),
            'system_voltage_current': self.get_system_voltage_current(),
            'system_intensity_current': self.get_system_intensity_current(),
        }

    def get_all_solar_panel_info_datas(self):
        """
        Devuelve toda la información de los paneles solares.
        :return:
        """
        return {
            'solar_current': self.get_solar_current(),
            'solar_voltage': self.get_solar_voltage(),
            'solar_power': self.get_solar_power(),
        }

    def get_all_datas (self):
        """
        Devuelve todos los datos del controlador de carga solar
        :return:
        """
        return {
            'battery_voltage': self.get_battery_voltage(),
            'battery_temperature': self.get_battery_temperature(),
            'battery_percentage': self.get_battery_percentage(),
            'controller_temperature': self.get_controller_temperature(),
            'load_voltage': self.get_load_voltage(),
            'load_current': self.get_load_current(),
            'load_power': self.get_load_power(),
            'solar_current': self.get_solar_current(),
            'solar_voltage': self.get_solar_voltage(),
            'solar_power': self.get_solar_power(),
        }

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
