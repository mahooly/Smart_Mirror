Smart Mirror
===============
Backend implemented with Django (Asynchronous Django), communication and sensor update with MQTT, and integrated Google account information.

* Install dependencies: ``pip install -r requirements.txt``
* Start ``redis``
* Start MQTT broker (e.g. ``mosquitto``)
* Migrate models ``./manage.py migrate``
* Run ``asgimqtt``
* Run webserver ``./manage.py runserver``
* Open http://localhost:8000
