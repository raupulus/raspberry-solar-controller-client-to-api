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



#######################################
# #            FUNCIONES            # #
#######################################

"""
Driver for the Renogy Rover Solar Controller using the Modbus RTU protocol
"""

import minimalmodbus
import time

sleep = time.sleep

DEBUG = True

minimalmodbus.BAUDRATE = 9600
minimalmodbus.MODE_RTU = 'rtu'
minimalmodbus.TIMEOUT = 0.05
minimalmodbus.PARITY = 'N'
minimalmodbus.BYTESIZE = 8
minimalmodbus.STOPBITS = 1
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
minimalmodbus.Instrument.debug = True
minimalmodbus.Instrument.BAUDRATE = 9600
minimalmodbus.BYTEORDER_LITTLE = 1

BATTERY_TYPE = {
    1: 'open',
    2: 'sealed',
    3: 'gel',
    4: 'lithium',
    5: 'self-customized'
}

CHARGING_STATE = {
    0: 'deactivated',
    1: 'activated',
    2: 'mppt',
    3: 'equalizing',
    4: 'boost',
    5: 'floating',
    6: 'current limiting'
}


class RenogyRover(minimalmodbus.Instrument):

    """
    Communicates using the Modbus RTU protocol (via provided USB<->RS232 cable)
    """

    def __init__(self, portname, slaveaddress):

        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)

    def model(self):
        """
        Read the controller's model information
        """
        return self.read_string(12, numberOfRegisters=8)

    def system_voltage_current(self):
        """
        Read the controler's system voltage and current
        Returns a tuple of (voltage, current)
        """

        while True:
            try:

                register = self.read_register(10)

                print(register)
                amps = register & 0x00ff
                voltage = register >> 8
                return (voltage, amps)
            except Exception(e):
                print(e)
                sleep(5)

        return None

    def version(self):
        """
        Read the controler's software and hardware version information
        Returns a tuple of (software version, hardware version)
        """
        registers = self.read_registers(20, 4)
        soft_major = registers[0] & 0x00ff
        soft_minor = registers[1] >> 8
        soft_patch = registers[1] & 0x00ff
        hard_major = registers[2] & 0x00ff
        hard_minor = registers[3] >> 8
        hard_patch = registers[3] & 0x00ff
        software_version = 'V{}.{}.{}'.format(
            soft_major, soft_minor, soft_patch)
        hardware_version = 'V{}.{}.{}'.format(
            hard_major, hard_minor, hard_patch)
        return (software_version, hardware_version)

    def serial_number(self):
        """
        Read the controller's serial number
        """
        registers = self.read_registers(24, 2)
        return '{}{}'.format(registers[0], registers[1])

    def battery_percentage(self):
        """
        Read the battery percentage
        """
        return self.read_register(256) & 0x00ff

    def battery_voltage(self):
        """
        Read the battery voltage
        """
        return self.read_register(257, numberOfDecimals=1)

    def battery_temperature(self):
        """
        Read the battery surface temperature
        """
        while True:
            try:

                register = self.read_register(259)
                battery_temp_bits = register & 0x00ff
                temp_value = battery_temp_bits & 0x0ff
                sign = battery_temp_bits >> 7
                battery_temp = -(temp_value - 128) if sign == 1 else temp_value
                return battery_temp
            except Exception as e:
                print(e)
                sleep(5)

        return None

    def controller_temperature(self):
        """
        Read the controller temperature
        """
        register = self.read_register(259)
        controller_temp_bits = register >> 8
        temp_value = controller_temp_bits & 0x0ff
        sign = controller_temp_bits >> 7
        controller_temp = -(temp_value - 128) if sign == 1 else temp_value
        return controller_temp

    def load_voltage(self):
        """
        Read load (raspberrypi) voltage
        """
        return self.read_register(260, numberOfDecimals=1)

    def load_current(self):
        """
        Read load (raspberrypi) current
        """
        return self.read_register(261, numberOfDecimals=2)

    def load_power(self):
        """
        Read load (raspberrypi) power
        """
        return self.read_register(262)

    def solar_voltage(self):
        """
        Read solar voltage
        """
        return self.read_register(263, numberOfDecimals=1)

    def solar_current(self):
        """
        Read solar current
        """
        return self.read_register(264, numberOfDecimals=2)

    def solar_power(self):
        """
        Read solar power
        """
        return self.read_register(265)

    def charging_amp_hours_today(self):
        """
        Read charging amp hours for the current day
        """
        return self.read_register(273)

    def discharging_amp_hours_today(self):
        """
        Read discharging amp hours for the current day
        """
        return self.read_register(274)

    def power_generation_today(self):

        return self.read_register(275)

    def charging_status(self):

        return self.read_register(288) & 0x00ff

    def charging_status_label(self):

        return CHARGING_STATE.get(self.charging_status())

    def battery_capacity(self):

        return self.read_register(57346)

    def voltage_setting(self):

        register = self.read_register(57347)
        setting = register >> 8
        recognized_voltage = register & 0x00ff
        return (setting, recognized_voltage)

    def battery_type(self):

        register = self.read_register(57348)
        return BATTERY_TYPE.get(register)

    # TODO: resume at 3.10 of spec


