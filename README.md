# raspberry-solar-controller-client-to-api

Proyecto para utilizar una raspberry pi como cliente para rs232/ttl/rs485 de un controlador de carga solar desde el que obtener información para subirla a una API REST


## Hardware

Para este proyecto solo es necesario una raspberry aunque según el tipo de
controlador de carga y requisitos de la conexión es posible necesitar elementos
para la conectividad SERIAL o adaptar la transmisión.

Por ejemplo, en mi caso usando un Renogy Rover LI de 20A RS232 he necesitado
para un correcto funcionamiento un conversor de RS232 a UART TTL. He optado
por usar un puerto UART TTL por USB ya que en mi caso con la raspberry pi 4 me 
ha sido más fácil de conectar sin perder funcionalidades o velocidad al 
obtener los datos.

Estos son los elementos
- Raspberry pi 4 (2 GB RAM)
- Puerto Serial USB UART TTL (3,3V)
- Conversor RS232 a UART TTL (MAX23232)
- Cable RJ11

## Software

- Raspbian (Debian 11)
- Python 3.9
- Postgresql

## Módulos python

- python3-serial 
- python3-pyserial
- python3-requests
- python3-sql
- python3-postgresql
- python3-sqlalchemy
- python3-dotenv
- python3-smbus
- python3-rpi.gpio
- python3-pip

Para instalarlos todos en raspbian sería esta línea:

```bash
sudo apt install python3-dotenv python3-serial python3-pyserial python3-requests \
python3-sql python3-postgresql python3-sqlalchemy python3-dotenv python3-smbus \
python3-rpi.gpio python3-pip
```

De todas formas, tener en cuenta que los nombres y origen de los paquetes pueden
cambiar. Tal vez en futuras versiones se necesite algunos instalar desde pip.
