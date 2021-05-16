from nsepython import *
import datetime, os, time, sys

# Mention near expiry date. Fetch next 4 weekly expiry dates 
this_expiry =  '20-May-2021'
this_expiry_obj = datetime.datetime.strptime(this_expiry, '%d-%b-%Y')
expiry_dates = [ (this_expiry_obj + datetime.timedelta(i)).strftime("%d-%b-%Y") for i in [0,7,14,21,28] ]

# Variables
now = datetime.datetime.now()
now_date = now.strftime("%d-%b-%Y")
now_time = now.strftime("%H%M")
out_file = os.path.join('/Users/mandar.shinde/personal/nse', 'nse_data-' + now_date + '.csv')

# CSV header
header = "Date,Time,Type,strikePrice, expiryDate, underlying, identifier, openInterest, changeinOpenInterest, pchangeinOpenInterest, totalTradedVolume, impliedVolatility, lastPrice, change, pChange, totalBuyQuantity, totalSellQuantity, bidQty, bidprice, askQty, askPrice, underlyingValue\n"

# Create a file if it doesn't exist. Dump the header if a new file is created
if not os.path.exists(out_file):
    fo = open(out_file, 'w')
    fo.write(header)
    fo.close()
#    print(header)

# If file exists, open it in append mode 
fo = open(out_file, 'a')

# Function to scrape the data, returns raw and filtered data
def scrape(symbol):
    a = nse_optionchain_scrapper(symbol)
    return (a['records']['data'], a)

# Get ATM strike price as per current index value
def get_atm_strike(payload):
    ltp = float(payload['records']['underlyingValue'])
    strike_price_list = [x['strikePrice'] for x in payload['records']['data']]
    atm_strike = sorted([[round(abs(ltp-i),2),i] for i in strike_price_list])[0][1]
    return atm_strike

# Skip scraping if the time doesn't fall in market time window
if not (int(now_time) >= 915 and int(now_time) <= 1530):
    print("Market is closed at the moment, data will not be scraped!")
    sys.exit()

# If market is open, start scraping 
scraped_data,raw_data = scrape('NIFTY')
atm_strike = get_atm_strike(raw_data)

# Each line in the scraped data represents a strikePrice-expiryDate combination
for i in scraped_data:
    # We are interested in the next 4 expiry dates, ignore others
    if i['expiryDate'] not in expiry_dates:
        continue

    # Ignore strike prices that are far away from ATM strike price
    if abs(i['strikePrice'] - atm_strike) > 1000:
        continue

    # Text manipulation to prepare CSV data
    ce_prefix = now_date + "," + now_time + ',CE,'
    pe_prefix = now_date + "," + now_time + ',PE,'
    ce_details = list( map( str, i['CE'].values() ) )
    pe_details = list( map( str, i['PE'].values() ) )

    # Write the data to the file and print it on console
    fo.write(ce_prefix + ",".join(ce_details) + "\n")
    fo.write(pe_prefix + ",".join(pe_details) + "\n")
    print(ce_prefix + ",".join(ce_details))
    print(pe_prefix + ",".join(pe_details))

fo.close()
