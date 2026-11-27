---
title: adoq QDA : un petit logiciel libre pour apprendre le codage qualitatif (et une expérience avec l'IA)
date: 2026-11-27
update: 2026-11-27
lang: fr
description: adoq QDA : un petit logiciel libre pour apprendre le codage qualitatif (et une expérience avec l'IA)
slug: 2026-11-27-adoq-qda-un-petit-logiciel-libre-pour-apprendre-le-codage-qualitatif
translation: 2026-11-27-adoq-qda-a-small-free-tool-for-learning-qualitative-coding
tags:
  - QDA
  - App
  - IA
  - adoq-QDA
reading_time: 6
---

Je mets aujourd'hui en ligne **adoq QDA**, un logiciel libre d'analyse de données qualitatives. « adoq » reprend les initiales d'*analyse de données qualitatives*, QDA dit la même chose en anglais (*qualitative data analysis*), et le logo est un petit poisson dont les écailles sont des lignes de texte surlignées... comme des passages codés.

![Le petit poisson qui sert de logo a adoq QAD](https://gregoirelits.eu/files/optimized/logoaqoqqda.png)

C'est un outil conçu d'abord pour **apprendre** le codage qualitatif : pour les étudiant·es qui découvrent l'analyse d'entretiens ou veulent réaliser un travail ou leur mémoire en analyse qualitative, et pour les enseignant·es qui les accompagnent. C'est aussi, et je le dis d'emblée, le résultat d'une expérimentation sur l'usage de l'IA dans la recherche qualitative. J'y reviens plus bas.

- Le code source de l'application : [github.com/MiiL-UCLouvain/adoqQDA](https://github.com/MiiL-UCLouvain/adoqQDA)
- Le manuel et le téléchargement : [https://gregoirelits.eu/app/adoq-qda/](https://gregoirelits.eu/app/adoq-qda/)
- Essayer l'app en ligne : [https://gregoirelits.eu/app/adoq-qda/adoq-QDA-0.4.3.html](https://gregoirelits.eu/app/adoq-qda/adoq-QDA-0.4.3.html)

## Qu'est-ce que ça fait ?

Tout le logiciel tient dans **un seul fichier HTML** (qui contient environ 2500 lignes de javaScript). Un double-clic l'ouvre dans le navigateur : rien à installer, pas de serveur, pas de cloud, pas de compte, travail hors ligne, ce qui est essentiel si on souhaite qu'une centaine d'étudiante.s équipés d'ordinateurs et de compétences informatiques divers puissent directement utiliser l'app.  Important aussi, aucune donnée ne quitte l'ordinateur. Quand on travaille sur des entretiens, ce n'est pas un détail.

On y retrouve les gestes de base du codage qualitatif :

- importer des entretiens (.txt, .docx, ou un corpus au format Iramuteq) ;
- sélectionner un passage et lui attribuer un ou plusieurs codes, avec des chevauchements possibles ;
- construire un arbre de codes, le réorganiser, fusionner ou scinder des codes, rédiger définitions et mémos ;
- distinguer les locuteurs (intervieweur·euse, répondant·e, participant·es d'un focus group) ;
- exporter les extraits par code, un livre de codes, des tableaux pour un tableur ou SPSS.

![Capture d'écran d'adoq QDA](https://gregoirelits.eu/files/optimized/screen-adoq-qda.png)

Et quelques fonctions plus directement pédagogiques : un **journal de l'arbre de codes**, tenu automatiquement, qui garde la trace de chaque création, fusion ou suppression (avec son motif) ; un **verrou** de l'arbre, pour passer d'une phase exploratoire à une phase de codage systématique ; le **travail à deux ou en groupe** (fusion des copies, kappa de Cohen, codage de consensus) ; et une **vue enseignant** pour suivre le travail de tout un groupe. Bref, ce qu'on demande d'habitude d'expliciter dans un chapitre méthodologique, l'outil aide à le documenter en cours de route.

adoq QDA n'est pas pensé pour de grands corpus traités par des équipes de recherche professionnelles, et il laisse volontairement de côté le travail simultané, les droits d'accès, l'audio et la vidéo ou les requêtes avancées. Mais il est suffisamment robuste (je pense, les premiers tests en situation réelle permettront de le montrer) pour analyser plusieurs dizaines d'entretiens. 

## Un format ouvert, lisible par un humain

La grande différence d'adoq QDA avec les autres logiciels libre d'anlayse qualitative est le format de données sur lequel il repose. Un projet adoq QDA est un simple **fichier texte** (`.qda.md`), lisible dans n'importe quel éditeur ou dans Obsidian. Le texte des entretiens n'est jamais modifié : le codage est écrit en clair sous chaque paragraphe, par exemple :

```
> [!codage]-
> - #defiance #dependance-politique @gl : « à la solde des politiciens »
```

Les données ne sont donc pas enfermées dans un logiciel : on peut les relire, les corriger à la main, les archiver, et les rouvrir dans dix ans sans se demander si l'éditeur existe encore. Ce format, baptisé **qda.md**, est la base de l'app et permet la vérification du travail de codage par un humain (sans utilisation de logiciel) et la manipulation des données par software d'analyse . Je l'ai décrit dans un working paper : Lits, G. (2026). *qda.md : un format ouvert, lisible et pérenne pour les données qualitatives codées* (Working paper du MiiL 1). [hdl.handle.net/2078.5/282719](https://hdl.handle.net/2078.5/282719). La spécification est sur [github.com/MiiL-UCLouvain/qdamd-format](https://github.com/MiiL-UCLouvain/qdamd-format).

Le logiciel est distribué sous licence **EUPL-1.2**.

## Une expérimentation sur l'IA et la recherche qualitative

En 2024, je racontais ici comment j'avais demandé à ChatGPT d'écrire les scripts Python qui génèrent ce site, et je me demandais s'il était [encore utile d'apprendre à coder](https://gregoirelits.eu/fr/2024-04-16-Apprendre-a-coder.html). Ma réponse était oui : sans compréhension du code, on devient dépendant de l'outil, et ce sont nos connaissances préalables qui permettent de lui poser les bonnes questions.

adoq QDA pousse l'expérience beaucoup plus loin. Le logiciel (et sa version de recherche, QDA-md, qui intègre notamment le codage abductif et l'analyse de la saturation) a été développé en un peu plus d'un mois, entièrement en dialogue avec un modèle d'IA, Claude (Opus 5.5 effort modéré). Je n'ai pas écrit moi-même les lignes de JavaScript (je n'en serais pas capable actuellement).

Ce que j'ai fait, en revanche : définir le format qda.md, décider de ce que l'outil devait faire et surtout de ce qu'il ne devait pas faire, exiger des tests (un fichier ouvert puis enregistré doit rester identique à l'octet près), commander un audit de sécurité, essayer l'outil sur de vrais corpus, et trancher, version après version. Autrement dit, l'expertise ne disparaît pas : elle se déplace de l'écriture du code vers sa spécification et sa vérification. Et cette expertise-là, c'est largement celle du chercheur en méthodes qualitatives, pas celle du développeur.

Faut-il donc toujours apprendre à coder ? Je maintiens que oui... mais peut-être plus tant pour écrire du code (quoique si le logiciel se diffuse, j'imagine mal que le code ne soit pas revu par un humain à un moment) que pour savoir quoi demander et être capable de juger ce qu'on obtient. Je reste aussi conscient d'un petit paradoxe, qui fait écho à ce que j'écrivais sur [l'IA et la dispersion des expertises](https://gregoirelits.eu/fr/2025-06-17-IA-et-dispersion-des-expertises.html) : j'ai utilisé une banque centralisée d'expertise pour construire un outil dont le principe est justement que les données restent chez soi, dans un format que personne ne contrôle. Quant à savoir si ce code vieillira bien... aucune idée, et c'est précisément pour ça que le format, lui, a été pensé pour survivre au logiciel.

## Tout retour est le bienvenu

adoq QDA en est à sa version 0.4.3 et est encore un prototype fonctionnel. C'est jeune, et c'est précisément le moment où les retours sont les plus utiles. Si vous êtes enseignant·e, étudiant·e ou chercheur·e et que vous l'essayez, n'hésitez pas à me dire ce qui coince, ce qui n'est pas clair, ce qui manque, ou comment vous l'utilisez en cours. Vous pouvez ouvrir une *issue* sur [le dépôt GitHub](https://github.com/MiiL-UCLouvain/adoqQDA) ou simplement m'écrire.

Déclaration sur l'usage de l'IA : ce post a été rédigé et édité avec l'aide de Claude (modèle Opus 5.5)
