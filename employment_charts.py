# source: https://fred.stlouisfed.org
# stacked line chart of employment ratio, unemployment rate and labor force participation rate

# environment set-up

import pandas as pd
import matplotlib.pyplot as plt
import requests

key = input('enter your FRED API key here: ')
endpoint = r'https://api.stlouisfed.org/fred/series/observations'

# data cleaning function
def process_api(api_pull):
    raw_data = api_pull.json()
    df = pd.DataFrame(raw_data['observations'])
    df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = df['value'].astype(float)

    return df

# API pulls
em_payload = {
    'api_key': key,
    'file_type': 'json',
    'series_id':  'EMRATIO'
}
em_content = requests.get(url=endpoint, params=em_payload)

un_payload = {
    'api_key': key,
    'file_type': 'json',
    'series_id':  'UNRATE'
}
un_content = requests.get(url=endpoint, params=un_payload)

civ_payload = {
    'api_key': key,
    'file_type': 'json',
    'series_id':  'CIVPART'
}
civ_content = requests.get(url=endpoint, params=civ_payload)

# process raw data
em_df = process_api(em_content)
un_df = process_api(un_content)
civ_df = process_api(civ_content)

#calculate most recent values for each cateogry
un_date = un_df.iloc[-1,0]
un_label = un_df.iloc[-1,-1]

civ_date = civ_df.iloc[-1,0]
civ_label = civ_df.iloc[-1,-1]

em_date = em_df.iloc[-1,0]
em_label = em_df.iloc[-1,-1]

# chart data on stacked line charts
fig, ax = plt.subplots(3,1, figsize=(12,8))

ax[0].plot(em_df['date'], em_df['value'], color='green')
ax[0].set_ylabel('Ratio \n(%)')
ax[0].set_title('Employment-Population Ratio')

ax[1].plot(un_df['date'], un_df['value'], color='green')
ax[1].set_ylabel('Unemployment \n(%)')
ax[1].set_title('Unemployment Rate')

ax[2].plot(civ_df['date'], civ_df['value'], color='green')
ax[2].set_ylabel('Participation \n(%)')
ax[2].set_title('Labor Force Participation')
fig.tight_layout()

ax[0].text(em_date, em_label, ' {}%'.format(em_label))
ax[1].text(un_date, un_label, ' {}%'.format(un_label))
ax[2].text(civ_date, civ_label, ' {}%'.format(civ_label))

ax[0].axhline(em_label, color='gray', linestyle=':')
ax[1].axhline(un_label, color='gray', linestyle=':')
ax[2].axhline(civ_label, color='gray', linestyle=':')

plt.savefig('employment_charts.png', pad_inches=0.75, bbox_inches='tight', orientation='portrait')

