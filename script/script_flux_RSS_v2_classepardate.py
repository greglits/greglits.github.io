from google.colab import drive
from xml.etree import ElementTree as ET
from datetime import datetime
import os

# Montez votre Google Drive pour accéder aux fichiers
drive.mount('/content/drive')

def create_atom_xml(directory_path, output_file):
    # Create the root element
    feed = ET.Element('feed', xmlns='http://www.w3.org/2005/Atom')

    # Add title, subtitle, and link elements
    title = ET.SubElement(feed, 'title')
    title.text = 'Do We Have a Problem? Blog of Grégoire Lits, assistant professor in media sociology'

    subtitle = ET.SubElement(feed, 'subtitle')
    subtitle.text = 'Personal blog of Grégoire Lits'

    link = ET.SubElement(feed, 'link', href='https://gregoirelits.eu')

    # Collect all HTML files with their last modified timestamp
    files = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.html'):
            filepath = os.path.join(directory_path, filename)
            last_modified_timestamp = os.path.getmtime(filepath)
            files.append((filepath, last_modified_timestamp))

    # Sort files by last modified date, newest first
    files.sort(key=lambda x: x[1], reverse=True)

    # Iterate through sorted HTML files
    for filepath, _ in files:
        filename = os.path.basename(filepath)
        last_modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%dT%H:%M:%SZ')

        # Create entry for each HTML file
        entry = ET.SubElement(feed, 'entry')

        entry_title = ET.SubElement(entry, 'title')
        entry_title.text = filename[:-5]  # remove '.html' extension

        entry_link = ET.SubElement(entry, 'link', href=f'https://gregoirelits.eu/fr/{filename}')

        entry_id = ET.SubElement(entry, 'id')
        entry_id.text = f'https://gregoirelits.eu/fr/{filename}'

        entry_updated = ET.SubElement(entry, 'updated')
        entry_updated.text = last_modified

        # Lire le contenu du fichier HTML
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Utiliser une expression régulière ou un analyseur HTML pour extraire le contenu
        import re
        match = re.search(r'<article>(.*?)</article>', html_content, re.DOTALL)
        summary_content = match.group(1) if match else 'No summary available'

        # Ajouter le champ "summary"
        entry_summary = ET.SubElement(entry, 'summary')
        entry_summary.text = summary_content

    # Create and write the Atom XML file
    tree = ET.ElementTree(feed)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    # Chemin du dossier local sur Google Drive
    site_directory = '/content/drive/MyDrive/greglits.github.io/fr'
    atom_xml_output = '/content/drive/MyDrive/greglits.github.io/atom.xml'

    create_atom_xml(site_directory, atom_xml_output)
    print(f'Atom XML file created: {atom_xml_output}')