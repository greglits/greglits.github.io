from google.colab import drive
import os
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz

# Montez votre Google Drive pour accéder aux fichiers
drive.mount('/content/drive')

# Chemin du dossier contenant les fichiers HTML
html_folder_path = "/content/drive/MyDrive/XXX/fr"

# Chemin du dossier où enregistrer les fichiers XML
xml_folder_path = "/content/drive/MyDrive/XXX/Entry_xml"

# Lecture du contenu du template
with open("/content/drive/MyDrive/XXX/template_entry.xml", "r") as template_file:
    template_content = template_file.read()

# Parcourir les fichiers HTML dans le dossier
for html_file in os.listdir(html_folder_path):
    if html_file.endswith(".html"):
        # Chemin complet du fichier HTML
        html_file_path = os.path.join(html_folder_path, html_file)

        # Lecture du contenu du fichier HTML
        with open(html_file_path, "r") as html_content:
            html_content = html_content.read()
            # Parsing du contenu HTML avec BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Extraction du titre entre les balises <h1></h1>
            h1_content = soup.find("h1").text.strip()

            # Extraction du contenu HTML entre les balises <article></article>
            article_content = soup.find("article").prettify()

            # Date de dernière modification du fichier HTML
            date_update = datetime.fromtimestamp(os.path.getmtime(html_file_path)).astimezone(tz.UTC).isoformat()

            # Remplacement des balises dans le template
            xml_content = template_content.replace("$H1", h1_content)\
                                           .replace("$HTML_LINK", html_file)\
                                           .replace("$DATE_UPDATE", date_update)\
                                           .replace("$CONTEN_HTML", article_content)

            # Chemin complet du fichier XML à créer
            xml_file_path = os.path.join(xml_folder_path, html_file.replace(".html", ".xml"))

            # Écriture du contenu dans le fichier XML
            with open(xml_file_path, "w") as xml_file:
                xml_file.write(xml_content)

print("Conversion terminée. Les fichiers XML ont été enregistrés dans", xml_folder_path)

# Partie 2 du code ######################"

# Création du fichier "bloc.xml"
xml_files = sorted(os.listdir(xml_folder_path), reverse=True)  # Liste des fichiers XML ordonnée Z-A

# Chemin du fichier "bloc.xml"
bloc_xml_path = os.path.join(xml_folder_path, "bloc.xml")

# Écriture du contenu des fichiers XML dans "bloc.xml"
with open(bloc_xml_path, "w") as bloc_xml_file:
    # bloc_xml_file.write("<?xml version='1.0' encoding='UTF-8'?>\n<entries>\n")
    for xml_file in xml_files:
        if xml_file != "bloc.xml":
            with open(os.path.join(xml_folder_path, xml_file), "r") as current_xml_file:
                bloc_xml_file.write(current_xml_file.read())
    # bloc_xml_file.write("</entries>")

print("Le fichier 'bloc.xml' a été créé avec succès dans", xml_folder_path)


# Partie 3 du code #############


# Chemin du dossier où enregistrer les fichiers XML
xml_folder_path = "/content/drive/MyDrive/XXX/Entry_xml"

# Chemin du fichier bloc.xml
bloc_xml_path = os.path.join(xml_folder_path, "bloc.xml")

# Lecture du contenu du fichier bloc.xml
with open(bloc_xml_path, "r") as bloc_xml_file:
    bloc_xml_content = bloc_xml_file.read()

# Suppression de toutes les balises "<article>" et "</article>"
bloc_xml_content = bloc_xml_content.replace("<article>", "").replace("</article>", "")

# Lecture du contenu du template "template_atom.xml"
with open("/content/drive/MyDrive/XXX/template_atom.xml", "r") as template_atom_file:
    template_content = template_atom_file.read()

# Remplacement de la balise $CONTENT_BLOC par le contenu de bloc.xml sans les balises "<article>"
xml_content = template_content.replace("$CONTENT_BLOC", bloc_xml_content)

# Obtention de la date actuelle au format RFC-3339 (ISO 8601)
date_updated2 = datetime.now().isoformat()

# Remplacement de la balise $DATE_Update par la date de création du fichier atom.xml
xml_content = xml_content.replace("$DATE_Update", date_updated2)

# Chemin du fichier atom.xml
atom_xml_path = os.path.join(xml_folder_path, "atom.xml")

# Écriture du contenu dans le fichier atom.xml
with open(atom_xml_path, "w") as atom_xml_file:
    atom_xml_file.write(xml_content)

print("Le fichier 'atom.xml' a été créé avec succès dans", xml_folder_path)
