# Étape 1 : Monter Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Importer les bibliothèques nécessaires Resize Image
from PIL import Image
import os

# Étape 2 : Installer la bibliothèque markdown2 pour convertir Markdown en HTML
!pip install markdown2

# Étape 3 : Importer les bibliothèques nécessaires MD-> HTML

import markdown2
from datetime import datetime

#librairie cretation blog et index
import bs4
from datetime import datetime

# librairie ATOM
from xml.etree import ElementTree as ET
from datetime import datetime
import os



############## Scripte resize image



# Chemin vers le dossier sur Google Drive
folder_path = '/content/drive/MyDrive/greglits.github.io/files'

# Liste tous les fichiers dans le dossier
files = os.listdir(folder_path)

# Parcourir tous les fichiers dans le dossier
for file in files:
    # Construire le chemin complet vers le fichier
    file_path = os.path.join(folder_path, file)

    # Tenter d'ouvrir l'image
    try:
        with Image.open(file_path) as img:
            # Obtenir les dimensions de l'image
            width, height = img.size

            # Vérifier si la largeur de l'image est supérieure à 625px
            if width > 625:
                # Calculer le nouveau rapport de hauteur en conservant le ratio
                new_height = int((625.0 / width) * height)

                # Redimensionner l'image
                img_resized = img.resize((625, new_height), Image.ANTIALIAS)

                # Sauvegarder l'image redimensionnée, en écrasant l'ancienne
                # ou en la sauvegardant sous un nouveau nom si vous préférez conserver l'original
                img_resized.save(file_path)

                print(f'Image "{file}" redimensionnée à 625x{new_height}.')
    except IOError:
        # Le fichier n'est pas une image ou ne peut pas être ouvert
        print(f'Le fichier "{file}" n\'est pas une image ou ne peut pas être ouvert.')



########################### Converter MD-HTML


# Étape 4 : Définir les chemins de base
base_path = "/content/drive/MyDrive/greglits.github.io"
md_path = f"{base_path}/converter"
html_path = f"{base_path}/fr"
template_path = f"{base_path}/template.html"

# Étape 5 : Lire le contenu du template HTML
with open(template_path, "r") as file:
    template_content = file.read()

# Étape 6 : Fonction pour convertir les fichiers .md en .html
def convert_md_to_html(md_file_path):
    # Lire le contenu du fichier Markdown
    with open(md_file_path, "r") as file:
        md_content = file.readlines()

    # Extraire le titre, le contenu (sans le premier et le dernier paragraphe) et le hashtag
    title = md_content[0].strip()
    # Le contenu HTML exclut maintenant la dernière ligne pour le hashtag
    html_content = markdown2.markdown("".join(md_content[2:-1]))
    hashtag = md_content[-1].strip()  # La dernière ligne est utilisée pour le hashtag

    # Utiliser le nom du fichier Markdown original pour le fichier HTML, mais avec l'extension .html
    html_file_name = os.path.basename(md_file_path).replace('.md', '.html')

    # Remplacer les balises dans le template avec le contenu, le titre, la date et le hashtag
    final_content = template_content.replace("$CONTENT", html_content)
    final_content = final_content.replace("$TITLE", title)
    date_today = datetime.now().strftime("%Y-%m-%d")
    final_content = final_content.replace("$date_of_the_day", date_today)
    final_content = final_content.replace("$HTMLLINK", html_file_name)
    # Remplacement de la balise $HASHTAG par le hashtag extrait
    final_content = final_content.replace("$HASHTAG", hashtag)

    # Écrire le contenu dans un nouveau fichier HTML
    with open(f"{html_path}/{html_file_name}", "w") as file:
        file.write(final_content)

    # Retourner le nom du fichier pour le déplacer ensuite
    return md_file_path, f"{md_path}/content_MD/{os.path.basename(md_file_path)}"

# Étape 7 : Convertir tous les fichiers .md du dossier spécifié
for md_file in os.listdir(md_path):
    if md_file.endswith(".md"):
        src, dest = convert_md_to_html(f"{md_path}/{md_file}")
        # Déplacer le fichier .md original dans le dossier spécifié
        os.rename(src, dest)

