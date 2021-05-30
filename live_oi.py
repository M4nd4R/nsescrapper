from nsepython import *
from termcolor import colored, cprint
#print(indices)

a = nse_optionchain_scrapper('NIFTY')
date = '03-Jun-2021'
b = [ i for i in a['records']['data'] if i['expiryDate'] == date ]
total_ce = 0
total_pe = 0
pcr_ce = 0
pcr_pe = 0

def get_atm_strike():
    payload = a
    ltp = float(payload['records']['underlyingValue'])
    strike_price_list = [x['strikePrice'] for x in payload['records']['data']]
    atm_strike = sorted([[round(abs(ltp-i),2),i] for i in strike_price_list])[0][1]
    return atm_strike

print_white_on_yellow = lambda x: cprint(x, 'white', 'on_yellow', attrs=['bold'])
print_white_on_red = lambda x: cprint(x, 'white', 'on_red', attrs=['bold'])
print_white_on_green = lambda x: cprint(x, 'white', 'on_green', attrs=['bold'])

atm_strike = get_atm_strike()

print("=" * 100)
print("{0:^12} {1:^12} {2:^12} {3:^9} {4:^13} {5:^9} {6:^12} {7:^12}".format('ExpiryDate', 'CE-OI', 'ChangeInOI', 'CE-LTP', 'StrikePrice', 'PE-LTP', 'PE-OI', 'ChangeInOI'))
print("_" * 100)

for i in b:
	if abs(i['strikePrice'] - atm_strike) > 700:
		continue
	total_ce += i['CE']['changeinOpenInterest']*75
	total_pe += i['PE']['changeinOpenInterest']*75
	pcr_ce += i['CE']['openInterest']
	pcr_pe += i['PE']['openInterest']

	if i['strikePrice'] == atm_strike:
		print_white_on_yellow("{0:^12} {1:^12} {2:^12} {3:^9} {4:^13} {5:^9} {6:^12} {7:^12}".format(i['expiryDate'], i['CE']['openInterest']*75, i['CE']['changeinOpenInterest']*75, i['CE']['lastPrice'], i['strikePrice'], i['PE']['lastPrice'], i['PE']['openInterest']*75, i['PE']['changeinOpenInterest']*75))
		continue
	print("{0:^12} {1:^12} {2:^12} {3:^9} {4:^13} {5:^9} {6:^12} {7:^12}".format(i['expiryDate'], i['CE']['openInterest']*75, i['CE']['changeinOpenInterest']*75,i['CE']['lastPrice'], i['strikePrice'], i['PE']['lastPrice'], i['PE']['openInterest']*75, i['PE']['changeinOpenInterest']*75))

print("=" * 100)
print("Total CE OI = " + str(total_ce) +" | Total PE OI = " + str(total_pe) + " | Diff = " + str(total_ce - total_pe))

print("Trend (based on OI change): ")
if total_ce > total_pe:
	print_white_on_red("Bearish")
elif total_ce < total_pe:
	print_white_on_green("Bullish")
else:
	print("Trend: Sideways")

pcr_ratio = round(pcr_pe/pcr_ce,2)
print( "Total CE OI: {}  |  Total PE OI: {}  |  PCR Ratio: {}".format(pcr_ce*75, pcr_pe*75, pcr_ratio) )
