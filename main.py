import random
import requests
import json

#list of all slot values
slot_values = {
    "cherry": 2,
    "lemon": 3,
    "orange": 4,
    "plum": 5,
    "bell": 6
}

slot_emojis = {
    "cherry": "🍒",
    "lemon": "🍋",
    "orange": "🍊",
    "plum": "🍑",
    "bell": "🔔"
}

headers = {
    "authorization": "Enter token here"
}

channelid = "Enter channel id here"

slot = []

def translate_slot() -> str:
    display = ""
    for i in range(0, 3, 1):
        display += slot_emojis[slot[i]] + " "
    display = display.strip()
    return display

#check for multiplier and return value
def check_slot() -> int:
    base_value = 0
    multiplier = 0
    max_count = 0

    for i in range(0, 3, 1):
        base_value += slot_values[slot[i]]
    for i in range(0, 3, 1):
        compare = slot[i]
        count = slot.count(compare)
        if count > max_count and count != 1:
            max_count = count
            multiplier = count

    if max_count == 3:
        multiplier = 7
        
    print(f"value: {base_value} multiplier: {multiplier}")
    value = base_value*multiplier
    return value
            
def retrieve_messages(channelid) -> list:
    list_of_messages = []
    r = requests.get(f"https://discord.com/api/v9/channels/{channelid}/messages", headers=headers)
    jsonn = json.loads(r.text)
    for value in jsonn:
        list_of_messages.append(value['content'])
    return list_of_messages[0]

#generates the slot values
def rand_slot() -> list[str]:
    choice = None 
    for i in range(0, 3, 1):
        choice = random.choice(list(slot_values.keys()))
        slot.append(choice)
    return slot

def send_message(channelid):
    rand_slot()
    payload = {
        "content": f"{translate_slot()} \nSCORE: {check_slot()}"
    }
    requests.post(url=f"https://discord.com/api/v9/channels/{channelid}/messages", data=payload, headers=headers)

if __name__ == "__main__":
    while True:
        slot_result = retrieve_messages(channelid=channelid)
        if slot_result == "/spin":
            send_message(channelid=channelid)
            slot = []
        