# -*-coding:utf-8-*-

from __future__ import absolute_import

try:
    from src.client import client
except ImportError:
    from client import client


if __name__ == '__main__':
    client.main()
