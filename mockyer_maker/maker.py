import json
import os
import urllib.parse
import hashlib


def maker():
    with open('test.json', 'r') as exported_file:
        _json = json.load(exported_file)

        for captured_data_pairs in _json['data']['pairs']:
            captured_request = captured_data_pairs['request']
            if captured_request is not None:
                request_path_in_folder_format = retrieve_request_path_in_folder_format(request=captured_request)
                request_method = retrieve_request_method(request=captured_request)
                if request_method == 'get':
                    full_request = retrieve_full_request(request=captured_request,
                                                         request_path=request_path_in_folder_format)
                else:
                    full_request = request_path_in_folder_format

                full_directory_path = retrieve_full_directory_path(file=exported_file,
                                                                   full_request=full_request,
                                                                   request_method=request_method)
                if directory_doesnt_exists(directory=full_directory_path):
                    os.makedirs(full_directory_path)

            captured_response = captured_data_pairs['response']
            if captured_response is not None:

                create_content_file(full_directory_path, captured_response)
                create_json_file(full_directory_path, captured_response)


def retrieve_request_path_in_folder_format(request):
    return request['path'][0]['value'].replace('/', '-')[1:]


def retrieve_request_method(request):
    return request['method'][0]['value'].lower()


def retrieve_request_query(request):
    return list(request['query'].keys())[0]


def retrieve_encoded_request_query(request_query):
    return urllib.parse.quote(request_query, safe='')


def has_query_param(request):
    try:
        return request['query'] is not None
    except:
        return False


def request_size(request_path, request_query):
    encoded_request_query = urllib.parse.quote(request_query, safe='')
    return len(request_path + '?' + encoded_request_query)


def full_request_with_digest(request_path, request_query):
    return request_path + '?' \
           + hashlib.sha1(('?' + retrieve_encoded_request_query(request_query)).encode('utf-8')).hexdigest()


def retrieve_full_request_with_query_param(request, request_path):
    request_query = retrieve_request_query(request)
    if request_size(request_path=request_path, request_query=request_query) > 225:
        return full_request_with_digest(request_path=request_path,
                                        request_query=request_query)
    else:
        return request_path + '?' + retrieve_encoded_request_query(request_query)


def retrieve_full_request(request, request_path):
    if has_query_param(request):
        return retrieve_full_request_with_query_param(request=request,
                                                      request_path=request_path)
    else:
        return request_path


def retrieve_full_directory_path(file, full_request, request_method):
    return os.getcwd() + '/' + os.path.splitext(file.name)[0] + '/' + f'{full_request}' + f'/{request_method}'


def directory_doesnt_exists(directory):
    return not os.path.isdir(directory)


def create_content_file(full_directory_path, response):
    filename = 0
    while os.path.isfile(full_directory_path + '/' + str(filename) + '.content'):
        filename = filename + 1

    with open(full_directory_path + '/' + str(filename) + '.content', 'w') as n:
        n.write(response['body'])


def create_json_file(full_directory_path, response):
    filename = 0
    while os.path.isfile(full_directory_path + '/' + str(filename) + '.json'):
        filename = filename + 1

    with open(full_directory_path + '/' + str(filename) + '.json', 'w') as h:
        json.dump({
            "status": response['status'],
            "headers": retrieve_response_headers(response)
        }, h)


def retrieve_response_headers(response):
    return response['headers']


maker()
