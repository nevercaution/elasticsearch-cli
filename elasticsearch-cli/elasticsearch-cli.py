from __future__ import absolute_import

import argparse
import readline

import requests

from completer import CustomCompleter

es_host = '127.0.0.1'
es_port = '9200'


support_commands = ['get', 'set', 'del', 'keys']


def check_connection():
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    es_uri = es_host + ':' + es_port
    request_host = 'http://' + es_uri if 'http://' not in es_uri else es_uri
    try:
        response = requests.get(request_host, headers=headers)
        print(response.text)
    except Exception as e:
        print(e)
        exit(-1)


def help_input():
    print('Commands: {}'.format(', '.join(support_commands)))


def command_get(command: str):
    command_list = split_command(command)

    if not command_list:
        return

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    es_uri = es_host + ':' + es_port



def command_del(command: str):
    pass


def command_set(command: str):
    pass


def command_keys(command: str):
    command_list = split_command(command)

    if not command_list:
        return



def split_command(command: str):
    command_list = command.split(' ')

    if len(command_list) == 1:
        print("(error) ERR wrong number of arguments for 'get' command")
        return None

    return command_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='elasticsearch host (default is http://localhost)')
    parser.add_argument('-port', help='elasticsearch port (default is 9200)')

    args = parser.parse_args()

    es_host = args.host if args.host else es_host
    es_port = args.port if args.port else es_port

    completer = CustomCompleter(support_commands)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

    check_connection()
    input_text = es_host.replace('http://', '') + ':' + es_port + '> '
    while True:
        user_input = input(input_text)
        readline.add_history(user_input)

        if user_input == 'exit':
            exit(1)
        elif user_input == 'help':
            help_input()
        elif 'get' in user_input:
            command_get(user_input)
        elif 'del' in user_input:
            command_del(user_input)
        elif 'set' in user_input:
            command_set(user_input)
        elif 'keys' in user_input:
            command_keys(user_input)



