import os
import xml.etree.ElementTree as ET
import xlrd #pip install xlrd
import xlwt  
from googletrans import Translator #pip install googletrans==4.0.0rc1
# from python_translator import Translator  #Translator.translate_text() got an unexpected keyword argument 'dest'
# from google_trans_new import google_translator
from xlwt import Workbook #pip install xlwt
from bs4 import BeautifulSoup #pip install beautifulsoup4 
import asyncio
import re
# import inspect
import ssl #  pip install --upgrade certifi
import time 
# from lxml import etree
# from deep_translator import GoogleTranslator #giving same response in every row
from lxml import etree


# Define the namespace to match in the XML
namespace = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}

# Set the path to the directory containing XLIFF files
path = r'C:\Users\ADMIN\Desktop\saad\python\file-translator-app\src'

# Create a workbook and add a sheet
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

# Initialize row counter for Excel
i = 0

# def remove_namespace(tag):
#     """ Remove XML namespace from tag names """
#     return re.sub(r'\{.*?\}', '', tag)  # Remove {namespace} from tag

# # Loop through each file in the directory
# for filename in os.listdir(path):
#     if not filename.endswith('.xlf'):
#         continue  # Skip non-XLIFF files

#     # Construct the full file path
#     pathname = os.path.join(path, filename)

#     # Parse the XML file
#     tree = ET.parse(pathname)
#     root = tree.getroot()

#     # Fetch the source and target language from the <file> tag
#     s_value = t_value = None
#     for tag in root.findall('xliff:file', namespace):
#         s_value = tag.get('source-language')
#         t_value = tag.get('target-language')
        

#     # print(f"Processing {filename} with source language: {s_value} and target language: {t_value}")


#     for file_tag in root.findall('xliff:file', namespace):
#         for trans_unit in file_tag.findall('.//xliff:trans-unit', namespace):
#             source = trans_unit.find('xliff:source', namespace)

#             if source is not None:
#                 # Convert XML element to a string (keeping tags)
#                 source_html = ET.tostring(source, encoding="unicode", method="xml")
               
#                 # Remove the <source> tags while keeping inner content intact
#                 source_html = re.sub(r'</?ns0:source.*?>', '', source_html).strip()

#                 if source_html:
#                     # print(f"Found source text: {source_html}")  # Debugging: Print source text
#                     sheet1.write(i, 0, source_html)  # Write to Excel
#                     i += 1
#                 else:
#                     print("No source text found in this trans-unit (empty after stripping)")
#             else:
#                 print("No <source> tag found in this trans-unit")
            


# # Save the workbook after processing all files
# book.save(r'src/sourcefile.xls')
# print("Excel file 'sourcefile.xls' has been successfully created!")


def extract_plain_text(source_element):
    """ Extract only plain text from <source>, removing XML tags. """
    text_content = "".join(source_element.itertext()).strip()
    return text_content

def extract_g_text(source_element):
    """ Extract only text inside <g> tags within <source>. """
    g_texts = [g.text for g in source_element.findall('.//xliff:g', namespace) if g.text]
    return "\n".join(g_texts)  # Join multiple <g> texts with new lines if needed

# Loop through each XLIFF file in the directory
for filename in os.listdir(path):
    if not filename.endswith('.xlf'):
        continue  # Skip non-XLIFF files

    # Construct the full file path
    pathname = os.path.join(path, filename)

    # Parse the XML file
    tree = etree.parse(pathname)
    root = tree.getroot()

    # Fetch the source and target language from the <file> tag
    s_value = t_value = None
    for tag in root.findall('xliff:file', namespace):
        s_value = tag.get('source-language')
        t_value = tag.get('target-language')

    for file_tag in root.findall('xliff:file', namespace):
        for trans_unit in file_tag.findall('.//xliff:trans-unit', namespace):
            source = trans_unit.find('xliff:source', namespace)

            if source is not None:
                plain_text = extract_plain_text(source)
                g_text = extract_g_text(source)

                # Write only if there's relevant text
                if plain_text:
                    sheet1.write(i, 0, plain_text)  # Plain text in column A
                    i += 1
                
                if g_text:
                    sheet1.write(i, 0, g_text)  # <g> tag text in column A
                    i += 1

# Save the workbook after processing all files
book.save(r'src/sourcefile.xls')
print("Excel file 'sourcefile.xls' has been successfully created!")


# # ############################################################################################################################################

