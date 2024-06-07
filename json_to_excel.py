from json_excel_converter import Converter
from json_excel_converter.xlsx import Writer
import json
import os

    
filename = input("File to be converted: ")
with open(filename, 'r') as f:
    data = json.load(f)

conv = Converter()
output_file_path = os.path.join('xls', f"{filename[:-5]}.xlsx")
conv.convert(data, Writer(file=output_file_path))