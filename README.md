# Conversify-lite
Conversify-lite is a lighter version of Conversify without the talking-face generation. This application allows the user to converse with a chatbot, whose personality and voice can be declared, via speech.

#

### Cloning the repository

--> Clone the repository using the command below :
```bash
git clone https://github.com/amauriciogonzalez/Conversify-lite.git

```

--> Move into the directory where we have the project files : 
```bash
cd Conversify-lite

```

--> Create a virtual environment :
```bash
# If you are on Windows
virtualenv env
# If you are on Linux or Mac
python -m venv env
```

--> Activate the virtual environment :
```bash
# If you are on Windows
.\env\Scripts\activate
# If you are on Linux or Mac
source env/bin/activate
```

--> Install the requirements :
```bash
pip install -r requirements.txt
```

--> Create a config.json file :
```bash
{
    "CAI_data": [
        {
            "token": "",
            "character": ""
        }
    ],
    "EL_data": [
        {
            "EL_key":  "",
            "voice": ""
        }

    ]
}
```

--> Access config.json to add ElevenLabs and CharacterAI keys :

Obtaining an ElevenLabs key:
  1. Access the ElevenLabs website: https://beta.elevenlabs.io/
  2. Click on Profile Settings on the top-right side of the page
  3. Copy the ElevenLabs api key

Obtaining a CharacterAI key (token):
  1. Log in on character.ai: https://beta.character.ai/
  2. Go to Network tab in DevTools and refresh page
  3. Search /dj-rest-auth/auth0/
  4. Copy the key value under Network

#

### Running the App

--> To run the App, we use :
```bash
python app.py
# Running the app with CharacterAI and ElevenLabs 
python app.py --ttt cai --tts el
```

#
