#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de site web statique à partir de fichiers Markdown
Version adaptée pour PC (Windows/Mac/Linux)
"""

from PIL import Image
import os
import markdown2
from datetime import datetime
import bs4
from dateutil import tz

# ============================================================================
# CONFIGURATION - Modifiez ces chemins selon votre structure de dossiers
# ============================================================================

# Option 1 : Utiliser le dossier du script
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Option 2 : Spécifier un chemin absolu (décommentez et modifiez si besoin)
# BASE_PATH = "C:/Users/VotreNom/Documents/greglits.github.io"  # Windows
# BASE_PATH = "/home/votrenom/greglits.github.io"  # Linux/Mac

# Sous-dossiers
IMAGES_FOLDER = os.path.join(BASE_PATH, "files")
MD_FOLDER = os.path.join(BASE_PATH, "converter")
HTML_FOLDER = os.path.join(BASE_PATH, "fr")
XML_FOLDER = os.path.join(BASE_PATH, "Entry_xml")
TEMPLATE_FOLDER = os.path.join(BASE_PATH, "template")

# Templates
TEMPLATE_ARTICLE = os.path.join(TEMPLATE_FOLDER, "template.html")
TEMPLATE_BLOG = os.path.join(TEMPLATE_FOLDER, "template_blog.html")
TEMPLATE_INDEX = os.path.join(TEMPLATE_FOLDER, "template_index.html")
TEMPLATE_ENTRY = os.path.join(TEMPLATE_FOLDER, "template_entry.xml")
TEMPLATE_ATOM = os.path.join(TEMPLATE_FOLDER, "template_atom.xml")

# Paramètres
MAX_IMAGE_WIDTH = 625

# ============================================================================
# ÉTAPE 1 : REDIMENSIONNEMENT DES IMAGES
# ============================================================================

def resize_images():
    """Redimensionne toutes les images à une largeur maximale"""
    print("\n=== REDIMENSIONNEMENT DES IMAGES ===")
    
    if not os.path.exists(IMAGES_FOLDER):
        print(f"⚠️ Dossier {IMAGES_FOLDER} introuvable. Étape ignorée.")
        return
    
    files = os.listdir(IMAGES_FOLDER)
    images_resized = 0
    
    for file in files:
        file_path = os.path.join(IMAGES_FOLDER, file)
        
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                
                if width > MAX_IMAGE_WIDTH:
                    new_height = int((MAX_IMAGE_WIDTH / width) * height)
                    img_resized = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
                    img_resized.save(file_path)
                    print(f'✅ "{file}" redimensionnée à {MAX_IMAGE_WIDTH}x{new_height}')
                    images_resized += 1
        except IOError:
            # Ce n'est pas une image, on ignore
            pass
    
    print(f"✅ {images_resized} image(s) redimensionnée(s)")

# ============================================================================
# ÉTAPE 2 : CONVERSION MARKDOWN → HTML
# ============================================================================

def convert_md_to_html():
    """Convertit tous les fichiers .md en .html"""
    print("\n=== CONVERSION MARKDOWN → HTML ===")
    
    # Vérifier que les dossiers existent
    if not os.path.exists(MD_FOLDER):
        print(f"❌ Dossier {MD_FOLDER} introuvable")
        return
    
    if not os.path.exists(TEMPLATE_ARTICLE):
        print(f"❌ Template {TEMPLATE_ARTICLE} introuvable")
        return
    
    # Créer le dossier HTML s'il n'existe pas
    os.makedirs(HTML_FOLDER, exist_ok=True)
    
    # Créer le dossier content_MD s'il n'existe pas
    content_md_folder = os.path.join(MD_FOLDER, "content_MD")
    os.makedirs(content_md_folder, exist_ok=True)
    
    # Lire le template
    with open(TEMPLATE_ARTICLE, "r", encoding="utf-8") as file:
        template_content = file.read()
    
    # Convertir chaque fichier .md
    md_files = [f for f in os.listdir(MD_FOLDER) if f.endswith(".md")]
    
    if not md_files:
        print("⚠️ Aucun fichier .md trouvé")
        return
    
    for md_file in md_files:
        md_file_path = os.path.join(MD_FOLDER, md_file)
        
        try:
            # Lire le contenu du fichier Markdown
            with open(md_file_path, "r", encoding="utf-8") as file:
                md_content = file.readlines()
            
            # Extraire titre, contenu et hashtag
            title = md_content[0].strip()
            html_content = markdown2.markdown("".join(md_content[2:-1]))
            hashtag = md_content[-1].strip()
            
            # Nom du fichier HTML
            html_file_name = md_file.replace('.md', '.html')
            
            # Remplacer les balises dans le template
            final_content = template_content.replace("$CONTENT", html_content)
            final_content = final_content.replace("$TITLE", title)
            date_today = datetime.now().strftime("%Y-%m-%d")
            final_content = final_content.replace("$date_of_the_day", date_today)
            final_content = final_content.replace("$HTMLLINK", html_file_name)
            final_content = final_content.replace("$HASHTAG", hashtag)
            
            # Écrire le fichier HTML
            html_path = os.path.join(HTML_FOLDER, html_file_name)
            with open(html_path, "w", encoding="utf-8") as file:
                file.write(final_content)
            
            # Déplacer le fichier .md
            dest_path = os.path.join(content_md_folder, md_file)
            os.rename(md_file_path, dest_path)
            
            print(f'✅ {md_file} → {html_file_name}')
            
        except Exception as e:
            print(f'❌ Erreur avec {md_file}: {e}')
    
    print(f"✅ Conversion terminée : {len(md_files)} fichier(s)")

# ============================================================================
# ÉTAPE 3 : GÉNÉRATION DE BLOG.HTML ET INDEX.HTML
# ============================================================================

def generate_blog_and_index():
    """Génère les pages blog.html et index.html"""
    print("\n=== GÉNÉRATION BLOG.HTML ET INDEX.HTML ===")
    
    if not os.path.exists(HTML_FOLDER):
        print(f"❌ Dossier {HTML_FOLDER} introuvable")
        return
    
    # Liste pour stocker les articles avec leurs dates
    items_with_dates = []
    
    # Parcourir les fichiers HTML
    for filename in os.listdir(HTML_FOLDER):
        if filename.startswith("2026") and filename.endswith(".html"):
            file_path = os.path.join(HTML_FOLDER, filename)
            
            try:
                # Date de modification
                mod_time = os.path.getmtime(file_path)
                
                # Extraire le titre
                with open(file_path, 'r', encoding='utf-8') as file:
                    contents = file.read()
                    soup = bs4.BeautifulSoup(contents, 'html.parser')
                    h1_text = soup.find('h1').text.strip()
                
                # Créer l'élément de liste (avec filename et titre pour index.html)
                list_item = f'<li>{filename[:10]} - <a href="fr/{filename}">{h1_text}</a></li>'
                items_with_dates.append((mod_time, list_item, filename, h1_text))
                
            except Exception as e:
                print(f'⚠️ Erreur avec {filename}: {e}')
    
    # Trier par date (plus récent en premier)
    items_with_dates.sort(reverse=True, key=lambda x: x[0])
    html_list_str = '\n'.join([item[1] for item in items_with_dates])
    
    # Générer blog.html
    try:
        with open(TEMPLATE_BLOG, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        new_content = template_content.replace('$LISTE_POST', html_list_str)
        
        blog_path = os.path.join(BASE_PATH, "blog.html")
        with open(blog_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"✅ blog.html créé avec {len(items_with_dates)} article(s)")
    except Exception as e:
        print(f"❌ Erreur création blog.html: {e}")
    
    # Générer index.html
    try:
        with open(TEMPLATE_INDEX, 'r', encoding='utf-8') as file:
            template_index_content = file.read()
        
        # Prendre uniquement le dernier article (le plus récent)
        if items_with_dates:
            last_filename = items_with_dates[0][2]
            last_title = items_with_dates[0][3]
            last_post_html = f'<p><a href="fr/{last_filename}">{last_title}</a></p>'
        else:
            last_post_html = ''
        
        # Date du jour au format YYYY-MM-DD
        date_maj = datetime.now().strftime("%Y-%m-%d")
        
        # Remplacer les placeholders
        new_index_content = template_index_content.replace('$Last_post', last_post_html)
        new_index_content = new_index_content.replace('$Date_maj', date_maj)
        
        index_path = os.path.join(BASE_PATH, "index.html")
        with open(index_path, 'w', encoding='utf-8') as file:
            file.write(new_index_content)
        
        print(f"✅ index.html créé avec le dernier article")
    except Exception as e:
        print(f"❌ Erreur création index.html: {e}")


# ============================================================================
# ÉTAPE 4 : GÉNÉRATION DU FLUX ATOM.XML
# ============================================================================

def generate_atom_feed():
    """Génère le flux RSS/Atom"""
    print("\n=== GÉNÉRATION FLUX ATOM ===")
    
    # Créer le dossier XML s'il n'existe pas
    os.makedirs(XML_FOLDER, exist_ok=True)
    
    # Supprimer l'ancien atom.xml
    atom_xml_path = os.path.join(BASE_PATH, "atom.xml")
    if os.path.exists(atom_xml_path):
        os.remove(atom_xml_path)
    
    # Partie 1 : Créer les fichiers entry
    if not os.path.exists(TEMPLATE_ENTRY):
        print(f"❌ Template {TEMPLATE_ENTRY} introuvable")
        return
    
    with open(TEMPLATE_ENTRY, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()
    
    entry_count = 0
    for html_file in os.listdir(HTML_FOLDER):
        if html_file.endswith(".html"):
            html_file_path = os.path.join(HTML_FOLDER, html_file)
            
            try:
                with open(html_file_path, "r", encoding="utf-8") as html_content:
                    html_content = html_content.read()
                    soup = bs4.BeautifulSoup(html_content, "html.parser")
                    
                    h1_content = soup.find("h1").text.strip()
                    article_element = soup.find("article")
                    article_content = article_element.prettify() if article_element else ""
                    
                    date_update = datetime.fromtimestamp(
                        os.path.getmtime(html_file_path)
                    ).astimezone(tz.UTC).isoformat()
                    
                    xml_content = template_content.replace("$H1", h1_content)\
                                                   .replace("$HTML_LINK", html_file)\
                                                   .replace("$DATE_UPDATE", date_update)\
                                                   .replace("$CONTEN_HTML", article_content)
                    
                    xml_file_path = os.path.join(XML_FOLDER, html_file.replace(".html", ".xml"))
                    with open(xml_file_path, "w", encoding="utf-8") as xml_file:
                        xml_file.write(xml_content)
                    
                    entry_count += 1
            except Exception as e:
                print(f"⚠️ Erreur avec {html_file}: {e}")
    
    print(f"✅ {entry_count} fichier(s) entry créé(s)")
    
    # Partie 2 : Créer bloc.xml
    xml_files = sorted(os.listdir(XML_FOLDER), reverse=True)
    bloc_xml_path = os.path.join(XML_FOLDER, "bloc.xml")
    
    with open(bloc_xml_path, "w", encoding="utf-8") as bloc_xml_file:
        for xml_file in xml_files:
            if xml_file != "bloc.xml":
                with open(os.path.join(XML_FOLDER, xml_file), "r", encoding="utf-8") as current_xml_file:
                    bloc_xml_file.write(current_xml_file.read())
    
    print("✅ bloc.xml créé")
    
    # Partie 3 : Créer atom.xml
    with open(bloc_xml_path, "r", encoding="utf-8") as bloc_xml_file:
        bloc_xml_content = bloc_xml_file.read()
    
    bloc_xml_content = bloc_xml_content.replace("<article>", "").replace("</article>", "")
    
    with open(TEMPLATE_ATOM, "r", encoding="utf-8") as template_atom_file:
        template_content = template_atom_file.read()
    
    xml_content = template_content.replace("$CONTENT_BLOC", bloc_xml_content)
    date_updated2 = datetime.now().isoformat()
    xml_content = xml_content.replace("$DATE_Update", date_updated2)
    
    with open(atom_xml_path, "w", encoding="utf-8") as atom_xml_file:
        atom_xml_file.write(xml_content)
    
    print(f"✅ atom.xml créé : {atom_xml_path}")
    
    # Partie 4 : Nettoyer (supprimer les fichiers temporaires)
    for file_name in os.listdir(XML_FOLDER):
        if file_name != "atom.xml":
            file_path = os.path.join(XML_FOLDER, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    print("✅ Fichiers temporaires supprimés")

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Fonction principale qui exécute toutes les étapes"""
    print("=" * 60)
    print("GÉNÉRATEUR DE SITE WEB STATIQUE")
    print("=" * 60)
    print(f"Dossier de travail : {BASE_PATH}")
    
    try:
        resize_images()
        convert_md_to_html()
        generate_blog_and_index()
        generate_atom_feed()
        
        print("\n" + "=" * 60)
        print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS !")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERREUR FATALE : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()