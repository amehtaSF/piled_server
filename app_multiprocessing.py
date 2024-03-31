from flask import Flask, render_template, request, redirect, url_for, make_response, Response, current_app
import multiprocessing


from led import LED


app = Flask(__name__)

led = LED()
led_process = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/led", methods=["GET"])
def led_program():
    global led
    global led_process
    program = request.args.get("program")
    R = request.args.get("R")
    G = request.args.get("G")
    B = request.args.get("B")
    resp = {"program": program}

    if led_process is not None:
        led_process.kill()

    if program == "rainbowWipe":
        led_process = multiprocessing.Process(target=led.rainbowWipe)
    if program == "clear":
        led_process = multiprocessing.Process(target=led.clear)
    led_process.start()

    resp = resp.update({"status": "ok"})
    resp = Response(resp, status=200, mimetype="application/json")
    return resp


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')