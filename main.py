from bottle import Bottle, request
import json
from html_telegraph_poster import TelegraphPoster

app = Bottle()

graph = TelegraphPoster()

@app.get('/create_api_token')
def create_api_token():
	kwargs = {
		'short_name': None,
		'author_name': None,
		'author_url': None,
	}

	args_raw = request.params.decode().dict
	args = {i: args_raw[i][0] for i in args_raw}

	kwargs.update(args)
	kwargs = {i: kwargs[i] for i in ['short_name', 'author_name', 'author_url']}

	if kwargs['author_name'] == None:
		return 400 #418 :)

	return graph.create_api_token(**kwargs)

app.run(host='0.0.0.0', port=8080)