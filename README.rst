==============
Smart Farm Hub
==============


.. image:: https://img.shields.io/pypi/v/LowCostSmartFarmHub.svg
        :target: https://pypi.python.org/pypi/LowCostSmartFarmHub

.. image:: https://img.shields.io/travis/itumeleng96/LowCostSmartFarmHub.svg
        :target: https://travis-ci.com/itumeleng96/LowCostSmartFarmHub

.. image:: https://readthedocs.org/projects/LowCostSmartFarmHub/badge/?version=latest
        :target: https://LowCostSmartFarmHub.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Gateway API for a Zigbee Wireless Network and Cloud Based Docker image for a smart farm hub written in Python 


* Free software: MIT license
* Documentation: https://LowCostSmartFarmHub.readthedocs.io.


Features
--------

* Add a range of Zigbee Devices or Sensors or Actuators to a RPI machine interface
* Add sensors or actuators to Xbee3 modules
* Publish sensor information to MQTT broker on the cloud
* Connect to the Web application to monitor and control the wireless sensor network remotely
* Automatically Detect new devices on the network and sensors
* Send commands from grafana to wireless sensor network

.. image:: https://github.com/itumeleng96/LowCostSmartFarmHub/blob/master/images/smartFarmHub.png
 
Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


The server Docker container instructions were adopted from https://github.com/iothon/docker-compose-mqtt-influxdb-grafana
