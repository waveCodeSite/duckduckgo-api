from itertools import islice

from duckduckgo_search import DDGS
from flask import Flask, request, jsonify
import config

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json;charset=UTF-8'
app.config.from_object(config)

VALID_TOKEN = app.config['AUTH_TOKEN']


def authenticate():
    return jsonify({'error': 'Invalid token'}), 403


def run():
    if request.method == 'POST':
        keywords = request.form['q']
        max_results = int(request.form.get('max_results', 10))
    else:
        keywords = request.args.get('q')
        # 从请求参数中获取最大结果数，如果未指定，则默认为10
        max_results = int(request.args.get('max_results', 10))
    return keywords, max_results


@app.route('/search', methods=['GET', 'POST'])
async def search():
    auth = request.headers.get('token')
    if auth != VALID_TOKEN:
        return authenticate()
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.text(keywords, safesearch='Off', timelimit='y', backend="lite")
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'data': results}


@app.route('/searchAnswers', methods=['GET', 'POST'])
async def search_answers():
    auth = request.headers.get('token')
    if auth != VALID_TOKEN:
        return authenticate()
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.answers(keywords)
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'data': results}


@app.route('/searchImages', methods=['GET', 'POST'])
async def search_images():
    auth = request.headers.get('token')
    if auth != VALID_TOKEN:
        return authenticate()
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.images(keywords, safesearch='Off', timelimit=None)
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'data': results}


@app.route('/searchVideos', methods=['GET', 'POST'])
async def search_videos():
    auth = request.headers.get('token')
    if auth != VALID_TOKEN:
        return authenticate()
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.videos(keywords, safesearch='Off', timelimit=None, resolution="high")
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'data': results}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
