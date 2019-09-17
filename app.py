#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Goddy <wuchuansheng@yeah.net> 2019-09-17
# Desc: 

from flask_cors import CORS
from flask import Flask, request, make_response, jsonify, session, redirect
from service import SearchService
from model import Schema

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    q = request.args.get('q')
    return jsonify(search_service.autocomplete(q))


@app.route('/_search', methods=['GET'])
def search():
    q = request.args.get('q')
    return jsonify(search_service.search(q))


@app.route('/<string:keyword>', methods=['GET'])
def json_ld(keyword):
    result = search_service.get_one(keyword)
    if result is None:
        return '', 404
    return jsonify(result)


@app.route('/_class/zip', methods=['GET'])
def class_zip():
    return jsonify(schema.class_zip)


if __name__ == '__main__':
    schema = Schema(version='1.0')
    search_service = SearchService(schema)

    app.run(host='0.0.0.0', port=5000, debug=True)
