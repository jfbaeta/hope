# -*- coding: UTF-8 -*-

class UsrSap(object):
	
	"""class UsrSap"""

	name           = '/usr/sap'
	
	vg_args        = ''
	
	lv_size        = '-l 100%VG'	
	lv_args        = lv_size

	fs_type        = 'ext3'
	fs_mount_point = '/usr/sap'
	fs_args        = ''
	
	def __init__(self):
		super(UsrSap, self).__init__()