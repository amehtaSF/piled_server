from flask import Flask, render_template, request, redirect, url_for, make_response, Response
from celery import Celery


from led import LED


app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


led = LED()

@celery.task
def led_celery(program, R=None, G=None, B=None):
    global led
    resp = {"program": program}
    if program == "rainbow":
        led.rainbow()
    elif program == "rainbowCycle":
        led.rainbowCycle()
    elif program == "theaterChaseRainbow":
        led.theaterChaseRainbow()
    elif program == "theaterChase":
        led.theaterChase(led.strip, (R, G, B))
        resp.update({"R": R, "G": G, "B": B})
    elif program == "colorWipe":
        led.colorWipe(led.strip, (R, G, B))
        resp.update({"R": R, "G": G, "B": B})
    elif program == "clear":
        led.clear()
    resp = resp.update({"status": "ok"})
    return resp

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/led", methods=["GET"])
def led_program():
    
    global led
    program = request.args.get("program")
    R = request.args.get("R")
    G = request.args.get("G")
    B = request.args.get("B")
    resp = {"program": program}
    task = led_celery.delay(program, R, G, B)
    resp = resp.update({"status": "ok"})
    resp = Response(resp, status=200, mimetype="application/json")
    return resp


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')