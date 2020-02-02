from bottle import Bottle, request
import json

app = Bottle()
@app.get('/')
def api():
    my_dict = request.params.decode()
    return json.dumpd(my_dict)