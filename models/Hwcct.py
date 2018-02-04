# -*- coding: UTF-8 -*-

from string import Template
import json, os, subprocess

class Hwcct(object):
	'''
	Class used for HWCCT (Hardware Configuration Check Tool) tests.
	'''
	def __init__(self):
		super(Hwcct, self).__init__()

	def extract(self):
		'''
		Method to extract SAP HANA Hardware Configuration Check Tool.
		It uses SAPCAR command to extract content.
		'''
		with open('/opt/hope/config/config.json', 'r') as config_file:
			config = json.load(config_file)

		sid = config['sid']

		for purpose_key, purpose_value in config.items():

			if purpose_key == 'hana':

				component_medium = purpose_value['component_medium']

		os.system('/usr/sap/hostctrl/exe/SAPCAR -xvf %s/51051851/DATA_UNITS/SAP_HANA_HWCCT_LINUX_PPC64/HWCCT.SAR -R /hana/shared' % (component_medium))

	def generate_files(self, test_type):
		'''
		Method to create JSON files used by SAP HANA to run KPI tests.
		'''
		with open('/opt/hope/config/config.json', 'r') as config_file:
			config = json.load(config_file)

		sid      = config['sid']
		hostname = subprocess.Popen(['hostname'], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()

		with open(test_type[0], 'r') as hwcct_test_file:
			print 'Generating JSON file for HWCCT Test...'
			tpl_hwcct_str = Template(hwcct_test_file.read())
			new_hwcct_str = tpl_hwcct_str.safe_substitute(hostname=hostname, sid=sid)

		with open(test_type[1], 'w') as new_hwcct_test_file:
			new_hwcct_test_file.write(new_hwcct_str)
		
		with open(test_type[1], 'r') as file:	
			print 'JSON File generated for HWCCT Test: %s' % test_type[1]
			print file.read()

	def run_test(self, test_type):
		'''
		Method to execute Operating System Evaluation, Short and Long KPI Performance tests.
		'''
		subprocess.Popen(['source /hana/shared/hwcct/envprofile.sh ; /hana/shared/hwcct/hwval -f %s' % test_type[1]], cwd='/hana/shared/hwcct', shell=True).communicate()[0]