# Fix SSL issue
ssl._create_default_https_context = ssl._create_unverified_context

# Initialize translator
translator = Translator()

# Source & Target language codes
src_lang = "en"  # Change as needed
tgt_lang = "hi"  # Change as needed

# Read source Excel file
source_file = r'src/sourcefile.xls'
wb_r = xlrd.open_workbook(source_file)
sheet_r = wb_r.sheet_by_index(0)

# Create new workbook to store translations
wb_w = xlwt.Workbook()
sheet_w = wb_w.add_sheet('Translated Sheet')


async def translate_text(text):
    """Translate only the main text inside <ns0:g> and keep XML structure intact."""
    soup = BeautifulSoup(text, "html.parser")  # Parse HTML/XML
    # print("Parsed Structure:", soup.prettify()) 
    # print("fffffffffffffffffffffffffffffffffffff",soup)
    # extracted_nodes = [] 
    async def translate_node(node):
        # print("ndddyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",node)
        if node is None:  # Avoid 'NoneType' errors
            return
        xml_string = str(node) 
        root = ET.fromstring(xml_string)
        text_element = root.find(".//{namespace}g[@ctype='x-text']")
        print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj",text_element)
        # text_element = root.find(".//{*}g[@ctype='x-text']") # {*} matches any namespace
        # if text_element is not None:
        #     text = text_element.text
        #     print(text)
        # else:
        #     print("Text element not found.")
        # g_tag= ET.
        # print(node.string)
        # if (node.string and node.string.strip()):
        #     print("found:",node)
            # Translate plain text
            # try:
            #     time.sleep(1)
            #     translated_text = await asyncio.to_thread(translator.translate, node.string, dest=tgt_lang)
            #     node.string.replace_with(translated_text.text if hasattr(translated_text, 'text') else str(translated_text))
            # except Exception as e:
            #     print(f"Translation error: {e}")
    

    await translate_node(soup)  
    return str(soup)  

async def translate_sheet():
    """Translate the entire sheet asynchronously using multi-threading."""
    loop = asyncio.get_event_loop()
    tasks = {}

    for row in range(sheet_r.nrows):
        for col in range(sheet_r.ncols):
            text = str(sheet_r.cell_value(row, col)).strip()
            if text:
                tasks[(row, col)] = loop.create_task(translate_text(text))  

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    # Write results to the new sheet
    for (row, col), translated in zip(tasks.keys(), results):
        if isinstance(translated, Exception):
            print(f"Error translating: {translated}")
            sheet_w.write(row, col, sheet_r.cell_value(row, col))  # Keep original text if translation fails
        else:
            sheet_w.write(row, col, translated)

    # Save translated file
    translated_file = r'src/translate.xls'
    wb_w.save(translated_file)
    print(f"✅ Translation completed! Saved as {translated_file}")

# Run the async translation with multi-threading
if __name__ == "__main__":
    asyncio.run(translate_sheet())






# # ############################################################################################################################################




# Read translated text from Excel
# File paths
# xliff_file = r"src/Management_of Shortness_of_Breath.xlf"
# translated_file = r"src/translate.xls"

# # Read translated text from Excel
# wb = xlrd.open_workbook(translated_file)
# sheet = wb.sheet_by_index(0)

# translated_texts = []
# for row in range(sheet.nrows):
#     translated_texts.append(sheet.cell_value(row, 0))  # Assuming translations are in the first column

# # Parse XLIFF file
# tree = ET.parse(xliff_file)
# root = tree.getroot()

# # XML Namespace Handling (Adjust as per your XLIFF version)
# namespace = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}  # Modify if using XLIFF 2.0+

# i = 0
# for trans_unit in root.findall(".//xliff:trans-unit", namespace):
#     # Find the text inside <g ctype="x-text">
#     text_node = trans_unit.find(".//xliff:g[@ctype='x-text']", namespace)

#     if text_node is not None and i < len(translated_texts):
#         # Create <target> if it doesn't exist
#         target = trans_unit.find("xliff:target", namespace)
#         if target is None:
#             target = ET.SubElement(trans_unit, "{urn:oasis:names:tc:xliff:document:1.2}target")

#         # Update text inside <target> with translated text
#         target.text = translated_texts[i]
#         i += 1

# # Save the updated XLIFF file (overwrite original file)
# tree.write("src/updated_example.xlf", encoding="utf-8", xml_declaration=True)

# print("Translation updated successfully in updated_example.xlf")