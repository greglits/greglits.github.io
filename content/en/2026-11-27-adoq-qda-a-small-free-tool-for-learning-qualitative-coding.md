---
title: adoq QDA: a small free tool for learning qualitative coding (and an experiment with AI)
date: 2026-11-27
update: 2026-11-27
lang: en
description: adoq QDA: a small free tool for learning qualitative coding (and an experiment with AI)
slug: 2026-11-27-adoq-qda-a-small-free-tool-for-learning-qualitative-coding
translation: 2026-11-27-adoq-qda-un-petit-logiciel-libre-pour-apprendre-le-codage-qualitatif
tags:
  - QDA
  - App
  - AI
  - adoq-QDA
reading_time: 6
---

Today I am releasing **adoq QDA**, a free and open-source tool for qualitative data analysis. "adoq" comes from the French initials of *analyse de données qualitatives*, QDA says the same thing in English (*qualitative data analysis*), and the logo is a small fish whose scales are highlighted lines of text... just like coded passages.

![The small fish that serves as the adoq QDA logo](https://gregoirelits.eu/files/optimized/logoaqoqqda.png)

It is a tool designed first and foremost for **learning** qualitative coding: for students who are discovering interview analysis or who want to carry out a project or their master's thesis using qualitative analysis, and for the teachers who support them. It is also, and I'll say it right away, the result of an experiment on the use of AI in qualitative research. More on that below.

- The application's source code: [github.com/MiiL-UCLouvain/adoqQDA](https://github.com/MiiL-UCLouvain/adoqQDA)
- Manual and download: [https://gregoirelits.eu/app/adoq-qda/](https://gregoirelits.eu/app/adoq-qda/)
- Try the app online: [https://gregoirelits.eu/app/adoq-qda/adoq-QDA-0.4.3.html](https://gregoirelits.eu/app/adoq-qda/adoq-QDA-0.4.3.html)

## What does it do?

The whole software fits into **a single HTML file** (containing about 2,500 lines of JavaScript). A double-click opens it in the browser: nothing to install, no server, no cloud, no account, and it works offline. This is essential if a hundred or so students, with all sorts of computers and very different levels of computer skills, are to be able to use the app straight away. Just as important, no data ever leaves the computer. When you are working with interviews, that is not a minor detail.

It covers the basic moves of qualitative coding:

- importing interviews (.txt, .docx, or a corpus in Iramuteq format);
- selecting a passage and assigning it one or more codes, with overlaps allowed;
- building a code tree, reorganising it, merging or splitting codes, writing definitions and memos;
- distinguishing speakers (interviewer, respondent, focus group participants);
- exporting excerpts by code, a codebook, and tables for a spreadsheet or SPSS.

![Screenshot of adoq QDA](https://gregoirelits.eu/files/optimized/screen-adoq-qda.png)

It also offers a few more explicitly teaching-oriented features: a **code tree log**, kept automatically, which records every creation, merge or deletion (along with the reason for it); a **lock** on the code tree, to move from an exploratory phase to a phase of systematic coding; **working in pairs or in groups** (merging copies, Cohen's kappa, consensus coding); and a **teacher view** for following the work of a whole class. In short, what we usually ask students to make explicit in a methods chapter, the tool helps them document as they go.

adoq QDA is not designed for large corpora handled by professional research teams, and it deliberately leaves out simultaneous work, access rights, audio and video, and advanced queries. But it is robust enough (I think; the first tests in real conditions will tell) to analyse several dozen interviews.

## An open format, readable by humans

What really sets adoq QDA apart from other free qualitative analysis software is the data format it relies on. An adoq QDA project is a simple **text file** (`.qda.md`), readable in any text editor or in Obsidian. The interview text is never modified: the coding is written in plain text under each paragraph, for example:

```
> [!codage]-
> - #defiance #dependance-politique @gl : « à la solde des politiciens »
```

So the data are not locked inside a piece of software: you can reread them, correct them by hand, archive them, and reopen them in ten years' time without wondering whether the vendor still exists. This format, called **qda.md**, is the foundation of the app. It allows a human to check the coding work (without any software) and analysis software to process the data. I have described it in a working paper: Lits, G. (2026). *qda.md : un format ouvert, lisible et pérenne pour les données qualitatives codées* (MiiL Working Paper 1). [hdl.handle.net/2078.5/282719](https://hdl.handle.net/2078.5/282719). The specification is available at [github.com/MiiL-UCLouvain/qdamd-format](https://github.com/MiiL-UCLouvain/qdamd-format).

The software is released under the **EUPL-1.2** licence.

## An experiment on AI and qualitative research

In 2024, I described here how I had asked ChatGPT to write the Python scripts that generate this website, and I wondered whether it was [still worth learning to code](https://gregoirelits.eu/fr/2024-04-16-Apprendre-a-coder.html) (in French). My answer was yes: without understanding the code, you become dependent on the tool, and it is your prior knowledge that lets you ask it the right questions.

adoq QDA takes that experiment much further. The software (and its research version, QDA-md, which notably supports abductive coding and saturation analysis) was developed in a little over a month, entirely in dialogue with an AI model, Claude (Opus 5.5, medium effort). I did not write the JavaScript myself (I wouldn't be able to at this point).

What I did do: define the qda.md format, decide what the tool should do and, above all, what it should not do, insist on tests (a file opened and then saved must remain identical, byte for byte), commission a security audit, try the tool on real corpora, and make the calls, version after version. In other words, expertise does not disappear: it shifts from writing code to specifying and checking it. And that expertise is largely that of the qualitative methods researcher, not that of the developer.

So is it still worth learning to code? I still think so... but perhaps less for writing code (although if the software spreads, I can hardly imagine the code not being reviewed by a human at some point) than for knowing what to ask for and being able to judge what you get. I am also aware of a small paradox, which echoes what I wrote about [AI and the dispersion of expertise](https://gregoirelits.eu/en/2025-06-17-AI-and-the-Dispersion-of-Expertise.html) : I used a centralised bank of expertise to build a tool whose whole principle is that data stay with you, in a format that nobody controls. As for whether this code will age well... no idea, and that is precisely why the format, at least, was designed to outlive the software.

## All feedback is welcome

adoq QDA is at version 0.4.3 and is still a working prototype. It is young, and this is exactly when feedback is most useful. If you are a teacher, student or researcher and you try it out, don't hesitate to tell me what gets stuck, what is unclear, what is missing, or how you use it in your teaching. You can open an *issue* on [the GitHub repository](https://github.com/MiiL-UCLouvain/adoqQDA) or simply write to me.

**AI use statement:** this post was written and edited with the help of Claude (Opus 5.5 model).