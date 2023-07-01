import json
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from elasticsearch import Elasticsearch
from farm.utils import initialize_device_settings
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack import Finder
from haystack.reader.farm import FARMReader
from haystack.retriever.dense import DensePassageRetriever
import torch

import sys
sys.path.append("C:\\temp\\Names\\NamesModel\\Assets")
sys.path.append("C:\\temp\\Names\\NamesModel\\Assets\\MetaData.json")

# Step 2: Create an Elasticsearch client
client = Elasticsearch(hosts=["localhost"])
# Step 3: Create an instance of the ElasticsearchDocumentStore
document_store = ElasticsearchDocumentStore(hosts=["localhost"], index="your_index_name")


def load_data():
    with open("C:\\temp\\Names\\NamesModel\\Assets\\MetaData.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
    sheets = json_data["sheets"]
    load_dotenv(find_dotenv())
    data_path = "Assets/" + os.environ.get("DATA_PATH")
    return sheets, data_path


names = []
sheets, data_path = load_data()
for sheet in sheets:
    sheet["file"] = "C:\\temp\\Names\\NamesModel\\Assets\\Predicted_Names_" + sheet["englishName"] + ".xlsx"
for sheet in sheets:
    if sheet["englishName"] == "Jew_Male":
        path = sheet["file"]
        data = pd.read_excel(path, index_col=0)
        names = data.columns
print(names)
model = SentenceTransformer('all-MiniLM-L6-v2')
name_embeddings = model.encode(names)




name1 = "River"
name2 = "Lake"

# Encode the names into embeddings
embedding1 = model.encode([name1])[0]
embedding2 = model.encode([name2])[0]

# Calculate the cosine similarity between the embeddings
similarity = cosine_similarity([embedding1], [embedding2])[0][0]
print(f"The semantic similarity between {name1} and {name2} is: {similarity}")
