# -*- coding: UTF-8 -*-

class UsrSap(object):
	'''
	Class used for /usr/sap attributes.
	Attributes and methods are passed to other LVM Classes.
	'''
	name           = 'usrsap'
	
	vg_args        = ''
	
	lv_size        = '-l 100%VG'	
	lv_args        = lv_size

	fs_type        = 'ext3'
	fs_mount_point = '/usr/sap'
	fs_args        = ''
	
	def __init__(self):
		super(UsrSap, self).__init__()