# Étape 1 : Monter Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Étape 2 : Installer la bibliothèque markdown2 pour convertir Markdown en HTML
!pip install markdown2

# Étape 3 : Importer les bibliothèques nécessaires
import os
import markdown2
from datetime import datetime

# Étape 4 : Définir les chemins de base
base_path = "/content/drive/MyDrive/greglits.github.io"
md_path = f"{base_path}/converter"
html_path = f"{base_path}/fr"
template_path = f"{html_path}/template.html"

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
