"""
 Lexbot Lambda handler.
 """
import requests
import json
from difflib import SequenceMatcher

API_Token = 'secret key'
database_id='database ID'
url = ('https://api.notion.com/v1/databases/{}/query'.format(database_id))
districts =['Achham','Arghakhachi','Baglung','Baitadi','Bajhang','Bajura','Banke','Bara','Bardiya','Bhaktapur','Bhojpur','Chitwan','Dadeldhura','Dailekh','Dang','Darchula','Dhading','Dhankuta','Dhanusa','Dolakha','Dolpa','Doti','East Nawalparasi','East Rukum','Gorkha','Gulmi','Humla','Ilam','Jajarkot','Jhapa','Jumla','Kabhrepalanchok','Kailali','Kalikot','Kanchanpur','Kapilvastu','Kaski','Kathmandu','Khotang','Lalitpur','Lamjung','Mahottari','Makwanpur','Manang','Morang','Mugu','Mustang','Myagdi','Nawalparasi','Nuwakot','Okhaldhunga','Palpa','Panchthar','Parbat','Parsa','Pyuthan','Ramechhap','Rasuwa','Rautahat','Rolpa','Rukum','Rupandehi','Salyan','Saptari','Sarlahi','Shankhuwasabha','Sindhuli','Sindhupalchowk','Siraha','Solukhumbu','Sunsari','Surkhet','Syangja','Tanahu','Taplejung','Terhathum','Udayapur','West Rukum']

#return corresponding district for list districts that matches with input.
def search_district(district_name):
    if district_name in districts:
        district = district_name
        print("Exact match with {}".format(district_name))
        return district
        #if district name is not a match to key, applies sequence match to find closest match e.g. if there is a typo
    else:
        for item in districts:
            similarity = SequenceMatcher(None, item.lower(), district_name.lower())
            if similarity.ratio() > 0.8:
                district = item
                print("{} matches with {}".format(district_name, district))
                return district

def get_mp_in_district(district):
    payload = {
        "filter": {
            "property": "District",
            "rich_text": {
                "equals": district
            }
        }
    }
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": API_Token
    }


    print('Getting MP in {}'.format(district))
    api_request = requests.post(url, json=payload, headers=headers)
    response_data = api_request.json()
    dict_of_mp_inDistrict = {}
    for item in response_data['results']:
        serialNumber = item['properties']['SerialNumber']['number']
        name = item['properties']['Name']['title'][0]['text']['content']
        party = item['properties']['PoliticalParty']['rich_text'][0]['text']['content']
        phone = item['properties']['Mobile']['phone_number']
        email = item['properties']['Email']['email']
        mp_detail = [name,party,phone,email]
        dict_of_mp_inDistrict[serialNumber] = '{} - {}'.format(mp_detail[0], mp_detail[1])
    return dict_of_mp_inDistrict

    

def lambda_handler(event, context):
    print('received request: ' + str(event))
    district_input = event['currentIntent']['slots']['np_district']
    member_of_parliament = get_mp_in_district(search_district(district_input.lower()))
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "SSML",
                "content": "".join([" ({0}) {1} \n".format(key, value) for (key, value) in member_of_parliament.items()])
                    
            },
        }
    }
    print('result = ' + str(response))
    return response
