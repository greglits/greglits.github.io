from google.colab import drive
import os
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz

# Montez votre Google Drive pour accéder aux fichiers
drive.mount('/content/drive')

# Chemin du dossier contenant les fichiers HTML
html_folder_path = "/content/drive/MyDrive/greglits.github.io/fr"

# Chemin du dossier où enregistrer les fichiers XML
xml_folder_path = "/content/drive/MyDrive/greglits.github.io/Entry_xml"

# Lecture du contenu du template
with open("/content/drive/MyDrive/greglits.github.io/template_entry.xml", "r") as template_file:
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