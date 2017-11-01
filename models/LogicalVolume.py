class LogicalVolume(object):
	
	"""class LogicalVolume"""
	
	index_header  = 'Index:'
	path_header   = 'Path:'
	vgname_header = 'Volume Group:'
	name_header   = 'Name:'

	max_index_header  = len(index_header)
	max_path_header   = len(path_header)
	max_vgname_header = len(vgname_header)
	max_name_header   = len(name_header)

	list_headers = []
	
	list_headers.append(index_header)
	list_headers.append(path_header)
	list_headers.append(vgname_header)
	list_headers.append(name_header)

	def __init__(self, index='', path='', vgname='', name=''):
		super(LogicalVolume, self).__init__()
		self.__index  = index
		self.__path   = path
		self.__vgname = vgname
		self.__name   = name

	@property
	def index(self):
		return self.__index

	@property
	def path(self):
		return self.__path

	@property
	def vgname(self):
		return self.__vgname

	@property
	def name(self):
		return self.__name

	@property
	def all(self):
		
		list_all = []

		list_all.append(self.__index)
		list_all.append(self.__path)
		list_all.append(self.__vgname)
		list_all.append(self.__name)

		return list_all

	@property
	def lengths(self):
		
		self.list_max_lenghts = []

		if len(self.__index) > self.max_index_header:
			self.max_index_header = len(self.__index)
		if len(self.__path) > self.max_path_header:
			self.max_path_header = len(self.__path)
		if len(self.__vgname) > self.max_vgname_header:
			self.max_vgname_header = len(self.__vgname)
		if len(self.__name) > self.max_name_header:
			self.max_name_header = len(self.__name)

		self.list_max_lenghts.append(self.max_index_header)
		self.list_max_lenghts.append(self.max_path_header)
		self.list_max_lenghts.append(self.max_vgname_header)
		self.list_max_lenghts.append(self.max_name_header)

		return self.list_max_lenghts

	def mklv():
		pass