# Étape 1 : Monter Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Importer les bibliothèques nécessaires Resize Image
from PIL import Image
import os

# Étape 2 : Installer la bibliothèque markdown2 pour convertir Markdown en HTML
!pip install markdown2

import markdown2
from datetime import datetime

#librairie cretation blog et index
import bs4


##############   Effacer vieille version de atom.xlm (car sinon script RSS bug)   ############## 

os.remove("/content/drive/MyDrive/greglits.github.io/Entry_xml/atom.xml")


##############  Script resize image  ############## 

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



###########################   Converter fichier .MD en fichier .HTML   ############## 


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



#############   Script création blog.html et et préparation création index.html    ############## 




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



################ Création de index.html sur base du template "template_index.html" ############## 

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





##########    télécharger les fichiers modifiés    ############## 

from google.colab import files

# Chemins des fichiers à télécharger
files_to_download = [
    "/content/drive/MyDrive/greglits.github.io/index.html",
    "/content/drive/MyDrive/greglits.github.io/blog.html"
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






################ Script création atom.xml   ############## 


from bs4 import BeautifulSoup
from dateutil import tz

##############  Partie 1 du code : création des fichiers "entry" ############## 

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

########   Partie  2 du code : création du "bloc"   ############## 

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



######## Partie  3 du code intégration du "bloc" dans le tempalte final atom.rss ############## 

# Chemin du dossier où enregistrer les fichiers XML
xml_folder_path = "/content/drive/MyDrive/greglits.github.io/Entry_xml"

# Chemin du fichier bloc.xml
bloc_xml_path = os.path.join(xml_folder_path, "bloc.xml")

# Lecture du contenu du fichier bloc.xml
with open(bloc_xml_path, "r") as bloc_xml_file:
    bloc_xml_content = bloc_xml_file.read()

# Suppression de toutes les balises "<article>" et "</article>"
bloc_xml_content = bloc_xml_content.replace("<article>", "").replace("</article>", "")

# Lecture du contenu du template "template_atom.xml"
with open("/content/drive/MyDrive/greglits.github.io/template_atom.xml", "r") as template_atom_file:
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



#########   Partie 4 : télécharger le fichier  ############## 

from google.colab import files

# Chemins des fichiers à télécharger
files_to_download = [
    "/content/drive/MyDrive/greglits.github.io/Entry_xml/atom.xml"
]

# Télécharger les fichiers spécifiés
for file_path in files_to_download:
    files.download(file_path)

print("Le fichier 'atom.xml' a été téléchargé avec succès")



######## Partie 5  : vider le dossier entre_xml sauf atom.xml  ############## 

# Chemin du dossier
folder_path_entry = "/content/drive/MyDrive/greglits.github.io/Entry_xml"

# Liste tous les fichiers dans le dossier
files = os.listdir(folder_path_entry)

# Parcourir tous les fichiers dans le dossier
for file_name in files:
    # Vérifie si le fichier n'est pas "atom.xml"
    if file_name != "atom.xml":
        # Construit le chemin complet du fichier
        file_path = os.path.join(folder_path_entry, file_name)
        # Vérifie si le chemin est un fichier
        if os.path.isfile(file_path):
            # Supprime le fichier
            os.remove(file_path)
            print(f"Fichier supprimé: {file_name}")
