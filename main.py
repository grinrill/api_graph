from bottle import Bottle, request
import json
from html_telegraph_poster import TelegraphPoster
from html_telegraph_poster.html_to_telegraph import _upload_via_api as upload
import urllib3
http = urllib3.PoolManager()

app = Bottle()

graph = TelegraphPoster()

print('hhhhhhhh')

@app.route('/create_api_token', method=['GET', 'POST'])
def create_api_token():
	try:
		kwargs = {i: None for i in ['short_name', 'author_name', 'author_url']}

		args_raw = request.params.decode().dict
		args = {i: args_raw[i][0] for i in args_raw}

		kwargs.update(args)
		kwargs = {i: kwargs[i] for i in ['short_name', 'author_name', 'author_url']}

		if kwargs['author_name'] == None:
			return {'ok': False, 'error': 'empty_fields', 'data': ['author_name'], 'explanation': 'these fields cant be empty'}
		if kwargs['short_name'] == None:
			return {'ok': False, 'error': 'empty_fields', 'data': ['short_name'], 'explanation': 'these fields cant be empty'}

		return {'ok': True, 'result': graph.create_api_token(**kwargs)}
	except Exception as e:
		return {'ok': False, 'error': 'unknown_error', 'data': e, 'explanation': 'unknown error, see data for more info'}


@app.route('/post', method=['GET', 'POST'])
def post():
	try:
		kwargs = {i: None for i in ['title', 'author', 'text']}

		args_raw = request.params.decode().dict
		args = {i: args_raw[i][0] for i in args_raw}

		if 'access_token' in args_raw:
			access_token = args_raw['access_token'][0]
		else:
			print('returned')
			return {'ok': False, 'error': 'empty_fields', 'data': ['access_token'], 'explanation': 'these fields cant be empty'}

		kwargs.update(args)
		kwargs = {i: kwargs[i] for i in ['title', 'author', 'text']}

		for i in ['title', 'author', 'text']:
			if kwargs[i] == None:
				return {'ok': False, 'error': 'empty_fields', 'data': [i], 'explanation': 'these fields cant be empty'}

		graph = TelegraphPoster(access_token)
		return {'ok': True, 'result': graph.post(**kwargs)}
	except Exception as e:
		return {'ok': False, 'error': 'unknown_error', 'data': e, 'explanation': 'unknown error, see data for more info'}

@app.route('/edit', method=['GET', 'POST'])
def edit():
	try:
		kwargs = {i: None for i in ['title', 'author', 'text']}

		args_raw = request.params.decode().dict
		args = {i: args_raw[i][0] for i in args_raw}

		if 'access_token' in args_raw:
			access_token = args_raw['access_token'][0]
		else:
			print('returned')
			return {'ok': False, 'error': 'empty_fields', 'data': ['access_token'], 'explanation': 'these fields cant be empty'}

		if 'path' in args_raw:
			path = args_raw['path'][0]
		else:
			print('returned')
			return {'ok': False, 'error': 'empty_fields', 'data': ['path'], 'explanation': 'these fields cant be empty'}

		kwargs.update(args)
		kwargs = {i: kwargs[i] for i in ['title', 'author', 'text']}

		for i in ['title', 'author', 'text']:
			if kwargs[i] == None:
				return {'ok': False, 'error': 'empty_fields', 'data': [i], 'explanation': 'these fields cant be empty'}
		
		res=upload(**kwargs, access_token=access_token, path=path)# tph_uuid=tph_uuid, page_id=page_id)
		return {'ok': True, 'result': res}
	except Exception as e:
		return {'ok': False, 'error': 'unknown_error', 'data': e, 'explanation': 'unknown error, see data for more info'}

app.run(host='0.0.0.0', port=8080)