# Note : Ce script suppose que le dossier "/content_MD" existe déjà.



#############   Scipte création Blog et index.html




# Chemin vers le dossier contenant les fichiers HTML
directory_path = "/content/drive/MyDrive/greglits.github.io/fr"

# Chemin vers le fichier template et le nouveau fichier blog.html
template_path = "/content/drive/MyDrive/greglits.github.io/template_blog.html"
new_blog_path = "/content/drive/MyDrive/greglits.github.io/blog.html"

# Liste pour stocker les tuples de (date de modification, élément de liste HTML)
items_with_dates = []

# Parcourir le dossier pour trouver les fichiers qui commencent par "2024"
for filename in os.listdir(directory_path):
    if filename.startswith("2024") and filename.endswith(".html"):
        file_path = os.path.join(directory_path, filename)
        # Obtenir la date de modification du fichier
        mod_time = os.path.getmtime(file_path)
        with open(file_path, 'r') as file:
            contents = file.read()
            soup = bs4.BeautifulSoup(contents, 'html.parser')
            # Extraire le contenu de la balise <h1>
            h1_text = soup.find('h1').text.strip()
            # Construire l'élément de la liste HTML
            list_item = f'<li>{filename[:10]} - <a href="fr/{filename}">{h1_text}</a></li>'
            # Ajouter le tuple (date de modification, élément de liste HTML) à la liste
            items_with_dates.append((mod_time, list_item))

# Trier la liste par date de modification, le fichier le plus récent en premier
items_with_dates.sort(reverse=True, key=lambda x: x[0])

# Extraire les éléments de liste HTML triés
html_list = [item[1] for item in items_with_dates]

# Générer la chaîne HTML pour la liste
html_list_str = '\n'.join(html_list)

# Lire le contenu du fichier template
with open(template_path, 'r') as file:
    template_content = file.read()

# Remplacer le placeholder par la liste HTML générée
new_content = template_content.replace('$LISTE_POST', html_list_str)

# Écrire le nouveau contenu dans le fichier blog.html
with open(new_blog_path, 'w') as file:
    file.write(new_content)

print("Le fichier blog.html a été créé avec succès, avec les éléments classés par date de modification.")



################ CREATION de INDEX.HTML

# Chemin vers le fichier template pour index.html
template_index_path = "/content/drive/MyDrive/greglits.github.io/template_index.html"
index_html_path = "/content/drive/MyDrive/greglits.github.io/index.html"

# Lire le contenu du fichier template pour index.html
with open(template_index_path, 'r') as file:
    template_index_content = file.read()

# Remplacer le placeholder par la même liste HTML générée pour blog.html
new_index_content = template_index_content.replace('$LISTE_POST', html_list_str)

# Écrire le nouveau contenu dans le fichier index.html
with open(index_html_path, 'w') as file:
    file.write(new_index_content)

print("Le fichier index.html a été créé avec succès, avec les éléments classés par date de modification.")



################ Scipte création atom.xml



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


########## télécharger les fihciers modifiés

from google.colab import files

# Chemins des fichiers à télécharger
files_to_download = [
    "/content/drive/MyDrive/greglits.github.io/index.html",
    "/content/drive/MyDrive/greglits.github.io/blog.html",
    "/content/drive/MyDrive/greglits.github.io/atom.xml"
]

# Télécharger les fichiers spécifiés
for file_path in files_to_download:
    files.download(file_path)

# Trouver le fichier HTML le plus récemment modifié dans le dossier spécifié
most_recent_file_path = None
most_recent_mod_time = 0
for filename in os.listdir(directory_path):
    if filename.endswith(".html"):
        file_path = os.path.join(directory_path, filename)
        mod_time = os.path.getmtime(file_path)
        if mod_time > most_recent_mod_time:
            most_recent_mod_time = mod_time
            most_recent_file_path = file_path

# Télécharger le fichier HTML le plus récemment modifié
if most_recent_file_path is not None:
    files.download(most_recent_file_path)