from flask import Flask
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__, static_folder="")

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<p><i>cannot connect to Redis, counter disabled,</i></p>"

    html = "<title>Favorite meme!</title>" \
    	   " <h1>The best meme is kind meme :)</h1> " \
           "<p><img src = 'meme.png' alt ='Dog walk - meme'/></p>" \
           "<p><b>Visits:</b> {visits}</p>"

    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)


