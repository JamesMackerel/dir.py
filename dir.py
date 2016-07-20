import os
from prettytable import PrettyTable

def calc_dir_size(root_dir):
	try:
		if not os.path.isdir(root_dir):
			return os.path.getsize(root_dir)
	except FileNotFoundError:
		print(root_dir+ " FileNotFound")
	
	size = 0

	try:
		for lists in os.listdir(root_dir):
			path = os.path.join(root_dir, lists)
			
			if os.path.isdir(path):
				size += calc_dir_size(path)
			else:
				try:
					size += os.path.getsize(path)
				except FileNotFoundError:
					print(root_dir+ " FileNotFound")
				
	except PermissionError:
		print(root_dir + " PermissionError")
	
	return size
	
if __name__=='__main__':
	root = os.getcwd()
	table = PrettyTable(['Name', 'Size(MB)'])
	
	print("Name\tSize")
	for dir_name in os.listdir(root):
		row = [dir_name, calc_dir_size(os.path.join(root, dir_name))/1024/1024]
		table.add_row(row)
		
	print(table)