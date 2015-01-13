Host Counter
============

Simple hit counter, aggregating by hostname

Requires:

* Python
* Flask
* Redis

Development
-----

To install locally and run in debug mode use:

  # create virtual environment
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt

  # set ENV variables
  source secrets.sh

  # start redis
  redis-server /usr/local/etc/redis.conf

  # start flask
  python app.py

When the dev server is running, the demo front-end will be accessible at http://localhost:5000/list.

Production
-----

Heroku
