---
title: Sur le code qui génère ce site / Est-il encore utile d'apprendre à coder ?
date: 2024-04-16
update: 2024-04-16
lang: fr
description: Résultat d'une expérience de codage assisté par IA.
slug: 2024-04-16-Apprendre-a-coder
translation: 
tags:
  - IA
  - codage
reading_time: 4
---



Sur le code qui génère ce site / Est-il encore utile d'apprendre à coder ?

 Dans un souci de sobriété numérique, j'ai construit ce blog en reprenant le template de [Ploum.net](https://ploum.net/) (merci à lui pour le partage !). Ce site est donc un site statique composé uniquement de pages simples écrites au langage HTML (le contenu n'est pas stocké dans une base de données et affiché sur une page web grâce à un script, le site n'utilise pas de PHP, pas de JavaScript, ce qui limite les ressources utilisées pour son affichage). 

Dans un premier temps, je voulais continuer de rédiger et coder en html l'ensemble des pages "à la main".  Je rédigeais les postes du blog dans un éditeur de texte markdown (Obsidian ou Zetllr en fonction de mon humeur du moment), puis je convertissais ce texte au format html grâce à un [convertisseur disponible en ligne](https://markdowntohtml.com/). Une fois cela réalisé, il me suffisait d'intégrer manuellement mon texte codé en html dans mon template de post de blog réalisé au préalable, puis d'ajouter dans la page d'accueil (index.html) du site et dans la page blog.html une ligne de code avec le lien vers le nouveau post. 

J'aime faire cela à la main car cela me donne un sentiment de maitrise technique et de simplicité. De plus ça ne prend vraiment pas beaucoup de temps (quelques minutes tout au plus). 

Par contre, le processus est un peu répétitif et très clairement, il pourrait être automatisé facilement. Autre problème, je voulais que mon site soit doté d'un flux RSS (qui est [ici](https://gregoirelits.eu/atom.xml)) et coder un flux RSS à la main est, après expérience, quelque chose d'assez fastidieux, pas sûr d'avoir envie de consacrer du temps à cela...

# Apprendre à coder en python ?

Mais pour automatiser ce processus (convertir le texte en html. Intégrer le texte dans le template d'un post de blog. Modifier la page d'accueil du site et celle du blog, et surtout créer le flux RSS), il faut savoir coder dans un langage de programmation tel que Python.

Le problème, c'est que malgré le fait que j'ai inscrit "apprendre à coder en python" sur ma *to-do list* depuis au moins 5 ans, je n'ai jamais pris le temps de m'y mettre. Il serait bien possible de reprendre des scriptes existants et de les adapter, mais même cela est au-dessus de mes capacités à ce stade. 

C'est là que les IA génératives entrent en jeu. Et si je demandais à ChatGPT de réaliser ce code pour moi ? 

C'est ce que j'ai fait. Je lui ai d'abord demandé de réaliser un script en python permettant de créer le fichier atom.rss de mon blog. En gros lui demandant d'aller visiter le dossier contenant l'ensemble des fichiers HTML qui composent le blog du site, de classer les pages dans l'ordre chronologique, puis d'écrire un fichier intitulé atom.xml qui reprend la liste des articles de manière lisible par un lecteur de flux RSS. 

