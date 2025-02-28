import xml.etree.cElementTree as ET
import xlrd
import xlwt
from xlwt import Workbook
from googletrans import Translator
from bs4 import BeautifulSoup
import os
import asyncio
import ssl
import copy
import re

path = r"C:\Users\ADMIN\Desktop\saad\python\file-translator-app\src"



def translate_file(file_path):

    if not file_path.endswith(".xlf"):
        print("Not an XLIFF file.")
        return None
    tree = ET.parse(file_path)
    root = tree.getroot()
    print(f"Processing file: {file_path}")

    source_Data= []

    # fetch each element within the source tag and save it in source file

    for trans in root:
        for header in trans:
            for body in header:
                for source in body:
                    # all_text = ""
                    for (
                        element
                    ) in source.iter():  # Iterate over all descendants of 'source'
                        text_content = (
                            element.text.strip() if element.text else None
                        )  # Remove leading/trailing spaces

                        if (
                            "ctype" in element.attrib
                            and element.attrib["ctype"] == "x-text"
                            and text_content
                        ):
                            source_Data.append(text_content)
                        elif not element.attrib and text_content:  # Ensure non-empty text
                            source_Data.append(text_content)

    print("saving .....")
    # book.save("src/sourcefile.xls")
    print("saved successfully", source_Data)


# #########################################################################################################

# #Create the instance of google translator class


# Fix SSL issue
    ssl._create_default_https_context = ssl._create_unverified_context

    translator = Translator()


    translated_Data=[]

    async def translate_cell():
        for value in source_Data:
                value = str(value).strip()
                

                if re.search(r"%.*%", value):
                    specialTxtList=[]
                    splittedValue = re.findall(r"%[^%]+%|\S+", value)
                    for elem in splittedValue:
                        if "%" not in elem:
                            translated = await translator.translate(elem, dest="hi")
                            elem = translated.text
                            specialTxtList.append(elem)
                        else:
                            specialTxtList.append(elem)   

                    specialTranslatedText= " ".join(specialTxtList)
                    print("specialTextbbbbbbbbbbbbbbbbbbb", specialTranslatedText)
                    translated_Data.append(specialTranslatedText)

                else:

                    # Properly await the async translate function
                    translated = await translator.translate(value, dest="hi")
                    translated_text = translated.text  # Extract translated text

                    print(translated_text)
                    translated_Data.append(translated_text)

        # translated data
        print("translated data", translated_Data)


# # Run the function in an event loop
    asyncio.run(translate_cell())


    return source_Data, translated_Data



# ####################################################################################################

def save_xliff_file(file_path, translated_data):
    
    
    if not file_path.endswith(".xlf"):
        print("Not an XLIFF file.")
        return None
    tree = ET.parse(file_path)
    root = tree.getroot()
    print(f"Processing file: {file_path}")

    # Define namespace
    namespace = "urn:oasis:names:tc:xliff:document:1.2"

    index = 0

    for files in root:
        for Outer_Tags in files:

            for trans_unit in Outer_Tags:
                target = trans_unit.find(f"{{{namespace}}}target")
                if target is None:
                    target = ET.Element(f"{{{namespace}}}target")
                    for source in trans_unit:
                        
                        # print("sorceeeeeeee", source)
                        if source is not None:
                            text_content = source.text.strip() if source.text else None
                            if not source.attrib and text_content:  # If plain text without attributes
                                text_element = ET.Element(f"{{{namespace}}}text")  # Create a new XML element
                                text_element.text = text_content  # Assign stripped text
                                target.append(copy.deepcopy(text_element))  # Append the new element
        
                            elif list(source):  # If there are child elements
                                for child in source:
                                    target.append(copy.deepcopy(child))  # Append each child to target
        
                            else:
                                print("jjjjjjj")

                    trans_unit.append(target)

                for element in target.findall("*"):  
                        text_content = element.text.strip() if element.text else None
                        # Only modify <g ctype="x-text"> inside <target>
                        if "ctype" in element.attrib and element.attrib["ctype"] == "x-text" and text_content:
                                element.text = translated_data[index]  # Assign cleaned translated text
                                index += 1
                        
                            
                        elif not element.attrib and text_content :
                                element.text = translated_data[index]
                                index += 1
                        


    tree.write(r"media/translated.xlf", encoding="utf-8", xml_declaration=True)