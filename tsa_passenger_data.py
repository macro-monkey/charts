### Creates a chart comparing 2019 and 2020 TSA Passenger trends
### data: https://www.tsa.gov/coronavirus/passenger-throughput

# set up environment

import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen

URL = 'https://www.tsa.gov/coronavirus/passenger-throughput'
req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
web_page = urlopen(req).read()

df = pd.read_html(web_page, header=0)[0]

df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

new_cols = {'Date':'date',
            'Total Traveler Throughput': 'pax_20',
            'Total Traveler Throughput  (1 Year Ago - Same Weekday)': 'pax_19'
            }

df.rename(columns=new_cols, inplace=True)

tsa = df.copy()

# data to dataframe and sorted by date, data to millions
# tsa = pd.read_csv('tsa_pass_data_7_1.csv', parse_dates=['date'], thousands=',')

tsa['pax_20_m'] = tsa['pax_20'] / 1000000
tsa['pax_19_m'] = tsa['pax_19'] / 1000000

tsa.sort_values(by='date', inplace=True)
tsa = tsa.reset_index(drop=True)

avg_2019 = tsa['pax_19_m'].mean()

# chart data on line chart

fig, ax = plt.subplots()
ax.plot(tsa['date'],tsa['pax_20_m'], linewidth=0.75, label='2020', color='red')
ax.plot(tsa['date'], tsa['pax_19_m'], linewidth=0.75, label='2019', color='green')
ax.axhline(avg_2019, linewidth=0.5, color='gray')
ax.set_ylabel('Daily Passenger Traffic (m)')
ax.set_title('TSA Passenger Traffic (2019 vs. 2020)')
ax.legend()
ax.plot()
fig.autofmt_xdate()
plt.savefig('TSA_data.png')
plt.show()


