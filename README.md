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

Deploy to Heroku with a Redis add-on. You may need to adjust the config variables to export to REDIS_URL.

Benchmarking
-----

On Heroku with 4 dynos, we can measure over 300 req/sec using ApacheBench:

    ab -n 1000 -c 100 -T application/x-www-form-urlencoded -p post.data http://host-counter.herokuapp.com/log

With more realistic AJAX requests, we measure only about 50 req/sec:

    http://jsfiddle.net/jlevinger/w008sgrs/1/
