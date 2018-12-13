from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import re
def main():
  urls = getUrls()
  csv_file = open('BoxOffice.csv', 'w+')
  csv_file.write("Title, Release Date, Box Office\n")
  for url in urls:
    try:
      scrapePage(url, csv_file)
    except Exception as e:
      print(e)
    time.sleep(.0005)
    print("Scraped: "+ url)
  #scrapePage("https://en.wikipedia.org/wiki/Internal_Affairs_(film)",csv_file)


def getUrls():
  init = "https://en.wikipedia.org"
  clss = "wikitable sortable jquery-tablesorter"
  base = []
  for i in range(1990, 2018):
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

def scrapePage(url, csv_file):
  page = urlopen(url)
  soup = BeautifulSoup(page, 'html.parser')
  table = soup.find('table', {'class', 'infobox vevent'})
  outRow = table.findAll('th')[0].text.replace(',','').replace(' ','_')
  rows = table.findAll('tr')
  num = "";
  date = "";
  for row in rows:
    if row.find('span') and 'Release date' in row.findAll('th')[0].text:
      date = row.findAll('span')[0].text.replace(' ','_').replace(',','_').replace('(','').replace(')','')[1:]
      outRow = outRow + ',' + date
    if row.find('th') and 'Box office' in row.findAll('th')[0].text:
    
      num = row.findAll('td')[0].text.split('[')[0].replace(',','')


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
      outRow = outRow + ',' + str(int(num))
    
  if date == "" or num == "" or int(num) < 100:
    print("not movie: " + url)
    return
  csv_file.write(outRow+'\n')

if __name__ == "__main__":
  main()
