import pandas as pd 
import re

whole_df = pd.read_csv('worlds all cities with their avg temp.csv')

# dataframe seems to contant both C and F. F being after new line and with () around it

print(whole_df.head())

# dropping the pointsless ref
whole_df = whole_df.drop('Ref.', axis=1)

# to clean the dataframe will start with creating a new dataframe of just months, cleanind them then adding them over

months = whole_df.drop(['Country', 'City'], axis=1)

print(months.head())

# to apply regex to the months to select only useful temps
def extract_first_float(text):
    match = re.search(r'\d+\.\d+', text)  # Match the float pattern that will be the celcius 
    if match:
        return float(match.group())  # Convert the matched string to float
    return None

for column_name in months.columns:
    months[column_name] = months[column_name].apply(extract_first_float)

# data is now just the celcius
print(months.head())

for column_name in months.columns:
    whole_df[column_name] = months[column_name]

# cleanr full data sheet
print(whole_df.head())

# corrent data types
print(whole_df.info())

# every month has a lot of missing data
print(whole_df.isna().sum())

print(whole_df[whole_df.isna()==True])

months_list = months.columns.tolist()
# dropping from the table when all the data is missing
whole_df.dropna(subset=months_list, inplace=True, how='all')

print(whole_df.isna().sum())

print(whole_df.info())

#chosen to forward fill na to not loose the whole months and as there was a good mixture over the year of where data is missing forward filling would average out between increase at start of year then end of year
whole_df.fillna(inplace=True, method='ffill')

print(whole_df.isna().sum())