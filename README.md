# Slack My Documents
Ein simpler Slackbot, der es erlaubt, mit den Daten der eigenen Dokumente zu sprechen.


## Start

### Slack-Konfiguration

Zunächst braucht unser kleiner Bot einen Zugriff auf Slack. Dazu nutzen wir das Bolt-Framework in Python, das von Slack selbst zur Verfügung gestellt wird, 
Bitte folgen Sie der Anleitung unter https://slack.dev/bolt-python/tutorial/getting-started, um einen SLACK_BOT_TOKEN und einen SLACK_APP_TOKEN zu erhalten. Der SLACK_BOT_TOKEN sollte mit xoxb-... beginnen, der SLACK_APP_TOKEN mit xapp-... .

### OpenAI-Key

Bitte legen Sie sich einen OpenAI-Account an und holen Sie sich unter https://platform.openai.com/account/api-keys einen API-Key. 

### Installation

In der aktuellen Fassung kann der Bot von überall aus gestartet und genutzt werden, denn er nutzt die WebSocket-API von Slack. Es ist also auch ein Betrieb vom lokalen Netzwerk aus möglich, eine öffentliche API ist nicht erforderlich. 

```
git clone https://github.com/mayflower/slack_my_documents
cd slack_my_documents

conda create -n slackbot python=3.10.9
conda activate slackbot

pip install -r requirements.txt 
```

### Konfiguration

Bitte kopieren Sie die Datei .env.example, um eine eigene Konfiguration anzulegen:
```
cp .env.example .env
```

Tragen Sie jetzt bitte die 3 Werte von oben in die .env ein, und ergänzen Sie das Keyword, auf das der Bot hören soll.

```
# cp .env.example .env
# Edit your .env file with your own values
# DON'T COMMIT OR PUSH .env FILE!

# API CONFIG
OPENAI_API_KEY=
OPENAI_API_MODEL=gpt-3.5-turbo # Options: gpt-4, gpt-4-32k, gpt-3.5-turbo, text-davinci-003, etc.
SLACK_BOT_TOKEN= # Slack Bot token from , "xoxb-..."
SLACK_BOT_KEYWORD= # Slack Bot keyword - when should be answer?
SLACK_APP_TOKEN= # Slack App token from , "xapp-..."```

### Daten importieren 

Der Bot unterstützt im Moment folgende Formate: 

* Word-Dokumente (.docx, .doc)
* Powerpoint (.pptx, .ppt)
* Mails (.eml, .msg)
* Ebooks (.rtf, .epub)
* HTML-Seiten (.html)
* Acrobat Reader (.pdf)
* MarkDown (.md)
* Text (.txt)
* Text in Grafiken (.png, .jpg) 


Bitte kopieren Sie alle benötigten Dateien einfach in den Folder ./data.

Starten Sie danach den Importer:

```
python import.py
```
Bitte nutzen Sie dieses Script auch, wenn Sie Ihre Daten aktualisieren wollen - und starten Sie danach den Bot neu, damit er mit den aktuellen Daten arbeitet.

## Start
Jetzt können Sie den Bot starten:
```
python app.py 
```

# Hinweise 
## Datenschutz
In dieser Version nutzt der Bot nicht nur Slack, sondern auch OpenAI. Und auch wenn die Dokumente lokale persistiert werden, und nur bei Bedarf ausgewählte Inhalte weitergegeben werden, so läuft transferiert man trotzdem zwangsläufig eigene Daten an Unternehmen wie Slack, OpenAI oder Microsoft. Prüfen Sie daher bitte im Vorfeld ihre Compliance-Rahmenbedingungen.

## Beispieldokument
Als Beispiel wird [“Soziokratie 3.0 - Ein Praxisleitfaden”](https://sociocracy30.org/_res/practical-guide/S3-Praxisleitfaden.pdf) von Bernhard Bockelbrink, James Priest und Liliana David mitgeliefert, unter Creative Commons Attribution-ShareAlike 4.0 International Lizenz.