from processing import *
from models import *
from plots import *
import ssl
import certifi

# This restores the same behavior as before.
ssl._create_default_https_context = ssl._create_unverified_context



def main():
    dataset = fetch_and_process_usgs_data('01636500', '2018-01-01', '2019-10-01')
    cleaned_dataset = clean_ffill(dataset)
    dataset_models = cleaned_dataset.copy()
    dataset_models = separate_date_parameters(dataset_models)
    dataset_models['Lyne_Hollick'] = lyne_hollick(dataset_models['Discharge'], 0.925)
    dataset_models['Chapman'] = chapman(dataset_models['Discharge'], 0.925, 0.075)
    dataset_models['Eckhardt'] = eckhardt(dataset_models['Discharge'], 0.8, 0.6)
    dataset_models['Chapman_Maxwell'] = chapman_maxwell(dataset_models['Discharge'], 0.7)
    
    dataset_models = quantiles(dataset_models, 'Month', 0.9)

    column_names = dataset_models.columns[4:].tolist()

    label_rows(dataset_models, column_names, 200)


    # plot the data
    plot_discharge_and_models(dataset_models, column_names)
    # plot_hydrograph_recession(dataset_models)

if __name__ == "__main__":
    main()



#    +------------+-----------+------+-------+-----+---------+---------+
#    |            | Discharge | Year | Month | Day | Model 1 | Model 2 |
#    +------------+-----------+------+-------+-----+---------+---------+
#    | YYYY-MM-DD |           |      |       |     |         |         |
#    +------------+-----------+------+-------+-----+---------+---------+
