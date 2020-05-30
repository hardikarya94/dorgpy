import sys, getopt
import os, shutil, time

process_subd = True
input_dir = '.'
year_list = []

usage = """\nHelp section for dorgpy.py -option <value>\n
-h:	help
-d:	directory to process (default ./)
-s:	bool, process sub-directory or not (default True)\n"""

def scandirtree(dir) :
	dir_entries = os.scandir(dir)
	for entry in dir_entries :
		info = entry.stat()
		if entry.name == 'dorgpy.py' :
			continue
		file_time = time.gmtime(info.st_mtime)
		print(file_time.tm_year)
		if entry.is_dir() :
			if process_subd :
				print('Is a Directory ->\n')
				scandirtree(os.path.join(dir, entry.name))
			continue
		if file_time.tm_year not in year_list :
			year_list.append(file_time.tm_year)
			path = os.path.join(input_dir, str(file_time.tm_year))
			try:
				print("Creating", path)
				mode = 0o777
				oldmask = os.umask(000)
				print(oldmask)
				os.mkdir(path, mode)
				os.chmod(path, mode)
				os.umask(oldmask)
			except:
				print("Path already there", path)
		cur_file_path = os.path.join(dir, entry.name)
		dest = os.path.join(input_dir, str(file_time.tm_year), entry.name)
		shutil.move(cur_file_path, dest) 
		print(cur_file_path, dest)

def parse_arg(argv) :
	global process_subd;
	optlist, args = getopt.getopt(argv, 'd:hs:')
	print("Option Given: ", optlist)
	for opt, arg in optlist :
		if opt == '-h' :
			print(usage)
			exit()
		elif opt == '-d' :
			print("Directory: ", arg)
			input_dir = arg
		elif opt == '-s' :
			process_subd = bool(int(arg))
			print("Process Sub-Directory: ", arg, process_subd);
def main() :
	global input_dir
	scandirtree(input_dir)
	print(year_list)

if __name__ == "__main__" :
	arg = len(sys.argv)
	print(sys.argv)
	if arg > 1 :
		parse_arg(sys.argv[1:])
	main()