from flask import Flask, request, render_template, abort
from flask_jsonpify import jsonify
from access_control_decorator import crossdomain, requires_auth

import redis
import urlparse

app = Flask(__name__)

if __name__ == "__main__":
    app.config.from_object('config.ConfigLocal')
else:
    app.config.from_object('config.ConfigProduction')

#REDIS_URL contains auth+port, but StrictRedis constructor needs it separately
redis_url = urlparse.urlparse(app.config['REDIS_URL'])
r = redis.StrictRedis(host=redis_url.hostname,
                      port=redis_url.port,
                      password=redis_url.password)

@app.route("/")
def home():
    return "Host Counter"

@app.route("/log", methods=['POST','OPTIONS'])
@crossdomain(origin='*')
def log():
    if request.form:
        data = request.form
        if 'host' in data:
            #cache key as {host}:{campaign}:{stat}
            host_key = '%(host)s:%(campaign)s:%(stat)s' % data
            r.zincrby('host', host_key, 1)

            campaign_key = '%(campaign)s:%(stat)s' % data
            r.zincrby('campaign', campaign_key, 1)

            stat_key = '%(stat)s' % data
            r.zincrby('stat', stat_key, 1)

            return jsonify({'status':"OK"})
        else:
            return abort(422, {'error':"missing host"})
    return abort(400, {'error':"missing data"})

@app.route('/list', methods=['GET',])
@requires_auth
def list():
    hosts = r.zrevrange('host',0,10, withscores=True)

    #clean up for display
    top_hosts = []
    for (key,val) in hosts:
        d = { 'host': key.split(':')[0],
              'hits': int(val)
            }
        top_hosts.append(d)

    return render_template('list.html', top_hosts=top_hosts)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
