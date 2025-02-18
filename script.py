import os
import xml.etree.ElementTree as ET
import xlrd
import xlwt
from googletrans import Translator 
from xlwt import Workbook
from bs4 import BeautifulSoup
import asyncio


# Define the namespace to match in the XML
namespace = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}

# Set the path to the directory containing XLIFF files
path = r'C:\Users\DELL\Desktop\python\file-translator\src'

# Create a workbook and add a sheet
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

# Initialize row counter for Excel
i = 0

# Loop through each file in the directory
for filename in os.listdir(path):
    if not filename.endswith('.xlf'):
        continue  # Skip non-XLIFF files

    # Construct the full file path
    pathname = os.path.join(path, filename)

    # Parse the XML file
    tree = ET.parse(pathname)
    root = tree.getroot()

    # Fetch the source and target language from the <file> tag
    s_value = t_value = None
    for tag in root.findall('xliff:file', namespace):
        s_value = tag.get('source-language')
        t_value = tag.get('target-language')

    print(f"Processing {filename} with source language: {s_value} and target language: {t_value}")

    # Fetch text from <source> tags and write to Excel
    for file_tag in root.findall('xliff:file', namespace):
        for body in file_tag.findall('xliff:body', namespace):
            for trans_unit in body.findall('xliff:trans-unit', namespace):
                source = trans_unit.find('xliff:source', namespace)
                if source is not None and source.text:
                    print(f"Found source text: {source.text}")  # Debug: Check source text
                    sheet1.write(i, 0, source.text)  # Write source text to Excel
                    i += 1
                else:
                    print("No source text found in this trans-unit")  # Debug: Check empty source

# Save the workbook after processing all files
book.save('sourcefile.xls')
print("Excel file 'sourcefile.xls' has been successfully created!")






# Create the instance of Google Translator class
translator = Translator()

# Set the path for the source file and create a new Excel workbook for the translated text
location = r'sourcefile.xls'
wb = xlwt.Workbook(encoding="utf-8")
sheet1 = wb.add_sheet('sheet 1')

# Reading the source file
wb_r = xlrd.open_workbook(location)
sheet = wb_r.sheet_by_index(0)

# Set source and target languages
s_value = 'en'  # Example: English
t_value = 'es'  # Example: Spanish

# Create an asynchronous function for translation
async def translate_text(value):
    translated = await translator.translate(value, src=s_value, dest=t_value)
    return translated.text

async def main():
    print('********************')

    # For each row and column, fetch the text, translate it, and save it in the translate file
    for column in range(sheet.nrows):
        for row in range(sheet.ncols):
            value = str(sheet.cell_value(column, row))

            # To detect any other XML tags within the source text
            htmltag = bool(BeautifulSoup(value, "html.parser").find())

            if htmltag:
                # If it's an HTML tag, write the value as is
                sheet1.write(column, row, value)
            else:
                # Translate text if no HTML tags are found
                translated_value = await translate_text(value)
                translated_value = str(translated_value).strip()
                sheet1.write(column, row, translated_value)

    # Save the translated file
    wb.save(r'translate.xls')
    print("Excel file 'translate.xls' has been successfully created!")

# Run the asynchronous main function
asyncio.run(main())