import requests
from bs4 import BeautifulSoup
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for

search_engines = {
  "Google": "https://www.google.com/search",
  "Bing": "https://www.bing.com/search",
  "Yahoo": "https://search.yahoo.com/search",
  "DuckDuckGo": "https://duckduckgo.com/html/",
  "Ask": "https://www.ask.com/web"
}


def get_search_results(query):
  results = []

  for search_engine, url in search_engines.items():
    params = {'q': query}

    headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    if search_engine == 'Google':
      results.extend([result['href']
                      for result in soup.select('.yuRUbf > a')][:5])
    elif search_engine == 'Bing':
      results.extend(
        [result['href'] for result in soup.select('.b_algo h2 > a')][:5])
    elif search_engine == 'Yahoo':
      results.extend([result['href']
                      for result in soup.select('.title > a')][:5])
    elif search_engine == 'DuckDuckGo':
      results.extend([
        result['href'] for result in soup.select('.result__url__domain > a')
      ][:5])
    elif search_engine == 'Ask':
      results.extend([
        result['href']
        for result in soup.select('.PartialSearchResults-item-title > a')
      ][:5])

  return results


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
  if request.method == "POST":
    query = request.form["query"]
    search_results = get_search_results(query)
    most_common_result = Counter(search_results).most_common(1)[0][0]
    return redirect(most_common_result)

  return render_template("index.html")


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=False)
