# -*- coding: UTF-8 -*-

def create_pvs(pvs):
	print 'Type Physical Volume name:'
	pv = raw_input()
	pvs.append(pv)

def create_vgs(vgs):
	print 'Type Volume Group name:'
	vg = raw_input()
	vgs.append(vg)

def create_lvs(lvs):
	print 'Type Logical Volume name:'
	lv = raw_input()
	lvs.append(lv)

def create_fss(fss):
	print 'Type File System name:'
	fs = raw_input()
	fss.append(fs)
	print fss
	print 'Creating File System /hana/data...'
	print 'Creating File System /hana/log...'
	print 'Creating File System /hana/shared...'

def menu():

	pvs = []
	vgs = []
	lvs = []
	fss = []

	option =''
	
	while(option != 'Q' and option != 'q' and option != 'E' and option != 'e'):
		print 'Create Physical Volumes (1):'
		print 'Create Volume Groups (2):'
		print 'Create Logical Volumes (3):'
		print 'Create File Systems (4):'
		print 'Quit/Exit (Q,q,E,e):'
		option = raw_input()

		if(option == '1'):
			create_pvs(pvs)
			print 'Creating Physical Volume hana_data_01...'
			print 'Creating Physical Volume hana_data_02...'
			print 'Creating Physical Volume hana_data_03...'
			print 'Creating Physical Volume hana_data_04...'
			print 'Creating Physical Volume hana_log_01...'
			print 'Creating Physical Volume hana_shared_01...'

		if(option == '2'):
			create_vgs(vgs)
			print 'Creating Volume Group hanadatavg...'
			print 'Creating Volume Group hanalogvg...'
			print 'Creating Volume Group hanasharedvg...'

		if(option == '3'):
			create_lvs(lvs)
			print 'Creating Logical Volume lv_hana_data...'
			print 'Creating Logical Volume lv_hana_log...'
			print 'Creating Logical Volume lv_hana_shared...'

		if(option == '4'):
			create_fss(fss)

		if(option != '1' and option != '2' and option != '3' and option != '4' and option != 'Q' and option != 'q' and option !='E' and option !='e'):
			print 'Invalid Option!'

menu()