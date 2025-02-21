from xml.etree import ElementTree as ET

def extract_x_text(file_path):
    """
    Extracts all text from <g> elements where ctype="x-text" in the given XLIFF file.
    
    :param file_path: Path to the XLIFF file
    :return: List of extracted text values
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    namespace = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}
    x_text_values = []
    
    # Find all <g> elements with ctype="x-text"
    for g in root.findall(".//g[@ctype='x-text']", namespaces=namespace):
        x_text_values.append(g.text.strip() if g.text else "")
    
    return x_text_values

# Example usage
xliff_file = "C:\\Users\\ADMIN\\Desktop\\saad\\python\\file-translator-app\\src\\de"
texts = extract_x_text(xliff_file)
print(texts)