import os
import urllib.request
import pandas as pd
import datetime as dt


def fetch_and_process_usgs_data(station_number, start_date, end_date):
    """
    Fetches USGS data for a specific station within a given date range, processes the data,
    and returns a pandas DataFrame containing the processed data.

    Parameters:
    - station_number (str): The USGS Station ID.
    - start_date (str): The start date in the format 'YYYY-M-D'.
    - end_date (str): The end date in the format 'YYYY-M-D'.

    Returns:
    pandas.DataFrame: A DataFrame containing the processed USGS data with columns: 'Date' and 'Discharge'.
    """

    folder = os.getcwd()

    section1 = 'https://nwis.waterdata.usgs.gov/nwis/dv?referred_module=sw&search_site_no='
    section2 = '&search_site_no_match_type=exact&site_tp_cd=OC&site_tp_cd=OC-CO&site_tp_cd=ES&site_tp_cd=' \
               'LK&site_tp_cd=ST&site_tp_cd=ST-CA&site_tp_cd=ST-DCH&site_tp_cd=ST-TS&index_pmcode_00060=1&group_key=' \
               'NONE&sitefile_output_format=html_table&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=date_range&begin_date='
    section3 = '&end_date='
    section4 = '&format=rdb&date_format=YYYY-MM-DD&rdb_compression=value&list_of_search_criteria=search_site_no%2Csite_tp_cd%2Crealtime_parameter_selection'

    link = (section1 + station_number + section2 + start_date + section3 + end_date + section4)
    print("Click here to see the generated USGS link: \n", link)

    USGS_page = urllib.request.urlopen(link)
    downloaded_data = USGS_page.read()
    str_data = downloaded_data.decode()
    f_str_data = str_data.split('\n')
    station_name = ''

    for line in range(len(f_str_data)):
        if f_str_data[line].startswith("#    USGS"):
            station_name = f_str_data[line][3:]

    date_flow = ''

    for line in range(len(f_str_data)):
        if f_str_data[line].startswith("USGS"):
            data = f_str_data[line][14:]
            columns = data.split('\t')
            rows = ','.join([columns[0], columns[1]])
            date_flow += rows + '\n'

    date_flow = date_flow.encode()

    with open(folder + '/USGS_Data_for_' + station_number + '.txt', 'wb') as text:
        text.write(date_flow)

    filename = folder + '/USGS_Data_for_' + station_number + '.txt'
    columns = ['Date', 'Discharge (cfs)']
    df = pd.read_csv(filename, header=None, names=columns, parse_dates=[0])
    # df.set_index('Date', inplace=True)
    # df = df.set_index(['Date'])
    df['Discharge (cfs)'] = pd.to_numeric(df['Discharge (cfs)'], errors='coerce')
    df.rename(columns={'Discharge (cfs)': 'Discharge'}, inplace=True)

    return df


def clean_ffill(df):
    """
      Fill NaN values in the 'Discharge' column of a DataFrame using forward fill.

      This function takes a DataFrame containing a datetime 'Date' column and a 'Discharge' column
      with potential NaN values. It performs forward fill on the 'Discharge' column, replacing NaN
      values with the most recent non-NaN value. The function returns the updated DataFrame.

      Parameters:
      df (pandas.DataFrame): Input DataFrame with 'Date' and 'Discharge' columns.

      Returns:
      pandas.DataFrame: DataFrame with NaN values in the 'Discharge' column filled using forward fill.
    """

    df['Discharge'] = df['Discharge'].ffill()
    return df


def separate_date_parameters(df):
    """
      Separates the 'Date' column of a DataFrame into year, month, week, and day columns.

      This function takes a DataFrame containing a datetime 'Date' column and returns a DataFrame
      with the 'Date' column split into 'Year', 'Month', 'Week', and 'Day' columns.

      Parameters:
      df (pandas.DataFrame): Input DataFrame with 'Date' column.

      Returns:
      pandas.DataFrame: DataFrame with 'Date' column split into 'Year', 'Month', 'Week', and 'Day' columns.
    """

    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    # df['Week'] = df['Date'].dt.week
    df['Day'] = df['Date'].dt.day

    return df


