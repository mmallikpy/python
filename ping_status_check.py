# ------------Script goal----------
# Script will ping a remote host, every time it will ping 20 times and calculate the pcketloss. If it faild to ping 5 or more than 5 then it will trigared a message in telegram.
# Tested on Ubuntu
# Required library subprocess, requests
# Telegram with a bot.

import subprocess
import requests

base_url = "https://api.telegram.org/bot--Your API Key--"

def send_message(replay_chat):
    print(replay_chat)
    parameters = {
        "chat_id": "-876xxxxxx",
        "text": replay_chat,
    }
    requests.get(base_url + "/sendMessage", data=parameters)
    requests.ReadTimeout()

    
while True:
    try:

        # Run the command
        command_output = subprocess.check_output("ping -c 20 9.9.9.9 | grep -E '^[0-9]+ packets transmitted'", shell=True)
        # Convert bytes to string
        command_output = command_output.decode("utf-8")
        # Print the output
        command_output = str(command_output)
        parameater = command_output.split(',')
        total_send_packet = int(parameater[0].split(" ")[0])
        total_received_packet = int(parameater[1].split(" ")[1])
        lost_packet_percent = parameater[2].split(" ")[1]
        latency = parameater[3].split(" ")[2]

        failed_packet = total_send_packet - total_received_packet

        if failed_packet >= 5:
            #print("Total packet loss \t:-",failed_packet)
            #print("Lost packet  by percent :-",lost_packet_percent)
            #print("Latency \t\t:-",latency)
            output = f"------DC-DR-Network------\nTotal packet loss:- {failed_packet}\nLost packet  by percent :- {lost_packet_percent}\nLatency:- {latency}"
            
            send_message(output)
        else:
            print("No Packet loss found....!!")
    except Exception as e:
        print("An error occurred : ", e)

