from flask import Flask, render_template, request, redirect, url_for, make_response, Response

# import threading
from led_threading import LED


app = Flask(__name__)

led = LED()

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
    if program == "rainbow":
        led.stop_pattern()
        led.start_pattern(led.rainbow)
    elif program == "rainbowCycle":
        led.stop_pattern()
        led.start_pattern(led.rainbowCycle)
    elif program == "theaterChaseRainbow":
        led.stop_pattern()
        led.start_pattern(led.theaterChaseRainbow)
    elif program == "theaterChase":
        led.stop_pattern()
        led.start_pattern(lambda: led.theaterChase(led.strip, (R, G, B)))
        resp.update({"R": R, "G": G, "B": B})
    elif program == "colorWipe":
        led.stop_pattern()
        led.start_pattern(lambda: led.colorWipe(led.strip, (R, G, B)))
        resp.update({"R": R, "G": G, "B": B})
    elif program == "clear":
        led.stop_pattern()
        led.start_pattern(led.clear)
    resp = resp.update({"status": "ok"})
    resp = Response(resp, status=200, mimetype="application/json")
    return resp


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')