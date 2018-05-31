from __future__ import absolute_import

import argparse
import readline
import json
import pprint

import requests

from completer import CustomCompleter

es_host = '127.0.0.1'
es_port = '9200'
es_info = {}
request_host = ''
pp = pprint.PrettyPrinter(indent=4)

support_commands = ['get', 'set', 'del', 'keys', 'info']


def check_connection():
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    try:
        response = requests.get(request_host, headers=headers)
        es_info.update(json.loads(response.text))
        print(response.text)
    except Exception as e:
        print(e)
        exit(-1)


def help_input():
    print('Commands: {}'.format(', '.join(support_commands)))


def command_get(command_list: list):
    pass


def command_del(command: str):
    pass


def command_set(command: str):
    pass


def command_keys(command: str):
    pass


def command_info():
    pp.pprint(es_info)


def command_cat(command_list: list):

    uri = '/'
    if len(command_list) > 0:
        # _cat 으로 통일하기 위해 cat 문구는 모두 삭제 하고 / 로 이어주자
        command_list.pop(0)
        uri += '/'.join(command_list)

    cat_request_uri = request_host + "/_cat" + uri
    response = request_get(cat_request_uri)

    if response.status_code != 200:
        error_res = json.loads(response.text)
        print('(error) ' + error_res.get('error').get('reason'))
        return

    print(response.text)


def request_get(uri: str):
    try:
        return requests.get(uri)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='elasticsearch host (default is http://localhost)')
    parser.add_argument('-port', help='elasticsearch port (default is 9200)')

    args = parser.parse_args()

    es_host = args.host if args.host else es_host
    es_port = args.port if args.port else es_port

    es_uri = es_host + ':' + es_port
    request_host = 'http://' + es_uri if 'http://' not in es_uri else es_uri

    completer = CustomCompleter(support_commands)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

    check_connection()
    input_text = es_uri + '> '
    while True:
        user_input = input(input_text)
        readline.add_history(user_input)

        command_split_list = user_input.split(' ')
        command_master = command_split_list[0]

        if command_master == 'exit':
            exit(1)
        elif command_master == 'help':
            help_input()
        elif command_master == 'get':
            command_get(command_split_list)
        elif command_master == 'del':
            command_del(user_input)
        elif command_master == 'set':
            command_set(user_input)
        elif command_master == 'keys':
            command_keys(user_input)
        elif command_master == 'cat':
            command_cat(command_split_list)
        elif command_master == 'info':
            command_info()
        elif command_master.replace(' ', '') == '':
            continue
        else:
            print("(error) ERR unknown command '" + user_input + "'")



