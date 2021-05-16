from nsepython import *
from termcolor import colored, cprint
import datetime, os, time

this_expiry =  '20-May-2021'
this_expiry_obj = datetime.datetime.strptime(this_expiry, '%d-%b-%Y')
expiry_dates = [ (this_expiry_obj + datetime.timedelta(i)).strftime("%d-%b-%Y") for i in [0,7,14,21,28] ]

now = datetime.datetime.now()
now_date = now.strftime("%d-%b-%Y")
now_time = now.strftime("%H%M")
out_file = os.path.join('/Users/mandar.shinde/personal/nse', 'nse_data-' + now_date + '.csv')

header = "Date,Time,Type,strikePrice, expiryDate, underlying, identifier, openInterest, changeinOpenInterest, pchangeinOpenInterest, totalTradedVolume, impliedVolatility, lastPrice, change, pChange, totalBuyQuantity, totalSellQuantity, bidQty, bidprice, askQty, askPrice, underlyingValue\n"

if not os.path.exists(out_file):
    fo = open(out_file, 'a')
    fo.write(header)
    fo.close()

fo = open(out_file, 'a')

def scrape(symbol):
    a = nse_optionchain_scrapper(symbol)
    return (a['records']['data'], a)

def get_atm_strike(payload):
    ltp = float(payload['records']['underlyingValue'])
    strike_price_list = [x['strikePrice'] for x in payload['records']['data']]
    atm_strike = sorted([[round(abs(ltp-i),2),i] for i in strike_price_list])[0][1]
    return atm_strike

if not (int(now_time) >= 915 and int(now_time) <= 1530):
    print("Market is closed at the moment, data will not be scraped!")

scraped_data,raw_data = scrape('NIFTY')
atm_strike = get_atm_strike(raw_data)

print(header)

for i in scraped_data:
    if i['expiryDate'] not in expiry_dates:
        continue
    if abs(i['strikePrice'] - atm_strike) > 1000:
        continue
    ce_prefix = now_date + "," + now_time + ',CE,'
    pe_prefix = now_date + "," + now_time + ',PE,'
    ce_details = list( map( str, i['CE'].values() ) )
    pe_details = list( map( str, i['PE'].values() ) )
    fo.write(ce_prefix + ",".join(ce_details) + "\n")
    fo.write(pe_prefix + ",".join(pe_details) + "\n")
    print(ce_prefix + ",".join(ce_details))
    print(pe_prefix + ",".join(pe_details))

fo.close()