def quantiles(df, period, quantile):
    # periods = ['Year', 'Month', 'Week', 'Day']

    # Group the DataFrame by the period column and calculate the 90th quantile for each group
    quantiles = df.groupby(f'{period}')['Discharge'].quantile(quantile)

    # Merge the quantiles back into the original DataFrame
    df = df.merge(quantiles.reset_index(name=f'{period} Quantile {quantile}'), on=f'{period}', how='left')

    return df


def label_rows(df, prediction_columns, threshold):
    # Calculate the absolute differences between the specified prediction columns
    df['Absolute_Difference'] = df[prediction_columns].apply(lambda row: abs(row[0] - row[1]), axis=1)

    # Create a new column 'Label' based on the threshold
    df['Label'] = df['Absolute_Difference'].apply(lambda x: 'BFO' if x <= threshold else 'NBF')

    # Drop the 'Absolute_Difference' column if you don't need it
    df.drop('Absolute_Difference', axis=1, inplace=True)

    # Save the DataFrame to a CSV file
    df.to_csv('labled_data.csv', index=False)

    return df


def create_quantiles_dataframe(dates, streamflow_list, percentile):

    date_df = pd.DataFrame({'Date': dates})
    date_df['Day'] = date_df.loc[:,'Date'].dt.dayofyear
    date_df['Week'] = date_df.loc[:,'Date'].dt.isocalendar().week
    date_df['Month'] = date_df.loc[:,'Date'].dt.month
    date_df['Season'] = 1
    for i in date_df.index:
        day = date_df.at[i, 'Day']
        if 80 <= day < 172:  # March 20 to June 19
            date_df.at[i, 'Season'] = 2
        elif 172 <= day < 266:  # June 20 to September 21
            date_df.at[i, 'Season'] = 3
        elif 266 <= day < 356:  # September 22 to December 20
            date_df.at[i, 'Season'] = 4
    date_df['Year'] = date_df.loc[:,'Date'].dt.year
    date_df['Streamflow (cfs)'] = df['Streamflow (cfs)']


    thresholds_df = pd.DataFrame()
    thresholds_df['Date'] = dates

    thresholds_df['Daily Streamflow'] = df['Streamflow (cfs)']
    thresholds_df['Weekly Streamflow'] = df.groupby([df['Date'].dt.year, df['Date'].dt.isocalendar().week])['Streamflow (cfs)'].mean().loc[list(zip(date_df['Year'], date_df['Week']))].values
    thresholds_df['Monthly Streamflow'] = df.groupby([df['Date'].dt.year, df['Date'].dt.month])['Streamflow (cfs)'].mean().loc[list(zip(date_df['Year'], date_df['Month']))].values
    thresholds_df['Seasonal Streamflow'] = df.groupby([date_df['Year'], date_df['Season']])['Streamflow (cfs)'].mean().loc[list(zip(date_df['Year'], date_df['Season']))].values
    thresholds_df['Yearly Streamflow'] = df.groupby(df['Date'].dt.year)['Streamflow (cfs)'].mean().loc[date_df['Year']].values

    total_daily_quantiles = date_df.groupby(['Day'])['Streamflow (cfs)'].quantile(percentile)
    thresholds_df['Daily Threshold'] = date_df['Day'].map(total_daily_quantiles)
    total_weekly_quantiles = date_df.groupby(['Week'])['Streamflow (cfs)'].quantile(percentile)
    thresholds_df['Weekly Threshold'] = date_df['Week'].map(total_weekly_quantiles)
    total_monthly_quantiles = date_df.groupby(['Month'])['Streamflow (cfs)'].quantile(percentile)
    thresholds_df['Monthly Threshold'] = date_df['Month'].map(total_monthly_quantiles)
    total_seasonal_quantiles = date_df.groupby(['Season'])['Streamflow (cfs)'].quantile(percentile)
    thresholds_df['Seasonal Threshold'] = date_df['Season'].map(total_seasonal_quantiles)
    total_yearly_quantiles = date_df.groupby(['Year'])['Streamflow (cfs)'].quantile(percentile)
    thresholds_df['Yearly Threshold'] = date_df['Year'].map(total_yearly_quantiles)

    thresholds_df = thresholds_df.round(1)
    thresholds_df['Percentile'] = percentile
    return thresholds_df
