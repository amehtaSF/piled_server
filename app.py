from flask import Flask, render_template, request, redirect, url_for, make_response, Response
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
    delay_ms = request.args.get("delay_ms")
    
    resp = {"program": program}

    if led_process is not None:
        led_process.kill()
    ''' No color argument functions '''
    
    if program == "rainbowWipe":
        led_process = multiprocessing.Process(target=led.rainbowWipe, 
                                              kwargs={"delay_ms": int(delay_ms)})
    elif program == "rainbowWipeAlwaysOn":
        led_process = multiprocessing.Process(target=led.rainbowWipeAlwaysOn,
                                              kwargs={"delay_ms": int(delay_ms)})
    elif program == "randomWipe":
        led_process = multiprocessing.Process(target=led.randomWipe,
                                              kwargs={"delay_ms": int(delay_ms)})
    # if program == "rainbowCycle":
    #     led_process = multiprocessing.Process(target=led.rainbowCycle)
    elif program == "theaterChaseRainbow":
        led_process = multiprocessing.Process(target=led.theaterChaseRainbow,
                                              kwargs={"delay_ms": int(delay_ms)})
    elif program == "theaterChase":
        rgb = (int(R), int(G), int(B))
        led_process = multiprocessing.Process(target=led.theaterChase,
                                              kwargs={"rgb": rgb,
                                                      "delay_ms": int(delay_ms)})
        
    elif program == "theaterChaseRainbow":
        led_process = multiprocessing.Process(target=led.theaterChaseRainbow,
                                              kwargs={"delay_ms": int(delay_ms)})
        
    elif program == "solidColor":
        rgb = (int(R), int(G), int(B))
        led_process = multiprocessing.Process(target=led.solidColor,
                                              kwargs={"rgb": rgb})
        
    elif program == "colorWipe":
        rgb = (int(R), int(G), int(B))
        led_process = multiprocessing.Process(target=led.colorWipe,
                                              kwargs={"rgb": rgb,
                                                      "delay_ms": int(delay_ms)})
        
    elif program == "rainbowWipe":
        led_process = multiprocessing.Process(target=led.rainbowWipe,
                                              kwargs={"delay_ms": int(delay_ms)})
        
    elif program == "colorShots":
        led_process = multiprocessing.Process(target=led.colorShotsMultiple)

    elif program == "clear":
        led_process = multiprocessing.Process(target=led.clear)
    else:
        resp = resp.update({"status": "error", "message": "Invalid program"})
        resp = Response(resp, status=400, mimetype="application/json")
        return resp

    led_process.start()

    resp = resp.update({"status": "ok"})
    resp = Response(resp, status=200, mimetype="application/json")
    return resp

@app.route("/get_state", methods=["GET"])
def get_state():
    global led
    resp = {"R": led.rgb[0], "G": led.rgb[1], "B": led.rgb[2],
            "delay_ms": led.delay_ms,
            "current_pattern": led.current_pattern}
    resp = Response(resp, status=200, mimetype="application/json")
    return resp


# @app.route("/get_rgb", methods=["GET"])
# def get_rgb():
#     global led
#     rgb = led.get_rgb()
#     resp = {"R": rgb[0], "G": rgb[1], "B": rgb[2]}
#     resp = Response(resp, status=200, mimetype="application/json")
#     return resp

# @app.route("/set_rgb", methods=["GET"])
# def set_rgb():
#     global led
#     R = request.args.get("R")
#     G = request.args.get("G")
#     B = request.args.get("B")
#     led.set_rgb((int(R), int(G), int(B)))
#     resp = {"status": "ok"}
#     resp = Response(resp, status=200, mimetype="application/json")
#     return resp

# @app.route("/get_delay_ms", methods=["GET"])
# def get_delay_ms():
#     global led
#     delay_ms = led.get_delay_ms()
#     resp = {"delay_ms": delay_ms}
#     resp = Response(resp, status=200, mimetype="application/json")
#     return resp

# @app.route("/set_delay_ms", methods=["GET"])
# def set_delay_ms():
#     global led
#     delay_ms = request.args.get("delay_ms")
#     led.set_delay_ms(int(delay_ms))
#     resp = {"status": "ok"}
#     resp = Response(resp, status=200, mimetype="application/json")
#     return resp






if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')