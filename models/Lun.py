class Lun(object):
	
	"""class Lun"""
	
	index_header   = 'Index:'
	devmap_header  = 'Devmap:'
	wwid_header    = 'WWID:'
	vendor_header  = 'Vendor:'
	product_header = 'Product:'
	size_header    = 'Size:'
	name_header    = 'Name:'

	max_index_header   = len(index_header)
	max_devmap_header  = len(devmap_header)
	max_wwid_header    = len(wwid_header)
	max_vendor_header  = len(vendor_header)
	max_product_header = len(product_header)
	max_size_header    = len(size_header)
	max_name_header    = len(name_header)

	list_headers = []
	
	list_headers.append(index_header)
	list_headers.append(devmap_header)
	list_headers.append(wwid_header)
	list_headers.append(vendor_header)
	list_headers.append(product_header)
	list_headers.append(size_header)
	list_headers.append(name_header)

	def __init__(self, index='', devmap='', wwid='', vendor='', product='', size='', name=''):
		super(Lun, self).__init__()
		self.__index   = index
		self.__devmap  = devmap
		self.__wwid    = wwid
		self.__vendor  = vendor
		self.__product = product
		self.__size    = size
		self.__name    = name

	@property
	def index(self):
		return self.__index

	@property
	def devmap(self):
		return self.__devmap

	@property
	def wwid(self):
		return self.__wwid

	@property
	def vendor(self):
		return self.__vendor

	@property
	def product(self):
		return self.__product

	@property
	def size(self):
		return self.__size

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name

	@property
	def all(self):
		
		list_all = []

		list_all.append(self.__index)
		list_all.append(self.__devmap)
		list_all.append(self.__wwid)
		list_all.append(self.__vendor)
		list_all.append(self.__product)
		list_all.append(self.__size)
		list_all.append(self.__name)

		return list_all

	@property
	def lengths(self):
		
		self.list_max_lenghts = []

		if len(self.__index) > self.max_index_header:
			self.max_index_header = len(self.__index)
		if len(self.__devmap) > self.max_devmap_header:
			self.max_devmap_header = len(self.__devmap)
		if len(self.__wwid) > self.max_wwid_header:
			self.max_wwid_header = len(self.__wwid)
		if len(self.__vendor) > self.max_vendor_header:
			self.max_vendor_header = len(self.__vendor)
		if len(self.__product) > self.max_product_header:
			self.max_product_header = len(self.__product)
		if len(self.__size) > self.max_size_header:
			self.max_size_header = len(self.__size)
		if len(self.__name) > self.max_name_header:
			self.max_name_header = len(self.__name)

		self.list_max_lenghts.append(self.max_index_header)
		self.list_max_lenghts.append(self.max_devmap_header)
		self.list_max_lenghts.append(self.max_wwid_header)
		self.list_max_lenghts.append(self.max_vendor_header)
		self.list_max_lenghts.append(self.max_product_header)
		self.list_max_lenghts.append(self.max_size_header)
		self.list_max_lenghts.append(self.max_name_header)

		return self.list_max_lenghts