if __name__ == "__main__":

    """
    for x in range(0, 255):
        try:
            print('Leyendo rango: ', x)
            rover = RenogyRover('/dev/ttyUSB0', x)
            print('Version: ', rover.version())
            print('Serial_number: ', rover.serial_number())
            break
        except Exception as e:
            print('Nada en rango', x)
    """

    rover = RenogyRover('/dev/ttyUSB0', 1)
 #   print('Model: ', rover.model())
    print('Version: ', rover.version())
    print('Serial_number: ', rover.serial_number())
    print('Battery %: ', rover.battery_percentage())
    # print('Battery Type: ', rover.battery_type())
    # print('Battery Capacity: ', rover.battery_capacity())
    # print('Battery Voltage: ', rover.battery_voltage())

    battery_temp = rover.battery_temperature()

    print('Battery Temperature: ', battery_temp, battery_temp * 1.8 + 32)

    controller_temp = rover.controller_temperature()

    # print('Controller Temperature: ', controller_temp, controller_temp * 1.8 + 32)
    # print('Load Voltage: ', rover.load_voltage())
    # print('Load Current: ', rover.load_current())
    # print('Load Power: ', rover.load_power())
    # print('Charging Status: ', rover.charging_status_label())
    # print 'solar ' 'voltage='+str(rover.solar_voltage())
    # print('Solar Current: ', rover.solar_current())
    # print('Solar Power: ', rover.solar_power())
    # print('Power Generated Today (kilowatt hours): ', rover.power_generation_today())
    # print('Charging Amp/Hours Today: ', rover.charging_amp_hours_today())
    # print('Discharging Amp/Hours Today: ', rover.discharging_amp_hours_today())
    print("solar_shed " "solar_volts="+str(rover.solar_voltage())+",amp_charge_today="+str(rover.charging_amp_hours_today())+",amp_discharge_today="+str(rover.discharging_amp_hours_today())+",battery_percent="+str(rover.battery_percentage())+",battery_volts="+str(rover.battery_voltage())+",solar_amps="+str(rover.solar_current()
                                                                                                                                                                                                                                                                                                                    )+",load_volts="+str(rover.load_voltage())+",load_amps="+str(rover.load_current())+",load_watts="+str(rover.load_power())+",solar_watts="+str(rover.solar_power())+",watts_gen_today="+str(rover.power_generation_today())+",temp_controller="+str(controller_temp * 1.8 + 32)+",temp_battery="+str(battery_temp * 1.8 + 32))


# Necesita módulos → pip3 install -U minimalmodbus modbus
# sudo apt install python3-serial python3-pymodbus python3-dbus python3-serial

## TODO → Crear interfaz para todos los modelos de controladores solares
## Crear modelo para controlador solar renogy-rover
## Crear clase para modelo de datos obtenidos del controlador solar
## Crear clase para la conexión a la db
## Crear clase para representar la conexión a la api








