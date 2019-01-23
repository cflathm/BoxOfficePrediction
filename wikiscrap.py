from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
import time
import re
import pickle
import json

res = {}

class movie:
  directors = []
  producers = []
  writers = []
  starring = []
  editors = []
  production_company = []
  distribution_company = []
  release_date = ""
  run_time = ""
  budget = ""
  box_office = ""
  url = ""



def main():
  #x = 0
  urls = getUrls()
  #'''
  for url in urls:
    #x = x + 1
    #if x == 20:
    #  break
    try:
      scrapePage(url)
    except Exception as e:
      print(e)
    #time.sleep(.00005)
    print("Scraped: "+ url)
  #'''
  
  #scrapePage("https://en.wikipedia.org/wiki/Speed_Racer_(film)")
  #for x in res:
  #  print(x)
  #  print("**\n" + str(res[x].starring) + "\n***")
  return res


def getUrls():
  init = "https://en.wikipedia.org"
  clss = "wikitable sortable jquery-tablesorter"
  base = []
  for i in range(1980, 2018):
    url = "https://en.wikipedia.org/wiki/"+str(i)+"_in_film"
    base.append([url, i])

  
  urls = []
  for url in base:
    time.sleep(1)
    page = urlopen(url[0])

    soup = BeautifulSoup(page, 'html.parser')
    if url[1] < 2000:
      tables = soup.findAll('table',{'class',"wikitable"})[2:]
    else:
      tables = soup.findAll('table', {'class', "wikitable sortable"})
    for table in tables:
      for links in table.findAll('i'):
        for link in links.findAll('a'):
          urls.append(init + link['href'])
  return urls  

def scrapePage(url):
  film = movie()
  film.url = url

  page = urlopen(url)
  soup = BeautifulSoup(page, 'html.parser')
  table = soup.find('table', {'class', 'infobox vevent'})
  outRow = table.findAll('th')[0].text.replace(',','').replace(' ','_')
  rows = table.findAll('tr')
  num = "";
  date = "";
  for row in rows:
    #release_date
    if row.find('span') and 'Release date' in row.findAll('th')[0].text:
      date = row.findAll('span')[0].text.replace(' ','_').replace(',','_').replace('(','').replace(')','')[1:]
      film.release_date = date
      #outRow = outRow + ',' + date

    #box_office
    if row.find('th') and 'Box office' in row.findAll('th')[0].text:   
      num = row.findAll('td')[0].text #.split('[')[0].replace(',','')
      film.box_office = num
      '''
      multi = 1
      if 'million' in num:
        multi = 1000000
      elif 'billion' in num:
        multi = 1000000000
      elif 'thousand' in num:
        multi = 1000

      if '$' in num:
        num = num.split('$')[1]
      num = num.split(' ')[0].replace(')','')
      num = float(num) * multi
      #outRow = outRow + ',' + str(int(num))
      '''   

    #writers
    if row.find('th') and 'Screenplay by' in row.findAll('th')[0].text:
      if row.find('li'):
        film.writers = appendList(row)
      else:
        film.writers = [row.findAll('td')[0].text]

    
    #directors
    if row.find('th') and 'Directed by' in row.findAll('th')[0].text:
      if row.find('li'):
        film.directors = appendList(row)
      else:
        film.directors = [row.findAll('td')[0].text]
  
    
    #producers
    if row.find('th') and 'Produced by' in row.findAll('th')[0].text:
      if row.find('li'):
        film.producers = appendList(row)
      else:
        film.producers = [row.findAll('td')[0].text]


    
    #starring
    if row.find('th') and 'Starring' in row.findAll('th')[0].text:
      if row.find('li'):
        film.starring = appendList(row)
      else:
        film.starring = [row.findAll('td')[0].text]
    
    #editors
    if row.find('th') and 'Edited by' in row.findAll('th')[0].text:
      if row.find('li'):
        film.editors = appendList(row)
      else: 
        film.editors = [row.findAll('td')[0].text]

    #production_company
    if row.find('th') and 'Production' in row.findAll('th')[0].text:
      if row.find('li'):
        film.production_company = appendList(row)
      else:
        film.production_company = [row.findAll('td')[0].text]

    #distribution_company
    if row.find('th') and 'Distributed by' in row.findAll('th')[0].text:
      if row.find('li'):
        film.distribution_company = appendList(row)
      else:
        film.distribution_company = [row.findAll('td')[0].text]

    #run_time
    if row.find('th') and 'Running time' in row.findAll('th')[0].text: 
      film.run_time = row.findAll('td')[0].text

    #budget   
    if row.find('th') and 'Budget' in row.findAll('th')[0].text:
      film.budget = row.findAll('td')[0].text
 
  #movie check
  if date == "" or num == "" :
    print("not movie: " + url)
    return
  #print(film.production_company)
  res[url] = json.dumps(film.__dict__) 

def appendList(row):
  ret = []
  for item in row.findAll('li'):
    ret.append(item.text)
  return ret
  

if __name__ == "__main__":
  main()
