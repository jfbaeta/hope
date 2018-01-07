class Formatter(object):
	
	"""class Formatter"""
	
	def __init__(self):
		super(Formatter, self).__init__()

	def show(self, resource):

		first_resource         = resource.get()[0]
		resources              = resource.get()
		first_resource_headers = first_resource.list_headers
		number_of_fields       = len(first_resource_headers)
		number_of_columns      = number_of_fields - 1
		line_adjustment        = number_of_columns - 2

		temp_resource_list = []
		for resource in resources:
			temp_resource_list.append(resource.lengths)

		resource_list = zip(*temp_resource_list)

		max_lengths = []

		for item in resource_list:
			max_lengths.append(max(item))

		total_len = sum(max_lengths)

		left_corner     = '+-'
		right_corner    = '-+'
		left_column     = "| "
		right_column    = "|"
		horizontal_line = left_corner + '-' * (total_len + ((number_of_fields * 2) + line_adjustment)) + right_corner
		normal_string   = '%s'
		bold_string     = '\033[1m%s\033[0m'

		print horizontal_line
		loop_item_count = 0
		for header in first_resource_headers:
			print left_column + (bold_string) % (header.ljust(max_lengths[loop_item_count])),
			loop_item_count+=1
		print right_column
		print horizontal_line
		for resource_line in resources:
			loop_item_count = 0
			for resource_column in resource_line.all:
				print left_column + (normal_string) % (resource_column.ljust(max_lengths[loop_item_count])),
				loop_item_count+=1
			print right_column
		print horizontal_line