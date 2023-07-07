from app import initVar
from characterai import PyCAI
import json


def initVar():
    global CAI
    global CAI_client
    global EL

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
    except:
        print("Unable to open JSON file.")
        exit()

    class CAI:
        token = data["CAI_data"][0]["token"]
        character = data["CAI_data"][0]["character"]

    if CAI.token:
        CAI_client = PyCAI(CAI.token)

    class EL:
        key = data["EL_data"][0]["EL_key"]
        voice = data["EL_data"][0]["voice"]


def main():
    initVar()

    chat = CAI_client.chat.get_chat(CAI.character)

    history_id = chat['external_id']
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    while True:
        message = input('You: ')
        print("")

        data = CAI_client.chat.send_message(
            CAI.character, message, history_external_id=history_id, tgt=tgt
        )

        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']

        print(f"{name}: {text}")
        print("")


if __name__ == '__main__':
    main()