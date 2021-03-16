from telethon import TelegramClient
import time
from telethon import sync, events
from json2table import convert
import requests
import json
import array
from datetime import datetime
import re
import io
import emoji

api_id = 3048536
api_hash = "d6b47c422a9818ab4e54241d15a33f09"
session = "VirusTotalBot"

client = TelegramClient(session, api_id, api_hash)
client.start()


def main():
    while True:
        print("Scan...")
        now = datetime.now()
        print("start at: ", now)
        check_ip()
        time.sleep(3)

    # print("timer dosent not start")


def check_ip():
    headers = {
        'x-apikey': 'e12923396923694b1679496f24026334f922d98047788777f1c13223f6dc0d90',
    }

    lastmsg = client.get_messages('shodanresponse_bot')
    ip_addr_list = re.findall("\d+.\d+.\d+.\d+", lastmsg[0].text)

    ip_addr_for_vtotal = ip_addr_list[0]

    with open("newscan.txt") as f:
        now = ip_addr_for_vtotal
        if now in f.read():
            print(f"IP arleady in file.({now})")
            return None
        else:
            with open("newscan.txt", "a") as ad:
                ad.write(now + '\n')

    ip = ip_addr_for_vtotal
    r = requests.get('https://www.virustotal.com/api/v3/search?query=' + "185.62.188.30", headers=headers)  # curl get запрос
    json_data = r.json()  # делает вместо кода респонса,жсон ответ

    result_json = json.dumps(json_data, indent=5)  # делает норм вид жсона, чисто для вида
    tmp_arr = []
    root = json_data['data'][0]['attributes']
    for i in root['last_analysis_stats']:
        if root['last_analysis_stats']['malicious'] != 0:
            print('malv:'+str(root['last_analysis_stats']['malicious']))
            time.sleep(2)
            prntres(json_data, ip)
        if root['last_analysis_stats']['suspicious'] != 0:
            print('malv:'+str(root['last_analysis_stats']['suspicious']))
            time.sleep(2)
            prntres(json_data, ip)
        else:
            pass


            #tmp = i + ":" + str(root['last_analysis_stats'][i])
            #tmp_arr.append(tmp)



def prntres(json_d, ip):
    tmp_arr = []
    repoort = []
    root = json_d['data'][0]['attributes']
    for i in root['last_analysis_stats']:
        if root['last_analysis_stats'][i] != 0:
            tmp = i + ":" + str(root['last_analysis_stats'][i])
            tmp_arr.append(tmp)
    for i in root['last_analysis_results']:
        if str(root['last_analysis_results'][i]['result']) == "clean":
            print("Undetectd")
        else:
            Engine_name = emoji.emojize(":construction_worker: ")+"**" + root['last_analysis_results'][i]["engine_name"] + "**" + "\n"
            repoort.append(Engine_name)
            Result = "Result: " + root['last_analysis_results'][i]['result'] + "\n \n"
            repoort.append(Result)

        # Category = "Category: " + root['last_analysis_results'][i]["category"]+"\n"
        # repoort.append(Category)


    str1 = ""
    for i in repoort:
        str1 += i

    arr = tmp_arr
    rep = ""
    str_rating = ""
    #smiles
    for i in arr:
        if i.startswith("harmless"):
            rep += emoji.emojize(":hatching_chick: "+i+"\n")

        if i.startswith("malicious"):
            rep += emoji.emojize(":fire: "+i+"\n")
            str_rating += i
        if i.startswith("suspicious"):
            rep += emoji.emojize(":japanese_goblin: "+i+"\n")
            str_rating += i
        if i.startswith("undetected"):
            rep += emoji.emojize(":clown_face: "+i+"\n")

        else:
            pass


    #get rating
    temp_arr_rate = re.findall('\d+', str_rating)
    try:
        rate = int(temp_arr_rate[0]) + int(temp_arr_rate[1])
    except IndexError:
        rate = int(temp_arr_rate[0])

    rating_to_message = ""

    if rate <= 2:
        rating_to_message += emoji.emojize(":star:")
    if rate <= 5 and rate > 2:
        rating_to_message += emoji.emojize(":star:") + emoji.emojize(":star:")
    if rate <= 7 and rate > 5:
        rating_to_message += emoji.emojize(":star:") + emoji.emojize(":star:") + emoji.emojize(":star:")
    if rate > 7:
        rating_to_message += emoji.emojize(":star:") + emoji.emojize(":star:") + emoji.emojize(":star:") + emoji.emojize(":star:") + emoji.emojize(":star:")

    now = datetime.now()
    dt_string = emoji.emojize(":alarm_clock: ") + now.strftime("%d/%m/%Y %H:%M:%S")
    ip_str = emoji.emojize(":black_flag: ") + ip
    mag = emoji.emojize(":man_detective: ")


    client.send_message("https://t.me/virtot",dt_string+"\n \n"+ ip_str+"\n \n"+"Malware rating: \n" + rating_to_message +"\n \n"+ rep +"\n"+ mag+"**AV Details: **\n" + "\n" + str1)
    print(rating_to_message)
    print("Scan done! Check Public")


"""#########################################################################################################"""
"""#############################################START#######################################################"""
"""#########################################################################################################"""

main()
