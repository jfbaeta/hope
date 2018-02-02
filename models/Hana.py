# -*- coding: UTF-8 -*-

from string import Template
import json, os, subprocess

class Hana(object):
	'''
	Class used for SAP HANA installation.
	'''
	def __init__(self):
		super(Hana, self).__init__()

	def check_and_install_unrar(self):
		'''
		Method to check if unrar is installed.
		If it is not installed, Operating System 16-bit return code  is 256.
		It will try to install unrar through zypper, looking at enabled repos.
		'''
		if os.system('rpm -qa | grep unrar') is 256:
			print 'Package unrar is not installed. Trying to install it through zypper...'
			os.system('zypper -v -n install unrar')
		else:
			print 'Package unrar found.'

	def extract_hana_software(self):
		'''
		Method to extract SAP HANA Software.
		It uses unrar command to extract content.
		'''
		with open('/opt/hope/config/config.json', 'r') as config_file:
			config = json.load(config_file)

		for purpose_key, purpose_value in config.items():

			if purpose_key == 'hana':

				hana_software_path = purpose_value['hana_software_path']
				component_medium   = purpose_value['component_medium']

		os.system('unrar x %s/51051851_part1.exe %s' % (hana_software_path, component_medium))

	def install(self):
		'''
		This method parses JSON config file and creates the command arguments
		based on file parameters.
		'''
		with open('/opt/hope/config/config.json', 'r') as config_file:
			config = json.load(config_file)

		sid = config['sid']

		for purpose_key, purpose_value in config.items():

			if purpose_key == 'hana':

				component_medium     = purpose_value['component_medium']
				components           = purpose_value['components']
				root_password        = purpose_value['root_password']
				number               = purpose_value['number']
				db_mode              = purpose_value['db_mode']
				system_usage         = purpose_value['system_usage']
				sapadm_password      = purpose_value['sapadm_password']
				password             = purpose_value['password']
				system_user_password = purpose_value['system_user_password']
				action               = purpose_value['action']

		os.system('%s/51051851/DATA_UNITS/HDB_LCM_LINUX_PPC64/hdblcm \
			       --sid=%s \
			       --component_medium=%s/51051851 \
			       --components=%s \
			       --root_password=%s \
			       --number=%s \
			       --db_mode=%s \
			       --system_usage=%s \
			       --sapadm_password=%s \
			       --password=%s \
			       --system_user_password=%s \
			       --action=%s \
			       --batch' \
			       % (component_medium, \
			       	  sid, \
			       	  component_medium, \
			       	  components, \
			       	  root_password, \
			       	  number, \
			       	  db_mode, \
			       	  system_usage, \
			       	  sapadm_password, \
			       	  password, \
			       	  system_user_password, \
			       	  action))

	def remove(self):
		'''
		Method used to uninstall SAP HANA from System.
		'''
		with open('/opt/hope/config/config.json', 'r') as config_file:
			config = json.load(config_file)

		sid = config['sid']
		
		os.system('/hana/shared/%s/global/hdb/install/bin/hdbuninst --batch' % (sid))
