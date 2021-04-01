#! /usr/bin/env python
# -*- coding: utf-8 -*-

from http.server import HTTPServer, CGIHTTPRequestHandler
import configparser
import cgi

config = configparser.ConfigParser()
config.read("config.ini")
server_address = ("", int(config["Server"]["port"]))
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()
