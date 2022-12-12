import re
import unicodedata
import requests
from bs4 import BeautifulSoup

def get_lyrics(key, url=None):
  if not url:
    url = f"https://www.google.com/search?q={key}+lyrics&ie=UTF-8"
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
  source = requests.get(url, headers=headers)

  soup = BeautifulSoup(source.text, "html.parser")

  lyricsRef = soup.find("div", {"class":"hwc"})
  titleRef = soup.find("div", {"class":"kCrYT"})
  correct = soup.find("div", {"class": "v0nnCb"})

  if correct:
    url = f"https://www.google.com{correct.a['href']}"
    return get_lyrics(key, url)

  if lyricsRef is None or titleRef is None:
    return None
  else:
    return lyricsRef.text
    

def parse_search_term(search_term):
  
  try:
      text = unicode(search_term, 'utf-8')
  except NameError:
    pass

  text = unicodedata.normalize('NFD', search_term)\
         .encode('ascii', 'ignore')\
         .decode("utf-8")

  return str(text)

def word_capture_or_literal(w):
   return '(?:\s+\S+)' if w == "_" else " *" + w    

def main(search_term):
  search_term_parsed = search_term.replace(',', ' ').replace('.', ' ').lstrip().lower()
  search_term_parsed = parse_search_term(search_term_parsed).split()
  search_result = get_lyrics(search_term.replace('_', ''))

  search_term_list = search_term_parsed
  for i in range(len(search_term_list)):
    if "_" in search_term_list[i]:
      search_term_list[i] = "_"

  lyrics = search_result.replace('\n', ' ').lower().replace('.', '').replace(',', '').replace('  ', ' ')
  lyrics = parse_search_term(lyrics)

  pattern = "".join(map(word_capture_or_literal, search_term_list))
  result = re.search(pattern, lyrics)
  result = result.group(0).strip()

  for i in range(len(search_term_list)):
    if "_" in search_term_list[i]:
      missing_index = i

  return result.split()[missing_index]