Je lui ai aussi demandé que ce scripte puisse fonctionner sur [Google Collab](https://colab.research.google.com/), un service de Google qui permet d'exécuter du code en python.

À ma grande surprise, après une petite heure d'allers-retours avec ChatGPT (surtout pour résoudre un problème lié à la manière dont le script Python pouvait accéder aux fichiers de mon blog stockés sur Google Drive), j'avais un code qui fonctionnait et qui en un clic générait un fichier RSS fonctionnel (même si clairement pas parfait.)

# Et si j'automatisais l'ensemble du blog ?

Vu la rapidité du processus, j'ai poussé l'expérience plus loin. Je me suis plongé dans le code source du blog de [Ploum.net](https://git.sr.ht/~lioploum/ploum.net/tree/master/item/publish.py) pour voir l'ensemble des étapes qu'il réalise et j'ai tenté de répliquer toutes ces étapes avec des scriptes séparés permettant de : 

- réduire la largeur des images du site, présentes dans le dossier /files du blog à maximum 600px. 
- de convertir mon texte rédigé au format markdown en une page HTML utilisant un template préexistant.
- d'éditer les pages index.html et blog.html pour les mettre à jour et intégrer le lien vers le nouveau post de blog créé. 
- de créer le flux RSS. 
- d'exporter sur mon ordinateur depuis Google Drive les quatre nouveaux fichiers créés : index.html, blog.html, nouveau-post.html et atom.rss. 

Au final, il m'aura fallu à peu près quatre heures de travail pour avoir quatre scriptes en python réalisant l'ensemble de ces tâches (dont au moins deux heures pour faire trois versions du script du flux RSS pour qu'il soit de plus en plus simple). 

Le workflow de ce site est maintenant le suivant : 

- Rédiger l'article du blog en markdown sur Obsidian. 
- Enregistrer le fichier .md dans un dossier particulier de mon Google Drive. 
- Ouvrir le Google Collab où j'ai placé ces quatre scriptes en Python.
- Faire fonctionner les scripts pour obtenir directement les quartes fichiers (le post de blog au format html, la page d'accueil du site mise à jour, la page blog mise à jour et le fichier atom.rss pour le flux rss)
- Importer ces quartes fichiers sur le site (hébergé sur Github). 

Il reste quelques petites choses que je pourrais corriger dans le script qui crée le fichier atom.rss, mais à part cela, l'ensemble fonctionne très bien.

# Quelques réflexions suite à cette expérience

- Cette expérience est assez perturbante et précisément, ce qui est perturbant, c'est que si je comprends globalement les grandes lignes de ce qu'il y a dans les codes, je suis bien incapable de comprendre pourquoi et comment ça fonctionne et que lorsque cela bug, souvent je ne comprends pas pourquoi... 

- Ce qui est très étonnant également est que chatGPT en plus d'avoir fabriqué le code que je voulais a spontanément adopté une démarche pédagogique avec moi.  En me proposant le code, il m'explique presque ligne par ligne (sans doute a-t-il déduit mon niveau d'incompétence en interprétant la *prompt* que je lui ai soumise) ce que fait le code. Quand je souhaite avoir plus de détail sur une ligne, je lui demande de m'expliquer ce qu'elle fait et il me l'explique clairement. Quand quelque chose ne marche pas, il est également capable très rapidement d'identifier le problème et de m'expliquer pourquoi ça ne marche pas.

- Ce processus m'a au final permis d'apprendre très rapidement beaucoup de choses sur la manière dont un code en python fonctionne, beaucoup de choses dont je n'avais presque aucune connaissance avant cela. 

-  Si j'ai pu réaliser cela, c'est cependant par ce que j'avais déjà quelques connaissances. Je comprends bien comment fonctionne un ordinateur (j'ai encore connu les ordinateurs fonctionnant sous DOS ou tout se passait dans le terminal). Je sais donc ce qu'est un chemin d'accès d'un fichier. Je sais aussi c'est qu'est le XML ou le HTML. Je comprends bien comment fonctionne un site web et sais coder de manière basique en HTML et CSS. J'ai également quelques petites bases en programmation acquises durant mes études de sociologie (un peu de SQL, un peu de SAS et de SPSS) et de programmation orientée objet (en gros je savais ce qu'était un IDE, un objet et un package), ayant suivi il y a quelques années un cours d'introduction au langage R. Je savais donc comment rédiger des prompts qui  permettent à l'IA de comprendre ce dont j'avais besoin en la guidant étape par étape. Le fait de reproduire les étapes du code source du blog de Ploum m'a également largement facilité la tâche évidement. 

# Est-il donc encore utile d'apprendre à coder ?

Cet exercice me renvoie à ma *to-do list*. Devrais-je y garder la ligne "apprendre le python" ? De manière plus générale, cela rejoint des débats que nous avons avec quelques collègues sur une réforme des programmes du bac en communication que nous sommes en train de mener. Devrions-nous inclure dans la formation de Bac en communication et information un cours de programmation à ce langage ?? 

Ma réponse est oui, cela reste intéressant, ne fut-ce que parce que la génération de code sans compréhension par l'IA nous rend complètement dépendants de l'outil, mais surtout parce que si je n'avais pas eu cette connaissance et expérience préalable en informatique (fonctionnement d'un ordinateur, qu'est ce qu'un fichier .txt, comment fonctionne un site web, comment coder en HTML, base générale de programmation, etc.) je n'aurais pas su construire des prompts efficaces.

Cela étant dit, et cela a été la surprise de l'exercice, l'utilisation d'une IA générative pour réaliser un premier projet en Python s'est révélée pour moi une très bonne aide à l'apprentissage.  Parce qu'elle fonctionne de manière assez didactique, mais aussi parce que j'ai pu lui poser au fil du projet toutes les questions qui me passaient par la tête (ce qui n'est par exemple pas le cas sur les plateformes d'auto-apprentissage comme CodeAcademy). 

# Une dernière interrogation...

Les scripts que j'ai rédigés avec ChatGPT sont ici. 

- script de production des pages HTML : [publish.py](https://github.com/greglits/greglits.github.io/blob/main/script/publish.py)
- script de création du flux RSS : [RSS.py](https://github.com/greglits/greglits.github.io/blob/main/script/RSS.py)

Je suis parfaitement incapable de savoir s'il s'agit de "bons" scripts ou non. Vont-ils durer dans le temps ou boguer dans deux semaines ? Aucune idée... Si des spécialistes veulent y jeter un œil, je suis preneur :-)

# Quelques ressources intéressantes 

- [A.I.'s Original Sin](https://www.nytimes.com/2024/04/16/podcasts/the-daily/ai-data.html?rref=vanity) (podcast du NYT, 16 avril 2024). Enquête sur les données qui ont servi à entrainer les IA Gen. Explique notamment comment Open AI à créé Whisper pour convertir en texte des millions d'heures de vidéo YouTube en texte pour entrainer GPT (en scrappant de manière sans doute illégale le contenu de YouTube)

 #code #python