import pandas as pd
import bs4 as bs
import requests

#website's base url
base_url = "https://www.goldpriceindia.com/"

#months list
months = ['january','february','march','april','may','june','july','august',
          'september','october','november','december']

#years list
years = [2017,2018,2019,2020]


def Query(month,year):
    """
    args : month name and year
    output : query to search gold price
    """
    return "gold-price-"+month+'-'+str(year)+'.php'

#dataframe to store gold prices
gold_prices = pd.DataFrame()

for year in years:
    for month in months:
      #requesting web page 
      page = requests.get(base_url + Query(month,year))

      #convert the responce into BeautifulSoup object
      soup = bs.BeautifulSoup(page.content)

      #tabels that contains gold prices
      tabels = soup.findAll("table",class_="table-data dayyeartable")

      #scrap days
      date_headings = soup.findAll("h4")
      dates = []
      for date in date_headings:
        dates.append(str(date.string)[14:])
      dates.reverse()

      #scraping gold price for each day from the tabels
      prices = []
      for table in tabels:
        price = str(table.find_all("td",class_="align-center")[0].string)
        if len(str(price)) <= 6:
          prices.append(price)
      prices.reverse()

      #store scraped data in to pandas DataFrame
      df = pd.DataFrame({"date":dates,"price":prices})

      #append df to main DataFrame gold_prices
      gold_prices = pd.concat([gold_prices,df],axis=0)

#saving gold prices
gold_prices.to_csv("gold_prices.csv",index = False)
