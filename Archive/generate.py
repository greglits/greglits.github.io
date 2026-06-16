#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de site statique bilingue (FR/EN).

Workflow :
  1. Écrire l'article en Markdown dans Obsidian, avec un front-matter YAML.
  2. Déposer le .md dans content/fr/ ou content/en/.
  3. Lancer ce script.

Il produit : les pages d'articles, index.html, blog.html (par langue)
et atom.xml — sans toucher aux sources.

Dépendance unique : markdown2. (pip install markdown2)
"""

import os
import re
import html
import shutil
from datetime import datetime, timezone

import markdown2
from PIL import Image

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

CONTENT_DIR   = os.path.join(BASE_PATH, "content")     # sources .md, par langue
TEMPLATE_DIR  = os.path.join(BASE_PATH, "templates")
IMAGES_DIR    = os.path.join(BASE_PATH, "files")        # images sources
IMAGES_OUT    = os.path.join(IMAGES_DIR, "optimized")   # images redimensionnées
OUT_DIRS      = {"fr": os.path.join(BASE_PATH, "fr"),
                 "en": os.path.join(BASE_PATH, "en")}

SITE_URL      = "https://gregoirelits.eu"
MAX_IMG_WIDTH = 625
LANGS         = ("fr", "en")

# Libellés dépendant de la langue (un seul endroit pour les traduire)
I18N = {
    "fr": {
        "role":        "Sociologue des médias et du numérique · UCLouvain",
        "skip":        "Aller au contenu",
        "lang_nav":    "Langue",
        "nav_label":   "Navigation principale",
        "post_nav_label": "Navigation entre billets",
        "foot_about":  "À propos de ce site",
        "updated":     "Dernière mise à jour",
        "post_updated": "Mis à jour le",
        "read_unit":   "min de lecture",
        "prev":        "← Billet précédent",
        "next":        "Billet suivant →",
        "og_locale":   "fr_FR",
        "nav": [("recherche.html", "Recherches"), ("publications.html", "Publications"),
                ("cours.html", "Enseignements"), ("blog.html", "Blog"),
                ("press.html", "Presse"), ("about.html", "À propos")],
        "months": ["", "janvier", "février", "mars", "avril", "mai", "juin",
                   "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
    },
    "en": {
        "role":        "Media and digital sociologist · UCLouvain",
        "skip":        "Skip to content",
        "lang_nav":    "Language",
        "nav_label":   "Main navigation",
        "post_nav_label": "Post navigation",
        "foot_about":  "About this site",
        "updated":     "Last updated",
        "post_updated": "Updated on",
        "read_unit":   "min read",
        "prev":        "← Previous post",
        "next":        "Next post →",
        "og_locale":   "en_US",
        "nav": [("recherche.html", "Research"), ("publications.html", "Publications"),
                ("cours.html", "Teaching"), ("blog.html", "Blog"),
                ("press.html", "Press"), ("about.html", "About")],
        "months": ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"],
    },
}

# ============================================================================
# OUTILS
# ============================================================================

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def fill(template, mapping):
    """
    Remplace les $CLÉ par leur valeur.
    Les clés sont traitées de la plus longue à la plus courte : sans cela,
    $LANG remplacerait le début de $LANG_TOGGLE. Indispensable avec str.replace.
    """
    out = template
    for key in sorted(mapping, key=len, reverse=True):
        value = mapping[key]
        out = out.replace("$" + key, value if value is not None else "")
    return out


# ============================================================================
# FRONT-MATTER : parseur YAML minimal (clé: valeur, et listes [a, b])
# ============================================================================

def parse_front_matter(raw):
    """
    Sépare un fichier .md en (métadonnées, corps Markdown).
    Le front-matter est délimité par deux lignes '---'.
    Gère :
      - 'clé: valeur'
      - listes inline      'tags: [a, b, c]'
      - listes multi-ligne 'tags:' puis '  - a' (format écrit par Obsidian)
    Rien de plus — volontairement.
    """
    if not raw.startswith("---"):
        raise ValueError("Front-matter manquant (le fichier doit commencer par '---').")

    _, fm, body = raw.split("---", 2)
    meta = {}
    current_list_key = None          # clé dont on accumule les éléments '- ...'
    for raw_line in fm.strip().splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Élément d'une liste multi-ligne : '- valeur'
        if stripped.startswith("- "):
            if current_list_key is None:
                raise ValueError(f"Élément de liste sans clé parente : {stripped!r}")
            meta[current_list_key].append(stripped[2:].strip())
            continue

        if ":" not in stripped:
            raise ValueError(f"Ligne de front-matter invalide : {stripped!r}")

        key, _, value = stripped.partition(":")
        key, value = key.strip(), value.strip()

        if value == "":
            # 'tags:' seul → début possible d'une liste multi-ligne
            meta[key] = []
            current_list_key = key
        elif value.startswith("[") and value.endswith("]"):
            meta[key] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
            current_list_key = None
        else:
            # Obsidian entoure parfois les valeurs de guillemets : on les retire.
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            meta[key] = value
            current_list_key = None

    return meta, body.strip()


def require(meta, key, path):
    if key not in meta or meta[key] == "":
        raise ValueError(f"Métadonnée '{key}' manquante dans {os.path.basename(path)}")
    return meta[key]


# ============================================================================
# CHARGEMENT DES ARTICLES
# ============================================================================

def load_posts():
    """Lit tous les .md de content/<lang>/ et retourne un dict {lang: [post, ...]}."""
    posts = {lang: [] for lang in LANGS}
    for lang in LANGS:
        src = os.path.join(CONTENT_DIR, lang)
        if not os.path.isdir(src):
            continue
        for name in os.listdir(src):
            if not name.endswith(".md"):
                continue
            path = os.path.join(src, name)
            meta, body = parse_front_matter(read(path))

            slug = meta.get("slug") or name[:-3]
            date_str = require(meta, "date", path)          # AAAA-MM-JJ
            date = datetime.strptime(date_str, "%Y-%m-%d")

            # Date de mise à jour : optionnelle. Si absente, le billet n'affiche
            # rien. Si présente, elle doit être >= à la date de publication.
            updated_str = meta.get("update", "").strip()
            updated = None
            if updated_str:
                updated = datetime.strptime(updated_str, "%Y-%m-%d")
                if updated < date:
                    raise ValueError(
                        f"'update' ({updated_str}) antérieure à 'date' ({date_str}) "
                        f"dans {os.path.basename(path)}")

            posts[lang].append({
                "lang":        lang,
                "slug":        slug,
                "title":       require(meta, "title", path),
                "description": meta.get("description", ""),
                "date":        date,
                "date_str":    date_str,
                "updated":     updated,                       # datetime ou None
                "updated_str": updated_str,                   # "" si absent
                "translation": meta.get("translation", ""),  # slug du pendant
                "reading":     meta.get("reading_time", ""),
                "body_html":   markdown2.markdown(body),
                "mtime":       os.path.getmtime(path),
            })
        # Tri antéchronologique sur la date de PUBLICATION (donnée, pas mtime)
        posts[lang].sort(key=lambda p: p["date"], reverse=True)
    return posts


def warn_missing_translations(posts):
    """
    Avertit (sans bloquer) quand un billet déclare un champ 'translation:'
    pointant vers un slug qui n'existe dans aucun fichier de l'autre langue.
    Le lien hreflang/bascule mènerait alors vers un 404.
    """
    slugs = {lang: {p["slug"] for p in posts[lang]} for lang in LANGS}
    problems = []
    for lang in LANGS:
        other = "en" if lang == "fr" else "fr"
        for p in posts[lang]:
            target = p["translation"]
            if target and target not in slugs[other]:
                problems.append(f'   • {lang}/{p["slug"]} → {other}/{target}.html (introuvable)')
    if problems:
        print("⚠️ Traductions déclarées mais manquantes (liens vers des 404) :")
        print("\n".join(problems))
    else:
        print("✅ Toutes les traductions déclarées existent")


def fr_date(date, lang):
    """Formate une date selon la langue : '17 juin 2025' / 'June 17, 2025'."""
    months = I18N[lang]["months"]
    if lang == "fr":
        return f"{date.day} {months[date.month]} {date.year}"
    return f"{months[date.month]} {date.day}, {date.year}"


# ============================================================================
# RENDU : parties communes du base.html
# ============================================================================

def lang_toggle(lang, current_slug, translation_slug):
    """Construit la bascule FR/EN. Lien actif = langue courante."""
    other = "en" if lang == "fr" else "fr"
    cells = []
    for code in ("fr", "en"):
        if code == lang:
            cells.append(f'<a aria-current="true">{code}</a>')
        else:
            # Cible : la traduction si elle existe, sinon l'accueil de l'autre langue
            target = f"/{other}/{translation_slug}.html" if translation_slug else f"/{other}/index.html"
            cells.append(f'<a href="{target}" hreflang="{other}">{code}</a>')
    return "      " + " · ".join(cells)


def nav_links(lang):
    items = [f'    <a href="/{lang}/{href}">{label}</a>' for href, label in I18N[lang]["nav"]]
    return "\n".join(items)


def render_page(lang, slug, title, description, main, og_type,
                translation_slug="", article_meta="", updated=None, is_index=False):
    """Assemble une page complète à partir de base.html."""
    t = I18N[lang]
    other = "en" if lang == "fr" else "fr"
    canonical = f"{SITE_URL}/{lang}/{slug}.html"

    # hreflang : on n'annonce l'autre langue que si une traduction existe
    hreflang = [f'  <link rel="alternate" hreflang="{lang}" href="{canonical}">']
    if translation_slug:
        hreflang.append(f'  <link rel="alternate" hreflang="{other}" '
                        f'href="{SITE_URL}/{other}/{translation_slug}.html">')
    elif is_index:
        hreflang.append(f'  <link rel="alternate" hreflang="{other}" '
                        f'href="{SITE_URL}/{other}/index.html">')

    # og:locale:alternate seulement sur les pages réellement bilingues
    og_alt = ""
    if translation_slug or is_index:
        og_alt = f'  <meta property="og:locale:alternate" content="{I18N[other]["og_locale"]}">'

    foot_updated = ""
    if updated:
        foot_updated = f'    <p>{t["updated"]} : {updated}.</p>'

    base = read(os.path.join(TEMPLATE_DIR, "base.html"))
    return fill(base, {
        "LANG":            lang,
        "TITLE":           html.escape(title),
        "DESCRIPTION":     html.escape(description),
        "CANONICAL":       canonical,
        "HREFLANG":        "\n".join(hreflang),
        "OG_TYPE":         og_type,
        "OG_LOCALE":       t["og_locale"],
        "OG_LOCALE_ALT":   og_alt,
        "ARTICLE_META":    article_meta,
        "SKIP_LABEL":      t["skip"],
        "ROLE":            t["role"],
        "LANG_NAV_LABEL":  t["lang_nav"],
        "LANG_TOGGLE":     lang_toggle(lang, slug, translation_slug),
        "NAV_LABEL":       t["nav_label"],
        "NAV_LINKS":       nav_links(lang),
        "MAIN":            main,
        "FOOT_ABOUT":      t["foot_about"],
        "FOOT_UPDATED":    foot_updated,
    })


# ============================================================================
# GÉNÉRATION : articles
# ============================================================================

def build_articles(posts):
    article_tpl = read(os.path.join(TEMPLATE_DIR, "article.html"))
    count = 0
    for lang in LANGS:
        lst = posts[lang]
        for i, post in enumerate(lst):
            t = I18N[lang]
            # Navigation précédent/suivant (la liste est antéchronologique)
            newer = lst[i - 1] if i > 0 else None
            older = lst[i + 1] if i + 1 < len(lst) else None
            nav_bits = []
            if older:
                nav_bits.append(f'<a href="/{lang}/{older["slug"]}.html">{t["prev"]}</a>')
            if newer:
                nav_bits.append(f'<a href="/{lang}/{newer["slug"]}.html">{t["next"]}</a>')
            post_nav = ""
            if nav_bits:
                post_nav = (f'    <nav class="post-nav" aria-label="{t["post_nav_label"]}">\n'
                            f'      {"".join(nav_bits) if len(nav_bits)==1 else nav_bits[0]+chr(10)+"      "+nav_bits[1]}\n'
                            f'    </nav>')

            meta_line = fr_date(post["date"], lang)
            if post["reading"]:
                meta_line += f' · {post["reading"]} {t["read_unit"]}'

            # Mention de mise à jour, en pied d'article (vide si pas d'update).
            post_updated = ""
            if post["updated"]:
                post_updated = (f'      <p class="post-updated">'
                                f'{t["post_updated"]} {fr_date(post["updated"], lang)}.</p>')

            main = fill(article_tpl, {
                "TITLE":    html.escape(post["title"]),
                "POST_META": meta_line,
                "CONTENT":  post["body_html"].rstrip(),
                "POST_UPDATED": post_updated,
                "POST_NAV": post_nav,
            })

            article_meta = (f'  <meta property="article:published_time" content="{post["date_str"]}">\n'
                            f'  <meta property="article:author" content="Grégoire Lits">')
            if post["updated_str"]:
                article_meta += (f'\n  <meta property="article:modified_time" '
                                 f'content="{post["updated_str"]}">')

            page = render_page(
                lang, post["slug"], post["title"], post["description"], main,
                og_type="article", translation_slug=post["translation"],
                article_meta=article_meta,
            )
            write(os.path.join(OUT_DIRS[lang], post["slug"] + ".html"), page)
            count += 1
    print(f"✅ {count} article(s) généré(s)")


# ============================================================================
# GÉNÉRATION : listes (index + blog)
# ============================================================================

def post_list_items(posts, lang):
    """Liste à puces : titre + date, format compact."""
    items = []
    for p in posts:
        date = fr_date(p["date"], lang)
        items.append(
            f'      <li>\n'
            f'        <a href="/{lang}/{p["slug"]}.html">{html.escape(p["title"])}</a>\n'
            f'        <span class="meta"> — {date}</span>\n'
            f'      </li>'
        )
    return "\n".join(items)


def build_index_and_blog(posts):
    today = datetime.now().strftime("%Y-%m-%d")
    for lang in LANGS:
        latest = posts[lang][:5]   # accueil : 5 derniers
        # index.html
        index_main = fill(read(os.path.join(TEMPLATE_DIR, f"index.{lang}.html")),
                          {"LISTE_POST": post_list_items(latest, lang)})
        write(os.path.join(OUT_DIRS[lang], "index.html"),
              render_page(lang, "index", "Grégoire Lits",
                          I18N[lang]["role"], index_main,
                          og_type="website", is_index=True, updated=today))
        # blog.html
        blog_main = fill(read(os.path.join(TEMPLATE_DIR, f"blog.{lang}.html")),
                         {"LISTE_POST": post_list_items(posts[lang], lang)})
        write(os.path.join(OUT_DIRS[lang], "blog.html"),
              render_page(lang, "blog", "Blog", I18N[lang]["role"],
                          blog_main, og_type="website", is_index=True))
    print("✅ index.html et blog.html générés (fr + en)")


# ============================================================================
# GÉNÉRATION : flux Atom (un par langue)
# ============================================================================

ATOM_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="{lang}">
  <title>Grégoire Lits — Blog</title>
  <link href="{site}/{lang}/blog.html"/>
  <link rel="self" href="{site}/atom-{lang}.xml"/>
  <id>{site}/{lang}/</id>
  <updated>{updated}</updated>
  <author><name>Grégoire Lits</name></author>
{entries}
</feed>
"""

