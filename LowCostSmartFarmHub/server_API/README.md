This Folder Contains the Docker.yml file and other folders for running the Server Applications

-MQTT Server on Port 1883
-Influx DB on Port 8086
-Grafana on Port 3000

The work is based on [Gautier Mechling](https://github.com/Nilhcem)'s
[home-monitoring-grafana](https://github.com/Nilhcem/home-monitoring-grafana)
repository, described in his blog post

### Installing docker and docker compose to your *server*

Install
[docker](https://docs.docker.com) and
[docker-compose](https://docs.docker.com/compose/), if you don't have
them installed in your *server* yet.
If you don't know if you have them installed or not, simply try to run the
commands `docker` and `docker-compose` on the command line.

For Windows or Mac OS X, the easiest way is to install
[Docker for Desktop](https://www.docker.com/products/docker-desktop).
Alternatively, for Mac OS X you can use [Homebrew](https://brew.sh),
with `brew install docker docker-compose`.

For Linux (Ubuntu or other Debian based), just use `apt install`:

```sh
   sudo apt install docker.io
   sudo apt install docker-compose
```

For anything else, follow the [official instructions](https://docs.docker.com/install/).

## Running Mosquitto + InfluxDB + Grafana in docker, in your *server*

Set the `DATA_DIR` environment variable to the path where will be stored local data, e.g. `/tmp`
if you are just testing.  For your Smart Farm Hub  demonstration or other "production", choose
something else.

```sh
   export DATA_DIR=/tmp
```
(Note: For Mac OS X with Docker for Desktop, use `export DATA_DIR=/private/tmp` instead,
as docker has problems in understanding that `/tmp` is a symbolic link.)

Create data directories, with write access for the Mosquitto and Grafana containers:

```sh
   mkdir -p ${DATA_DIR}/mosquitto/data ${DATA_DIR}/mosquitto/log ${DATA_DIR}/influxdb ${DATA_DIR}/grafana
   sudo chown -R 1883:1883 ${DATA_DIR}/mosquitto
   sudo chown -R 472:472 ${DATA_DIR}/grafana
```

Run docker compose:

```sh
   cd 00-docker
   docker-compose up -d
```

This starts four containers on your *server*: Mosquitto, InfluxDB, Grafana, and
the Mosquitto-to-InfluxDB bridge from the `02-bridge` folder.  You can check that
they are nicely up and running with

```sh
   docker ps
```

You should see all the four containers running continuously, and not restarting.
If any of them is restarting, you can use `docker logs <container-name>` to see its
logs, or `docker exec -it <container-name> sh` to run a shell in the container.

To shut down your containers, e.g. if you need to change the settings, run
```sh
   docker-compose down
```

You can now test your Granafa at http://<your-server-ip>:3000.  See below how to
log in to and configure Grafana, and how to get the data flowing.

The Mosquitto username and passwords are `mqttuser` and `mqttpassword`.
To change these, see the **Optional: Update mosquitto credentials** section below.

## Grafana setup

It is a good idea to log in your Grafana right away and change your
`admin` password.  You can also add an InfluxDB data source already now,
or later.  For having a meaningful Dashboard, you must first get some
data to your InfluxDB database.

- Access Grafana from `http://<your-server-ip>:3000`
- Log in with user/password `admin/admin`
- Go to Configuration > Data Sources
- Add data source (InfluxDB)
  - Name: `InfluxDB`
  - URL: `http://influxdb:8086`
  - Database: `iothon_db`
  - User: `root`
  - Password: `root`
  - Save & Test
- Create a Dashboard
  - Add Graph Panel
  - Edit Panel
  - Data Source: InfluxDB
  - FROM: `[default] [temperature] WHERE [location]=[bme280]`
  - SELECT: `field(value)`
  - FORMAT AS: `Time series`
  - Draw mode: Lines
  - Stacking & Null value: Null value [connected]
  - Left Y
    - Unit: Temperature > Celcius
  - Panel title: Temperature (°C)
