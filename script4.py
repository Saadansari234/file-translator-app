import xml.etree.cElementTree as ET
import xlrd
import xlwt
from xlwt import Workbook
from googletrans import Translator  
from bs4 import BeautifulSoup
import os


path = r'\src'
for filename in os.listdir(path):
    if not filename.endswith('.xlf'): continue
    pathname = os.path.join(path, filename)
    tree = ET.parse(pathname)