ATOM_ENTRY = """  <entry>
    <title>{title}</title>
    <link href="{site}/{lang}/{slug}.html"/>
    <id>{site}/{lang}/{slug}.html</id>
    <updated>{updated}</updated>
    <published>{published}</published>
    <summary>{summary}</summary>
    <content type="html">{content}</content>
  </entry>"""


def build_atom(posts):
    now = datetime.now(timezone.utc).isoformat()
    for lang in LANGS:
        entries = []
        for p in posts[lang]:
            published = p["date"].replace(tzinfo=timezone.utc).isoformat()
            entries.append(ATOM_ENTRY.format(
                title=html.escape(p["title"]),
                site=SITE_URL, lang=lang, slug=p["slug"],
                updated=published, published=published,
                summary=html.escape(p["description"]),
                content=html.escape(p["body_html"]),
            ))
        feed = ATOM_TEMPLATE.format(lang=lang, site=SITE_URL, updated=now,
                                    entries="\n".join(entries))
        write(os.path.join(BASE_PATH, f"atom-{lang}.xml"), feed)
    print("✅ atom-fr.xml et atom-en.xml générés")


# ============================================================================
# IMAGES : redimensionnement NON destructif (vers files/optimized/)
# ============================================================================

def resize_images():
    if not os.path.isdir(IMAGES_DIR):
        print("⚠️ Dossier files/ introuvable — étape ignorée.")
        return
    os.makedirs(IMAGES_OUT, exist_ok=True)
    done = 0
    for name in os.listdir(IMAGES_DIR):
        src = os.path.join(IMAGES_DIR, name)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(IMAGES_OUT, name)
        # Idempotent : on saute si la sortie est déjà à jour
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            continue
        try:
            with Image.open(src) as img:
                if img.width > MAX_IMG_WIDTH:
                    h = int(MAX_IMG_WIDTH / img.width * img.height)
                    img = img.resize((MAX_IMG_WIDTH, h), Image.Resampling.LANCZOS)
                img.save(dst)
                done += 1
        except (IOError, OSError):
            pass  # pas une image
    print(f"✅ {done} image(s) (re)générée(s) dans files/optimized/")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("GÉNÉRATEUR DE SITE STATIQUE BILINGUE")
    print("=" * 60)
    try:
        resize_images()
        posts = load_posts()
        print(f"   {len(posts['fr'])} billet(s) FR · {len(posts['en'])} billet(s) EN")
        warn_missing_translations(posts)
        build_articles(posts)
        build_index_and_blog(posts)
        build_atom(posts)
        print("\n✅ TERMINÉ")
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
