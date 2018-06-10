# -*-coding:utf-8-*-

from __future__ import absolute_import
import argparse
import readline
import json
import sys

from termcolor import cprint

import requests

try:
    from src.client.completer import CustomCompleter
except ImportError:
    from client.completer import CustomCompleter


es_host = '127.0.0.1'
es_port = '9200'
es_info = {}
request_host = ''

support_commands = ['get', 'del', 'delete_by_query', 'info', 'cat', 'match_all', 'match', 'analyze']


def help_input():
    print('Commands: {}'.format(', '.join(support_commands)))


def check_connection():
    global es_info

    uri = '/'
    response = _request_get(uri)
    if response.status_code != 200:
        cprint('(error) invalid host', color='red')
        sys.exit(-1)
    print(response.text)

    es_info.update(json.loads(response.text))


def command_info():
    print(json.dumps(es_info, indent=4))


def command_get(command_list: list):

    uri = '/'
    if len(command_list) > 0:
        command_list.pop(0)
        uri += '/'.join(command_list)

    response = _request_get(uri)
    _response_print(response)


def command_del(command_list: list):

    if len(command_list) < 2:
        cprint('(error) invalid request. Use > del {index} {type:Optional} {id:Optional}', color='red')
        return

    command_list.pop(0)
    index = command_list.pop(0)

    uri = '/' + index + '/' + '/'.join(command_list)

    response = _request_delete(uri)
    _response_print(response)


def delete_by_query(command_list: list):

    if len(command_list) < 4:
        cprint('(error) invalid request. Use > delete_by_query {index} {document} {value}', color='red')
        return

    command = command_list.pop(0)  # delete_by_query command
    index = command_list.pop(0)

    document = command_list.pop(0)
    value = command_list.pop(0)

    data = {
        'query': {
            'match': {
                document: value
            }
        }
    }

    uri = '/' + index + '/_' + command
    response = _request_post(uri, data=data)
    _response_print(response)


def match_all(command_list: list):

    if len(command_list) < 2:
        cprint('(error) invalid request Use > match_all {index} {from:optional} {size:optional}', color='red')
        return

    index = command_list[1]

    _from, _size = 0, 50
    if len(command_list) > 2:
        _from = command_list[2]
    if len(command_list) > 3:
        _size = command_list[3]

    data = {
        'query': {
            'match_all': {}
        },
        'from': _from,
        'size': _size
    }

    uri = '/' + index + '/_search'
    response = _request_get(uri, data=data)
    _response_print(response)


def match(command_list: list):

    if len(command_list) < 4:
        cprint('(error) invalid request Use > match {index} {document} {value}', color='red')
        return

    command_list.pop(0)  # match keyword
    index = command_list.pop(0)  # index

    document = command_list.pop(0)
    value = command_list.pop(0)

    data = {
        'query': {
            'match': {
                document: {
                    'query': value
                }
            }
        }
    }

    uri = '/' + index + '/_search'
    response = _request_get(uri, data=data)
    _response_print(response)


def command_cat(command_list: list):

    uri = '/_cat'
    command_list.pop(0)  # cat command

    uri += '/'.join(command_list)

    response = _request_get(uri)
    _response_print(response)


def analyze(command_list: list):

    if len(command_list) < 3:
        cprint('(error) invalid request Use > analyze {analyzer} {text}', color='red')
        return

    command_list.pop(0)  # analyze command
    analyzer = command_list.pop(0)
    text = command_list.pop(0)

    data = {
        'analyzer': analyzer,
        'text': text
    }

    uri = '/_analyze'
    response = _request_post(uri, data=data)
    _response_print(response)


def _response_print(response: requests.Response):

    color = 'white'
    if response.status_code != 200:
        color = 'red'

    try:
        text = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
    except json.JSONDecodeError:
        text = response.text

    cprint(text=text, color=color)


class CustomResponse(requests.Response):

    def __init__(self):
        super().__init__()
        self.custom_message = ''

    @property
    def text(self):
        return self.custom_message


def _request_get(uri: str, **kwargs):
    request_uri = request_host + uri
    data = kwargs.get('data', {})
    print('uri : ', request_uri, ', data : ', data)

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    try:
        return requests.get(request_uri, data=json.dumps(data), headers=headers)
    except Exception as e:
        res = CustomResponse()
        res.status_code = 500
        res.custom_message = e
        return res


def _request_delete(uri: str):
    request_uri = request_host + uri

    try:
        return requests.delete(request_uri)
    except Exception as e:
        res = CustomResponse()
        res.status_code = 500
        res.custom_message = e
        return res


def _request_post(uri: str, **kwargs):
    request_uri = request_host + uri
    data = kwargs.get('data', {})

    headers = {'Content-Type': 'application/json; charset=utf-8'}

    try:
        return requests.post(request_uri, data=json.dumps(data), headers=headers)
    except Exception as e:
        res = CustomResponse()
        res.status_code = 500
        res.custom_message = e
        return res


def main():
    global es_host, es_port, request_host

    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='elasticsearch host (default is http://localhost)')
    parser.add_argument('-port', help='elasticsearch port (default is 9200)')

    args = parser.parse_args()

    es_host = args.host if args.host else es_host
    es_port = args.port if args.port else es_port

    es_uri = (es_host + ':' + es_port).replace('http://', '')
    request_host = 'http://' + es_uri

    completer = CustomCompleter(support_commands)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

    check_connection()
    input_text = es_uri + '> '
    while True:
        try:
            user_input = input(input_text).lstrip()
            readline.add_history(user_input)

            command_split_list = user_input.split(' ')
            command_master = command_split_list[0]

            if command_master == 'exit':
                sys.exit(1)
            elif command_master == 'help':
                help_input()
            elif command_master == 'get':
                command_get(command_split_list)
            elif command_master == 'del':
                command_del(command_split_list)
            elif command_master == 'delete_by_query':
                delete_by_query(command_split_list)
            elif command_master == 'cat':
                command_cat(command_split_list)
            elif command_master == 'info':
                command_info()
            elif command_master == 'match_all':
                match_all(command_split_list)
            elif command_master == 'match':
                match(command_split_list)
            elif command_master == 'analyze':
                analyze(command_split_list)
            elif command_master.replace(' ', '') == '':
                continue
            else:
                print("(error) ERR unknown command '" + user_input + "'")

        except KeyboardInterrupt:
            print('thank you!')
            sys.exit(0)




