# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
def main():
  first = True
  urls = getUrls()
  csv_file = open('BoxOffice.csv', 'w+')
  for url in urls:
    scrapePage(url, first, csv_file)
    time.sleep(30)
    first = False
  


def getUrls():
  url = "https://www.boxofficemojo.com/genres/"

  page = urlopen(url)

  soup = BeautifulSoup(page, 'html.parser')
  rows = soup.findAll('table')[-1].findAll('tr')
  urls = []
  for row in rows[1:]:
    href = row.findAll('a')[0]['href']
    url = 'https://www.boxofficemojo.com/genres' + href[1:]
    urls.append(url)
    #print(url)
  return urls


def scrapePage(url, first, csv_file):
  try:
    page = urlopen(url)
  except Exception as e:
    print(url)
    print(e)
    if '503' in str(e):
      #time.sleep(10)
      scrapePage(url, first, csv_file)
    return

  print("Scraping: " + url.split('=')[-1])

  soup = BeautifulSoup(page, 'html.parser')

  cat = soup.find('h1').text


  rows = soup.findAll('table')[-2].findAll('tr')
  if first is True:
    printHead(rows[0], csv_file)


  for row in rows[1:-1]:
    itms = row.findAll('td')
    texts = []
    for itm in itms:
      texts.append(itm.text.replace(" ", "_").replace("\'","").replace("\"","").replace(":","").replace(",",""))
    texts.append(cat.replace(" ","_"))
    csv_file.write(",".join(texts))
    csv_file.write("\n")


def printHead(row, csv_file):
  itms = row.findAll('td')
  texts = []
  for itm in itms:
    texts.append(itm.text.replace(" ", "_").replace("\'","").replace("\"","").replace(":","").replace("/",","))
  texts.append("genre")
  csv_file.write(",".join(texts))
  csv_file.write("\n")


if __name__ == "__main__":
  main()


