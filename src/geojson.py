import json
from tkinter import filedialog
from tkinter import *
import geopandas as gp


def read_json_file(path):
    # Opening JSON file
    file = open(path, "r")
    # returns JSON object as a dictionary
    return json.loads(file.read())


def get_path():
    root = Tk()
    root.filename = filedialog.askopenfilename(title="Select file",
                                               filetypes=(("jpeg files", "*.geojson"), ("all files", "*.*")))
    return root.filename


gdf = gp.read_file(get_path())

gdf_b = gdf[gdf['geometry'].apply(lambda x: x.type == 'LineString')]
print(gdf_b)

gdf.to_csv("civic_substation.csv")