import json
import requests
from bs4 import BeautifulSoup

COLLEGE = 'RIT'

def read_config(filename):
    with open(filename) as json_data_file:
        data = json.load(json_data_file)
        return data

def write_config(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def get_votes(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="lxml")

    lis = soup.findAll('a')

    colleges = []

    for maintag in soup.find_all('ul', {'class': 'list-group'}):
        spans = maintag.find_all('span')
        for i, litag in enumerate(maintag.find_all('li')):
            college = {
                'name':litag.text.strip(),
                'place':i+1,
                'votes':int(spans[i+1].contents[0])
            }
            colleges.append(college)
            if college['name'] == COLLEGE:
                cur = college


    return cur, colleges

def build_message(prev, cur, colleges):
    message = ''
    if (prev['votes']-cur['votes']) >= 1:
        message += 'Heads up gang, looks like we\'ve been bot cleaned. We dropped from {} to {}, losing {} votes in the process. '.format(prev['votes'],cur['votes'], (prev['votes']-cur['votes']))

    if cur['place'] < prev['place']:
        beating = colleges[cur['place']]
        message += 'Good news!! We are are now beating {}! Currently in spot {} with {} votes and climbing! '.format(beating['name'], cur['place'], cur['votes'])
    elif cur['place'] > prev['place']:
        losing = colleges[cur['place']-2]
        message += 'Uh oh! We seem to have dropped a spot! We\'re just behind {} in spot {} with {} votes. '.format(losing['name'], cur['place'], cur['votes'])
    elif (cur['votes']-prev['votes']) >= 1:
        message += 'We\'ve gotten {} more votes, bringing us up to a total of {}! We\'re still in spot {}. '.format(cur['votes']-prev['votes'], cur['votes'], cur['place'])


    if len(message) > 0 and cur['place'] > 1:
        losing = colleges[cur['place']-2]
        message += 'Only {} more votes until we overtake {}! '.format(losing['votes']-cur['votes'], losing['name'])

    return message

def post_message(webhook_url, message):
    data = {
        "username": "WarBot",
        "avatar_url": "https://www.wikihow.com/images/f/ff/Make-a-Standing-Tiger-Out-of-Clay-Step-15.jpg",
        "content": message,
    }
    requests.post(webhook_url, data)

if __name__ == "__main__":
        config = read_config('warbot.json')
        webhook_url = config['webhook']
        url = config['url']
        prev = config['prev']
        cur, colleges = get_votes(from)

        message = build_message(prev,cur,colleges)

        if len(message) > 0:
        #    print(message)
            post_message(webhook_url, message)

        new_config = {'webhook': webhook_url,
                     'prev': cur}

        write_config('warbot.json', new_config)
