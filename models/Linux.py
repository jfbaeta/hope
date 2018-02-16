# -*- coding: UTF-8 -*-

import os, re, subprocess

class Linux(object):
	'''
	Class used to check Operating System distribution, version and other settings.
	'''
	def __init__(self, index='', lvname='', size='', name=''):
		super(Linux, self).__init__()

	reg_exps = [
		re.compile(r'(?:^NAME=")(.*)(?:")'),\
		re.compile(r'(?:^VERSION=")(.*)(?:")'),\
		re.compile(r'(?:^PRETTY_NAME=")(.*)(?:")')
		]

	@property
	def distribution(self):
		'''
		Method to verify Operating System distribution.
		'''
		with open('/etc/os-release', 'r') as os_release_file:

			os_name = re.findall(self.reg_exps[0], os_release_file.read())

		return os_name

	@property
	def version(self):
		'''
		Method to verify Operating System version.
		'''
		with open('/etc/os-release', 'r') as os_release_file:

			os_version = re.findall(self.reg_exps[1], os_release_file.read())

		return os_version

	@property
	def name(self):
		'''
		Method to verify Operating System pretty name.
		'''
		with open('/etc/os-release', 'r') as os_release_file:

			os_pretty_name = re.findall(self.reg_exps[2], os_release_file.read())

		return os_pretty_name