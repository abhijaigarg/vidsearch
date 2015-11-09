#!flask/bin/python
from flask import Flask,jsonify
from flask import request, render_template
# from flask.ext.jsonpify import jsonify

app = Flask(__name__)

import json

from collections import defaultdict

from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.index import open_dir

import os

indexName = 'tempInd'

def search(term, limit=3):
  ix = open_dir(indexName)
  searcher = ix.searcher()

  parsed_query = QueryParser("data",ix.schema).parse(term)

  if limit >= 0:
    print "with limit"
    return searcher.search(parsed_query, limit = int(limit))
  else:
    print "without limit"
    return searcher.search(parsed_query)


def make_json(results):
	json_results = []
	for i in range(results.scored_length()):
		try:
			# print results[i]['frame_time']
			result = {'frame_time': results[i]['frame_time'],'frame_path': results[i]['frame_path']}
			json_results.append(result)

		except:
			pass

	return json_results


@app.route('/video/api/v1.0/search')
def get_results():
	query = request.args.get('q')
	limit = request.args.get('limit')

	if limit == None:
		results = search(query)
	else:
		results = search(query, limit)

	final_results = make_json(results)
	final = {
		'results': final_results
	}
	return jsonify(final)

if __name__ == '__main__':
	app.run(debug=True)


