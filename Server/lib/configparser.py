#!/usr/bin/env python3

import configparser

def parseConfig(filename):
	config = configparser.ConfigParser()
	config.read(filename)

	server = config['Server']
	port = config['Port']

	return server['serverName'], port['port']
