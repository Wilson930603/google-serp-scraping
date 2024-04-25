from serpapi import GoogleSearch
from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

SERP_API_KEY = "xxxxx"
DEFAULT_MAX_ARTICLE_RESULT = 100

def execute_search(keyword, from_date, to_date):
  start = 0
  results = list()
  is_default_search = not (is_valid_date(from_date) and is_valid_date(to_date))
  while True:
    params = {
      "q": keyword,
      "hl": "en",
      "gl": "ca",
      "google_domain": "google.com",
      "api_key": SERP_API_KEY,
      "start": start,
      "tbm":"nws"
    }
    search = GoogleSearch(params)
    google_results = search.get_dict()
    if 'news_results' in google_results:
      results = results + google_results['news_results']

    if len(results) >= DEFAULT_MAX_ARTICLE_RESULT and is_default_search:
      break

    if not 'serpapi_pagination' in google_results:
      break

    pagination = google_results['serpapi_pagination']

    if not 'next' in pagination:
      break

    start = get_start(pagination['next'])

  return filter_results(results, from_date, to_date)

def is_valid_date(text):
  format = "%Y-%m-%d"
  try:
    datetime.strptime(text, format)
    return True
  except ValueError:
    return False

def article_sorting_key(article):
  return article['Date_posted']

def get_time_article(time):
  is_ok = False
  time_formats = ['%b %d, %Y', '%d %b %Y']
  for time_format in time_formats:
    try:
      time_check = time
      time_check = time_check.replace('Sept', 'Sep')
      time_check = time_check.replace('July', 'Jul')
      time_check = time_check.replace('June', 'Jun')
      time_check = time_check.replace('Octo', 'Oct')
      time_check = time_check.replace('Apri', 'Apr')
      time_check = time_check.replace('Febr', 'Feb')
      time_check = time_check.replace('Janu', 'Jan')
      time_check = time_check.replace('Nove', 'Nov')
      Date_posted = datetime.strptime(time_check, time_format)
      Date_posted = Date_posted.strftime('%Y-%m-%d')
      is_ok = True
      break
    except:
      continue

  if not is_ok:
    Date_posted = time
  Date_posted = ago_do_date(Date_posted)
  if not is_validate_date(Date_posted):
    Date_posted = datetime.today().strftime('%Y-%m-%d')

  return Date_posted

def is_validate_date(date_text):
  try:
      datetime.strptime(date_text, '%Y-%m-%d')
      return True
  except ValueError:
      return False

def ago_do_date(time_str):
  try:
    if 'ago' not in time_str:
      return time_str

    value, unit = re.search(r'(\d+) (\w+) ago', time_str).groups()
    if not unit.endswith('s'): unit += 's'

    delta = relativedelta(**{unit: int(value)})

    return (datetime.now() - delta).strftime('%Y-%m-%d')
  except:
    return time_str

def filter_results(data, from_date, to_date):
  all_articles = list()

  print(data)
  for article in data:
    item = dict()
    item['Headline'] = article['title']
    item['Source'] = article['source']
    item['desc'] = article['snippet'] if 'snippet' in article else ''
    item['link'] = article['link']

    time_article = article['date'] if 'date' in article else ''
    item['Date_posted'] = get_time_article(time_article)
    # item['time'] = item['Date_posted']
    all_articles.append(item)

  all_articles.sort(reverse=True, key=article_sorting_key)

  if is_valid_date(from_date) and is_valid_date(to_date):
    filtered_articles = list(filter(lambda article: article['Date_posted'] >= from_date and article['Date_posted'] <= to_date, all_articles))
  else:
    if is_valid_date(from_date) or is_valid_date(to_date):
      if not is_valid_date(to_date):
        filtered_articles = list(filter(lambda article: article['Date_posted'] >= from_date, all_articles))
      else:
        filtered_articles = list(filter(lambda article: article['Date_posted'] <= to_date, all_articles))
    else:
      # most recent 100 news
      filtered_articles = all_articles[:100]

  return filtered_articles

def get_start(url):
  parsed_url = urlparse(url)
  captured_value = parse_qs(parsed_url.query)['start'][0]
  return captured_value

def main(keyword='crimedoor', from_date=None, to_date=None):
  results = execute_search(keyword, from_date, to_date)
  # print(results['organic_results'])
  print('Google search found: ', len(results))
  return results

"""
Test Function
"""
import csv

def save_dict_list_to_csv(dict_list, filename):
    fieldnames = dict_list[0].keys() if dict_list else []
    
    with open(filename, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_list)
if __name__ == "__main__":
  results = main("Data", '2023-07-04', '2023-07-04')
  if len(results)>0:
    save_dict_list_to_csv(results,'google_search_results.csv')
  print(results)
