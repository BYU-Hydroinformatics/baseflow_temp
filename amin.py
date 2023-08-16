import netCDF4

def list_features(dataset_path):
    """
    Lists the features (variables) available in a GLDAS NetCDF dataset.
    
    Parameters:
        dataset_path (str): Path to the GLDAS NetCDF dataset file.
    """
    # Open the NetCDF dataset
    dataset = netCDF4.Dataset(dataset_path)

    # Get the list of variable names (features) in the dataset
    variable_names = list(dataset.variables.keys())

    # Print the list of features
    print("List of features (variables) in the dataset:")
    for variable_name in variable_names:
        print(variable_name)

    # Close the dataset
    dataset.close()

# Path to your GLDAS NetCDF dataset file
dataset_path = "/users/amin/downloads/GLDAS_NOAH025_3H.A20210101.0000.021.nc4"

# Call the function to list features
list_features(dataset_path)





import netCDF4 as nc
import pandas as pd

def convert_gldas_to_dataframe(gldas_file_path, variable_name, output_csv_file):
    # Open the netCDF file
    gldas_data = nc.Dataset(gldas_file_path)

    # Extract variables from the netCDF file
    time = gldas_data.variables['time'][:]
    latitude = gldas_data.variables['lat'][:]
    longitude = gldas_data.variables['lon'][:]
    variable_data = gldas_data.variables[variable_name][:]

    # Convert time values to datetime objects (assuming a default calendar)
    time_units = gldas_data.variables['time'].units
    time_datetime = nc.num2date(time, units=time_units)

    # Flatten the latitude, longitude, and variable arrays
    latitude_flat = latitude.flatten()
    longitude_flat = longitude.flatten()
    variable_flat = variable_data.flatten()

    # Create a pandas DataFrame
    data = {
        'Time': time_datetime[0],  # Using the first datetime value for all data
        'Latitude': latitude_flat,
        'Longitude': longitude_flat,
        'Variable': variable_flat
    }

    df = pd.DataFrame(data)

    # Close the netCDF file
    gldas_data.close()

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv_file, index=False)

    print(f'Data saved to {output_csv_file}')

# Example usage
gldas_file_path = '/users/amin/downloads/GLDAS_NOAH025_3H.A20210101.0000.021.nc4'
variable_name = 'SoilMoi0_10cm_inst'
output_csv_file = 'gldas_data.csv'

convert_gldas_to_dataframe(gldas_file_path, variable_name, output_csv_file)




import os
import urllib.request
import pandas as pd

class USGSDataDownloader:
    def __init__(self):
        self.folder = os.getcwd()

    def get_user_input(self):
        self.station_number = input("What is the USGS Station ID?\t")
        self.start_date = input("Start Date (YYYY-MM-DD):\t")
        self.end_date = input("End Date (YYYY-MM-DD):\t")
    
    def generate_download_link(self):
        section1 = 'https://nwis.waterdata.usgs.gov/nwis/dv?referred_module=sw&search_site_no='
        section2 = '&search_site_no_match_type=exact&site_tp_cd=OC&site_tp_cd=OC-CO&site_tp_cd=ES&site_tp_cd='\
        'LK&site_tp_cd=ST&site_tp_cd=ST-CA&site_tp_cd=ST-DCH&site_tp_cd=ST-TS&index_pmcode_00060=1&group_key='\
        'NONE&sitefile_output_format=html_table&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=date_range&begin_date='
        section3 = '&end_date='
        section4 = '&format=rdb&date_format=YYYY-MM-DD&rdb_compression=value&list_of_search_criteria=search_site_no%2Csite_tp_cd%2Crealtime_parameter_selection'
    
        self.link = (section1 + self.station_number + section2 + self.start_date + section3 + self.end_date + section4)

    def download_data(self):
        USGS_page = urllib.request.urlopen(self.link)
        downloaded_data = USGS_page.read()
        self.str_data = downloaded_data.decode()

    def extract_station_name(self):
        f_str_data = self.str_data.split('\n')
        self.station_name = ''
    
        for line in range(len(f_str_data)):
            if f_str_data[line].startswith("#    USGS"):
                self.station_name = f_str_data[line][3:]

    def organize_dataset(self):
        date_flow = ''
        f_str_data = self.str_data.split('\n')
    
        for line in range(len(f_str_data)):
            if f_str_data[line].startswith("USGS"):
                data = f_str_data[line][14:]
                columns = data.split('\t')
                rows = ','.join([columns[0], (columns[1])])
                date_flow += rows + '\n'
        self.date_flow = date_flow.encode()
    
        with open(self.folder + '/USGS_Data_for_' + self.station_number + '.txt', 'wb') as text:
            text.write(self.date_flow)

    def process_data(self):
        filename = self.folder + '/USGS_Data_for_' + self.station_number + '.txt'
        columns = ['Date', 'Discharge (cfs)']
        df = pd.read_csv(filename, header=None, names=columns, parse_dates=[0])
        df = df.set_index(['Date'])
        df['Discharge (cfs)'] = pd.to_numeric(df['Discharge (cfs)'], errors='coerce')
        return df

if __name__ == "__main__":
    usgs_downloader = USGSDataDownloader()
    usgs_downloader.get_user_input()
    usgs_downloader.generate_download_link()
    usgs_downloader.download_data()
    usgs_downloader.extract_station_name()
    usgs_downloader.organize_dataset()
    df = usgs_downloader.process_data()
    print(df.head())
