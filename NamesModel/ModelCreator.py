import json
import os
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from dotenv import find_dotenv, load_dotenv
from sklearn.neighbors import KNeighborsRegressor


def load_data():
    with open("Assets/MetaData.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
    sheets = json_data["sheets"]
    load_dotenv(find_dotenv())
    data_path = "Assets/" + os.environ.get("DATA_PATH")
    return sheets, data_path


def createModel(data_path: str, sheet_name: str, sheet_name_english: str,
                private_name_col_name: str = "Year / Private Name",
                prev_name_col_name: str = "שם פרטי", sum_col_name: str = "sum between 1948-2021",
                predicting: int = 5, sum_column_index: int = 1, header_num=12):
    data = pd.read_excel(data_path, sheet_name=sheet_name, header=header_num)
    prev_sum_col_name = data.iloc[:, sum_column_index].name
    data.rename(columns={prev_sum_col_name: sum_col_name, prev_name_col_name: private_name_col_name}, inplace=True)

    # CLean and transform the data
    clean_data = data.drop(columns=[sum_col_name], axis=1)
    clean_data = clean_data.T
    names = clean_data.iloc[0]
    clean_data.columns = names
    clean_data.drop([private_name_col_name], inplace=True, axis=0, errors='ignore')
    for idx, row in clean_data.iterrows():
        row.replace({np.nan: 0, '.': 0, '..': 2, np.inf: 0, -np.inf: 0}, inplace=True)
    clean_data = clean_data.astype('int64')
    clean_data.set_index(pd.DatetimeIndex(clean_data.index).to_period('Y'))
    x = clean_data.index.values

    # Create new zero rows
    zeros_df = pd.DataFrame(0, index=[i + 2021 for i in range(1, predicting + 1)], columns=clean_data.columns)
    clean_data = pd.concat([clean_data, zeros_df])

    # Build a model
    for i in range(len(clean_data.columns)):
        count = clean_data.iloc[:, i].values
        years = clean_data.index.values
        # KNN
        n_neighbors = 3
        knn = KNeighborsRegressor(n_neighbors, weights="distance")
        knn = knn.fit(years[:0 - predicting].reshape(-1, 1), count[:0 - predicting].reshape(-1).ravel())
        predicted_values = knn.predict(years[0 - predicting:].reshape(-1, 1)).astype("int")

        predicted_values = np.clip(predicted_values, 0, None)
        clean_data.iloc[0 - predicting:, i] = predicted_values.flatten()

    # Export the new predicted dataframe to new excel
    clean_data.to_excel("Assets/Predicted_Names_" + sheet_name_english + ".xlsx", index=True)


def init():
    sheets, data_path = load_data()
    for sheet in sheets:
        createModel(data_path, sheet["name"], sheet["englishName"])
