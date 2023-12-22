from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
index_name = "titleindex1"
app = Flask(__name__)
es = Elasticsearch(['http://localhost:9200'])

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('search.html')

@app.route('/multi', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query == '':
        return render_template('search.html')

    page = request.args.get('page', 1, type=int)
    results_per_page = 10
    start = (page - 1) * results_per_page

    response = es.search(
        index=index_name,
        body={
            "from": start, "size": results_per_page,
            "query": {
                # "multi_match": {
                #     "query": query,
                #     "fields": ["title"],
                # }
                "match":{
                    "title": query,
                }
            }
        }
    )

    results = response['hits']['hits']
    total_results = response['hits']['total']
    total_pages = (total_results + results_per_page - 1) // results_per_page

    return render_template('results.html', results=results, total_pages=total_pages, current_page=page, query=query)


@app.route('/reg', methods=['GET'])
def search_reg():
    query = request.args.get('query', '')
    if query == '':
        return render_template('search.html')

    page = request.args.get('page', 1, type=int)
    results_per_page = 10
    start = (page - 1) * results_per_page

    response = es.search(
        index=index_name,
        body={
            "from": start, "size": results_per_page,
            "query": {
                "regexp":{
                    "title": query,
                }
            }
        }
    )

    results = response['hits']['hits']
    total_results = response['hits']['total']
    total_pages = (total_results + results_per_page - 1) // results_per_page

    return render_template('results.html', results=results, total_pages=total_pages, current_page=page, query=query)


@app.route('/fuzzy', methods=['GET'])
def search_fuzzy():
    query = request.args.get('query', '')
    if query == '':
        return render_template('search.html')

    page = request.args.get('page', 1, type=int)
    results_per_page = 10
    start = (page - 1) * results_per_page

    response = es.search(
        index=index_name,
        body={
            "from": start, "size": results_per_page,
            "query": {
                "fuzzy":{
                    "title":{
                        "value": query,
                    }
                }
            }
        }
    )

    results = response['hits']['hits']
    total_results = response['hits']['total']
    total_pages = (total_results + results_per_page - 1) // results_per_page

    return render_template('results.html', results=results, total_pages=total_pages, current_page=page, query=query)

@app.route('/showall', methods=['GET'])
def showall():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    results_per_page = 10
    start = (page - 1) * results_per_page

    response = es.search(
        index=index_name,
        body={
            "from": start, "size": results_per_page,
            "query": {
                "match_all": {},
            }
        }
    )

    results = response['hits']['hits']
    total_results = response['hits']['total']
    total_pages = (total_results + results_per_page - 1) // results_per_page

    return render_template('results_showall.html', results=results, total_pages=total_pages, current_page=page, query=query)

if __name__ == '__main__':
    app.run(debug=True)
