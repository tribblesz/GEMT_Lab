---
ELN version: 0.5.0
cssclass: 
  - note
  - strong-accent
  - accent-heading
date-created: 2023-06-01
author: StarDustX
note type: how-to
tags:
  - " #note/how-to  "
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```
# Obsidian ELN - Getting Started Guide

> [!Warning]
> This guide reflects the original general-purpose ELN structure and is no longer the active onboarding path for this vault.
>
> Use [[Quick Start Guide]] for the current APT/FIM workflow built around experiment series, experiment runs, specimens, instrument configurations, startup checklists, shutdown checklists, and data records.
>
> For template-specific instructions, use [[APT FIM Template Workflow]].

> [!Info] Current APT/FIM workflow
> The active workflow now uses [[Lab Log Writer]] as the main structured entry path into the vault.
>
> Before creating notes, update [[ELN Settings]] so the folder paths, gases, gauge labels, statuses, and note defaults match the instrument.
>
> Use the writer for experiment series, experiment logs, MCP image logs, ion column image logs, instrument configurations, specimens, startup checklists, shutdown checklists, daily notes, meetings, contacts, task lists, and general notes.
>
> The writer's [Resources panel](http://127.0.0.1:8765/?form=resource-library) now supports PDF intake, summarization, topic synthesis, and optional embeddings for `Resources/APT-FIM`.
>
> New intake PDFs start in `Resources/APT-FIM/PDFs`. Successful intake processing moves them to `Resources/APT-FIM/PDFs/Processed`; failed runs move them to `Resources/APT-FIM/PDFs/Failed`; extracted chunk data is stored in `Resources/APT-FIM/.index`.
>
> Provider, base URL, model, and embedding-model defaults are saved by the writer, while API keys stay only in the current browser session/local storage.

> [!Example] TOC
>   - [[#Step 1 Familiarize yourself with Obsidian]]
>   - [[#Step 2 Learn the basics of Markdown formatting]]
>   - [[#Step 3 Learn how to add metadata to your notes using YAML]]
>   - [[#Step 4 Why should you use Obsidian as ELN?]]
>   - [[#Step 5 Configure Obsidian ELN]]
>   - [[#Step 6 Obsidian ELN core structure]]
>   - [[#Step 7 ELN List Views]]
>   - [[#Step 8 Change the look of Obsidian and your notes]]
>   - [[#Step 9 Working with Literature Notes]]


## Step 1: Familiarize yourself with Obsidian

Obsidian is a powerful Markdown-based note-taking application. If you're new to Obsidian, Elisabeth Buttler's [step-by-step guide](https://elizabethbutlermd.com/obsidian-notes/) is a good place to start to familiarize yourself with its core features.

## Step 2: Learn the basics of Markdown formatting

Obsidian uses Markdown to format notes. Markdown is an easy-to-read and easy-to-learn text formatting language. It only takes a few minutes to [[Markdown Formatting Guide|learn the basic formatting rules]] and start writing your own beautifully formatted notes. 

To make the transition from traditional word processors as seamless as possible, Obsidian ELN comes pre-installed with the [Make.md](https://www.make.md) plugin. This plugin has a lot of powerful features to help you organize your notes. In addition, it helps beginners to get started with Markdown formatting by providing a formatting bar that automatically appears when you select text in your note. 

## Step 3: Learn how to add metadata to your notes using YAML

Obsidian supports adding metadata to your notes using YAML Frontmatter. Adding metadata to your notes allows you to use your notes as a database that can be easily searched using the [Dataview Plugin](https://blacksmithgu.github.io/obsidian-dataview/).

The electronic laboratory notebook (ELN) uses YAML metadata to store information about your samples, analyses, etc., and has dynamically updated tables and lists based on this metadata to give you a better overview of the information stored in your ELN. 

Like Markdown, YAML was designed to be easy for people to read and write. To familiarize yourself with YALM, I recommend reading the [YAML tutorial](https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started) by Erik Francis. 

## Step 4: Why should you use Obsidian as ELN?

Before discussing how to use Obsidian ELN, let us first consider the benefits of using Obsidian as an ELN compared to traditional paper notebooks, other note taking apps, digital word processors or even other ELN solutions.

Paper notebooks have served researches well over decades and are still extensively used today. But maybe you are already collecting your lab notes in a digital format. So why should you make the switch?

#### Benefits compared to paper notebooks


#### Benefits compared to digital note taking or word processing apps


#### Benefits compared to other ELN solutions

## Step 5: Configure Obsidian ELN

Obsidian ELN uses a YAML note file to store some basic settings of the ELN. These settings will be used by the template files and can be customized to your needs. The settings file can be found in the assets folder and is called [[ELN Settings]].

For the current APT/FIM vault, it is recommended that you review the YAML sections for folders, note defaults, experiment-series and experiment-log statuses, gases, specimen types, instrument-configuration types, and the default gauge labels for the main chamber, load lock, and ion column. The note author defined in the ELN Settings file will be automatically added to the notes created with the writer.

The operator list and gauge labels are used directly by the APT/FIM forms in [[Lab Log Writer]], so the settings should match the actual instrument readbacks and the people who will create experiment logs, image logs, and checklists.

The same settings file also controls the resource-library folders used by the writer:

- `Resources/APT-FIM/PDFs`
- `Resources/APT-FIM/Summaries`
- `Resources/APT-FIM/Topics`
- `Resources/APT-FIM/.index`

![[ELN Settings YAML.png|500]]
***Figure:** YAML section of the ELN Settings file used to configure note defaults, operators, folders, and standard APT/FIM readbacks.*

## Step 6: Obsidian ELN core structure

Obsidian ELN provides a set of smart templates to make the collection of meta data to document your research as seamless as possible.

Currently there are templates for resources, processes, projects, samples and analyses. 

##### Device And Instrument Notes

- [[Lists/Operations/Instrument Configurations|Instrument Configurations]] for machine state, interlocks, gauges, and operating defaults.
- [[Lists/Experiment/Experiment Series|Experiment Series]] for campaign planning.
- [[Lists/Experiment/Specimens|Specimens]] for physical items under test.
- [[Lists/Experiment/Experiment Logs|Experiment Logs]] for actual operating sessions.
- [[Lists/Experiment/MCP Image Logs|MCP Image Logs]] and [[Lists/Experiment/Ion Column Image Logs|Ion Column Image Logs]] for per-image metadata that links back to experiment logs.
- [[Resources/APT-FIM/Library|APT/FIM Resources]] for PDF intake, summary notes, topic syntheses, and literature indexing state.
- [[Lab Log Writer]] for the local GUI used to create current APT/FIM notes and run the resource-library workflow.

## Step 7: ELN List Views

In the section above you already got to know the list view pages for 
- [[Lists/Reference/Contacts|Contacts]]
- [[Lists/Operations/Daily Notes|Daily Notes]]
- [[Labs]]
- [[Lists/Operations/Meetings|Meetings]]
- [[Lists/Experiment/Notes|Notes]]
- [[Lists/Reference/Publications|Publications]]
- [[Resources/APT-FIM/Library|APT/FIM Resources]]

## Step 8: Change the look of Obsidian and your notes

#### Obsidian themes

#### Icon Folder Plugin 

#### Style Settings Plugin and ***cssclass*** options.

#### Note styles:
- dashboard
- research-note

#### Formatting styles:
- colored headings
- colored tables
- colored bold and italic text
- colored buttons

#### Page formatting:
- wide-view
- multi-column


## Step 9: Working with Literature Notes

Obsidian offers a plugin ([Zotero Integration](https://github.com/mgmeyers/obsidian-zotero-integration)) that links to your Zotero literature database and lets you import metadata and annotations into your Obsidian vault.

Before we start using the plugin, we should configure Zotero to use a WebDAV server to sync your literature notes and pdfs between devices, because Zotero only offers 50 MB of web space for free to store your library. This might be to low for most practical uses. You can sign up for a subscription plan to increase your quota, but if you have access to an online file server that supports WebDAV like nextcloud (e.g. bwSync&Share) you can increase your storage space for free.

### Configure Zotero to use a WebDAV server

The following description assumes that you are using a nextcloud based server. If you are using a different server the steps to obtain the WebDAV URL of you server and your user name and password to access the service may differ.

If you are using a nextcloud based service, go to the web interface of your server and log into your account. Navigate to the gear icon in the lower left corner and click it. A menu like similar to the picture below should appear. Copy the link shown in the field below WebDAV into your clipboard.

![[Pasted image 20230630131010.png|300]]

Go to your Zotero app and open the settings pane. Navigate to the sync tab and choose WebDAV from the drop-down menu shown under the file-sync section. Next copy your WebDAV link in the URL field as shown below.

![[Pasted image 20230630135306.png]]
*Note:* If necessary remove the https:// at the beginning of the URL.

Return to the web interface of your nextcloud server and create an app-password for Zotero. To do so click on your profile icon in the upper right corner and select *Settings*. Next choose *Security* on the left navigation tab. Search for the *Create new App-Password* field as shown below and enter a name for your new app-password (i.e. *zotero*) and create a new app password.
Copy the displayed user name and app password in the respective fields of your Zotero sync settings as shown above.
If you plan to multiple devices that sync to your WebDAV account you have to create an app password for each of the devices. Be aware that nextcloud displays the app password only once when you create it. If you plan to reuse the password later be sure to store the password at a save place.

![[Pasted image 20230630132519.png]]


When finished press the "check server" button on the Zotero sync settings tab to verify your WebDAV connection. If the server test is successful you are ready to use your WebDAV server for file syncing between devices. 

### Install *Better BibTex* plugin for Zotero

Before you can use the Zotero integration in Obsidian you also have to install the *Better BibTex* plugin. The download link and installation instructions for Better BibTex can be found [here](https://retorque.re/zotero-better-bibtex/installation/).

### How to use Zotero Integration in Obsidian

Import literature notes from Zotero:
1. Launch the Zotero application if its not already running
2. Back in Obsidian either click on the *Import Publication* icon in the top right corner of a note *(see image below)* or press `<Ctrl> + P` (`<Cmd> + P` on mac) to display Obsidian's command palette. Type "zotero" in the search field and select *Zotero Integration: Import Publication*
   ![[Pasted image 20230719112129.png|200]]
3. It may take a few seconds before you are redirected to the Zotero literature picker shown below
4. Type the author name or keywords of the publication you want to import and select it for the search results. Import the selected publication by pressing the enter key. 
   [![A screenshot of the Zotero search bar](https://raw.githubusercontent.com/mgmeyers/obsidian-zotero-integration/main/screenshots/03.png)](https://raw.githubusercontent.com/mgmeyers/obsidian-zotero-integration/main/screenshots/03.png)
5. After having a successfully imported the publication you can find the corresponding literature note in the folder `Literature/Publications`
 
A more detailed tutorial for using Zotero Integration will be added later. For the time being please refer to the [official plugin documentation](https://github.com/mgmeyers/obsidian-zotero-integration).

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
