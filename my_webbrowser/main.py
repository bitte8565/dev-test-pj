# Google検索する

import urllib.parse
import webbrowser

url = "https://www.google.com/search"

params = urllib.parse.urlencode({"query": "テスト"})
search_url = f'{url}?{params}'
print(search_url)
webbrowser.open(search_url)
