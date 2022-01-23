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

from abc import ABC, abstractmethod


#######################################
# #            FUNCIONES            # #
#######################################

class AbstractModel(ABC):
    """
    Tipos de baterías.
    """
    BATTERY_TYPE = {
        1: 'open',
        2: 'sealed',
        3: 'gel',
        4: 'lithium',
        5: 'self-customized'
    }

    """
    Estados de carga para la batería.
    """
    CHARGING_STATE = {
        0: 'deactivated',
        1: 'activated',
        2: 'mppt',
        3: 'equalizing',
        4: 'boost',
        5: 'floating',
        6: 'current limiting'
    }

    @property
    def table_name (self):
        """
        Nombre de la tabla en la base de datos.
        :return:
        """
        pass

    @abstractmethod
    def get_today_historical_info_datas (self):
        """
        Devuelve una lista con los datos históricos para el día actual
        :return:
        """
        pass

    @abstractmethod
    def get_historical_info_datas (self):
        """
        Devuelve una lista con los datos históricos generales
        :return:
        """
        pass

    @abstractmethod
    def get_all_controller_info_datas (self):
        """
        Devuelve información del controlador de carga solar.
        :return:
        """
        pass

    @abstractmethod
    def get_all_solar_panel_info_datas (self):
        """
        Devuelve toda la información de los paneles solares.
        :return:
        """
        pass

    @abstractmethod
    def get_all_datas (self):
        """
        Devuelve un diccionario con los datos (coincidiendo con el tablemodel)
        según lo tomado desde controlador.
        """
        pass

    @abstractmethod
    def tablemodel (self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """
        pass

    @abstractmethod
    def debug (self):
        """
        Función para depurar funcionamiento del modelo proyectando datos por
        consola.
        """
        pass

