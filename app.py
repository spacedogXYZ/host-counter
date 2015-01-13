from flask import Flask, request, render_template
from flask_jsonpify import jsonify
from access_control_decorator import crossdomain, requires_auth

import redis
import json

app = Flask(__name__)
app.config.from_object('config.ConfigProduction')

r = redis.StrictRedis(host=app.config['REDIS_URL'], port=6379, db=0)

@app.route("/")
def home():
    return "Host Counter"

@app.route("/log", methods=['POST',])
@crossdomain('*')
def log():
    if request.data:
        data = json.loads(request.data)
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
            return jsonify({'error':"missing host"})
    return jsonify({'error':"missing data"})

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
    # load the debugger config
    app.config.from_object('config.ConfigLocal')
    app.run(host='0.0.0.0')