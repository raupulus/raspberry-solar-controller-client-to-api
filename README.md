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
- Puerto Serial USB UART TTL (3,3V o 5v según conversor)
- Conversor RS232 a UART TTL (MAX23232)
- Cable RJ11

## Software

- Raspbian (Debian 12)
- Python 3.10
- Postgresql

## Módulos python

- python3-serial 
- python3-requests
- python3-sql
- python3-postgresql
- python3-sqlalchemy
- python3-dotenv
- python3-smbus
- python3-rpi.gpio
- python3-pip
- python3-psycopg2

Para instalarlos todos en raspbian sería esta línea:

```bash
sudo apt install python3-dotenv python3-serial python3-requests \
python3-sql python3-postgresql python3-sqlalchemy python3-dotenv python3-smbus \
python3-rpi.gpio python3-pip python3-psycopg2
```

De todas formas, tener en cuenta que los nombres y origen de los paquetes pueden
cambiar. Tal vez en futuras versiones se necesite algunos instalar desde pip.

## Models

Hasta el momento he utilizado esto con mi propio cargador solar por lo que solo
dispone de este modelo:

- RenogyRoverLi

Si tienes un controlador distinto, tendrías que crear un modelo para ese 
heredando los métodos de AbstractModel e instanciarlo en main.py reemplazando
el modelo de RenogyRoverLi.

## Instalación

A continuación describo los pasos para instalar que he ido usando durante el
desarrollo de la aplicación, será necesario adaptar a vuestra situación cada
paso.

Para el desarrollo trabajo en el directorio **git** dentro del **home** del
usuario por defecto: **/home/pi/git/raspberry-solar-controller-client-to-api**

El SGBD que utilizo es Postgresql, si prefieres otro debería funcionar igualmente
ya que para ello utilizo SqlAlchemy intentnado abstraer esa parte.

En mi caso tengo varias aplicaciones que utilizan PostgreSQL, por lo que he 
decido seguir usándolo también para esta aplicación en lugar de instalar otro.

### Crear usuario y base de datos solar_controller

Creo el usuario para postgresql

```bash
sudo -u postgres createuser pi
```

Al crear el usuario así, tal vez necesitemos cambiar la contraseña del
usuario recién creado.

Para ello entramos al intérprete de comandos para postgres con **psql**

```bash
sudo -u postgres psql
```

Una vez dentro le pedimos cambiar la contraseña del usuario **pi**:

```postgresql
\password pi
```

Creo la base de datos para almacenar las lecturas hasta que sean subidas:

```bash
sudo -u postgres createdb -O pi -T template1 solar_controller
```

### Clonar repositorio

Creamos el directorio git y entramos a él, si deseamos otro directorio no
es inconveniente mientras existan permisos adecuados para el usuario.

```bash
mkdir /home/pi/git && cd /home/pi/git
git clone https://gitlab.com/raupulus/raspberry-solar-controller-client-to-api.git
```

### Asignar tarea cron para ejecutarse automáticamente al iniciar la raspberry.

Podemos hacer que se inicie automáticamente al iniciar nuestra raspberry y
de esta forma asegurarnos que siempre tomará datos aunque sea reiniciada.

En el crontab se añade la línea hacia el script indicando que lo ejecute nuestro
usuario.

Adicionalmente guardo toda la salida en un log temporal dentro de **/tmp**,
esto tiene el inconveniente de que se pierde al reiniciar. Lo mantengo así
pues solo lo utilizo para depurar la salida y ver errores que pueda ir
corrigiendo. Puedes utilizar cualquier directorio para mantener permanente el
log.

Nótese que al crontab le asigno un retardo de 50 segundos para dejar tiempo a
terminar de cargar el sistema (no era necesario pero así aseguro que se
ejecuta correctamente ya que inicio bastantes aplicaciones y servicios).

Añadir la siguiente línea a crontab:

@reboot pi sleep 50 && python3 /home/pi/git/raspberry-solar-controller-client-to-api/main.py >> /tmp/log-raspberry-solar-controller-client-to-api.log 2>> /tmp/log-raspberry-solar-controller-client-to-api.log
