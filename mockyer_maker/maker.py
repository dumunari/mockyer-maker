import json
import os
import urllib.parse
import hashlib

with open('your_simulation.json', 'r') as f:
    _json = json.load(f)

    for x in _json['data']['pairs']:
        if x['request']:
            request_value = x['request']['path'][0]['value'].replace('/', '-')[1:]
            request_method = x['request']['method'][0]['value'].lower()
            if request_method == 'get':
                request_query = list(x['request']['query'].keys())[0]
                if len(request_value + '?' + urllib.parse.quote(request_query, safe='')) > 225:
                    full_request = request_value + '?' + hashlib.sha1(('?' + urllib.parse.quote(request_query, safe=''))
                                                                      .encode('utf-8')).hexdigest()
                else:
                    full_request = request_value + '?' + urllib.parse.quote(request_query, safe='')
            else:
                full_request = request_value
            full_directory_path = os.getcwd() + '/' + os.path.splitext(f.name)[0] + '/' + f'{full_request}' + f'/{request_method}'
            if not os.path.isdir(full_directory_path):
                os.makedirs(full_directory_path)

        if x['response']:
            filename = 0

            if os.path.isfile(full_directory_path + '/' + str(filename) + '.content'):
                with open(full_directory_path + '/' + str(filename + 1) + '.content', 'w') as n:
                    n.write(x['response']['body'])
            else:
                with open(full_directory_path + '/0.content', 'w') as n:
                    n.write(x['response']['body'])

            if os.path.isfile(full_directory_path + '/' + str(filename) + '.json'):
                with open(full_directory_path + '/' + str(filename + 1) + '.json', 'w') as h:
                    json.dump({
                        "status": x['response']['status'],
                        "headers": {
                            "accept": "text/html,application/xhtml+xml,application/xml,text/xml;q=0.9,*/*;q=0.8",
                            "accept-charset": "utf-8",
                            "content-type": "text/xml; charset=utf-8",
                            "connection": "close"
                        }
                    }, h)
            else:
                with open(full_directory_path + '/0.json', 'w') as h:
                    json.dump({
                        "status": x['response']['status'],
                        "headers": {
                            "accept": "text/html,application/xhtml+xml,application/xml,text/xml;q=0.9,*/*;q=0.8",
                            "accept-charset": "utf-8",
                            "content-type": "text/xml; charset=utf-8",
                            "connection": "close"
                        }
                    }, h)