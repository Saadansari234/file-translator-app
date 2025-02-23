import xml.etree.cElementTree as ET
import xlrd
import xlwt
from xlwt import Workbook
from googletrans import Translator  
from bs4 import BeautifulSoup
import os
import asyncio
import ssl

path = r'C:\Users\DELL\Desktop\python\file-translator-app\src'
for filename in os.listdir(path):
    if not filename.endswith('.xlf'): continue
    pathname = os.path.join(path, filename)
    tree = ET.parse(pathname)


#get the root element 
tree=ET.ElementTree(file=pathname)
root=tree.getroot()


#Create a workbook 
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

#fetch each element within the source tag and save it in source file
i=0
for trans in root:
   for header in trans:
        for body in header:
            for source in body:
                # all_text = ""
                for element in source.iter():  # Iterate over all descendants of 'source'
                   text_content = element.text.strip() if element.text else None  # Remove leading/trailing spaces

                   if 'ctype' in element.attrib and element.attrib['ctype'] == 'x-text' and text_content:
                        sheet1.write(i, 0, text_content)  
                        i += 1   
                   elif not element.attrib and text_content:  # Ensure non-empty text
                        sheet1.write(i, 0, text_content)  
                        i += 1
                       
print("saving .....")                    
book.save('src/sourcefile.xls')
print("saved successfully")



# #########################################################################################################

# #Create the instance of google translator class

# Fix SSL issue
# ssl._create_default_https_context = ssl._create_unverified_context

# translator = Translator()
# location = (r'sourcefile.xls')
# #Writing to file
# wb = Workbook()
# sheet1 = wb.add_sheet('sheet 1')
# #Reading file
# wb_r = xlrd.open_workbook(location)
# sheet = wb_r.sheet_by_index(0)
# sheet.cell_value(0,0)
# print('********************') 

# Fix SSL issue
ssl._create_default_https_context = ssl._create_unverified_context

translator = Translator()
location = (r'src/sourcefile.xls')
#Writing to file
wb = Workbook()
sheet1 = wb.add_sheet('sheet 1')
#Reading file
wb_r = xlrd.open_workbook(location)
sheet = wb_r.sheet_by_index(0)
sheet.cell_value(0,0)
print('********************') 

#for each row and column, fetch the text, translate, and save in translate file
# async def translate_cell():
#     for column in range(sheet.nrows):
#         for row in range(sheet.ncols):
#             value = str(sheet.cell_value(column, row))
#             value = await asyncio.to_thread(translator.translate(value,dest="zh-cn"))
#             print(value)
#             value=str(value).strip()
#             sheet1.write(column, row, value)
#     wb.save(r'translate.xls')

async def translate_cell():
    for row in range(sheet.nrows):  # Iterate over rows first
        for col in range(sheet.ncols):  # Then iterate over columns
            value = str(sheet.cell_value(row, col)).strip()

            # Properly await the async translate function
            translated = await translator.translate(value, dest="hi")
            translated_text = translated.text  # Extract translated text
            
            print(translated_text)
            sheet1.write(row, col, translated_text)  # Write translated text to new sheet

    wb.save('src/translate.xls')  # Save the translated file

# Run the function in an event loop
asyncio.run(translate_cell())




# ####################################################################################################


#create a list and store all the translated text
translatedtext=[]
# opening the source excel file
filename ="src/translate.xls"
twb_r = xlrd.open_workbook(filename)
tsheet = twb_r.sheet_by_index(0)
tsheet.cell_value(0,0)
# opening the destination excel file 
for column in range(tsheet.nrows):
    for row in range(tsheet.ncols):
        value = str(tsheet.cell_value(column, row))
        translatedtext.append(value)

print(translatedtext)


#One by one store the translated text within the respective target tag and save it.
# Find and modify translation units
index = 0  # Track translated text index
for trans_unit in root.iter("trans-unit"):  # Find all translation units
    source = trans_unit.find("source")  # Locate source tag inside trans-unit
    if source is not None and index < len(translatedtext):
        # Check if a target tag exists; if not, create one
        target = trans_unit.find("target")
        if target is None:
            target = ET.Element("target")
            trans_unit.append(target)

        # Insert translated text
        target.text = translatedtext[index]
        index += 1

# Save the modified XLF file
tree.write(r'src/translated.xlf', encoding="utf-8", xml_declaration=True)

print(f"Translated XLF file saved at: {'src/translated.xlf'}")