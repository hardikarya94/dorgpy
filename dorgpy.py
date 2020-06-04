import sys, getopt
import os, shutil, time

process_subd = True
input_dir = '.'

# Defines for organising by file year
org_year = True
year_list = []

# Defines for organising by file extention
org_ext = True
ext_list = {
	"IMAGE": ["img", "jpg", "jpeg", "raw", "png", "bmp", "ico", "gif"],
	"VIDEO": ["mp4", "avi", "mkv", "3gp", "flv", "mov", "mpeg", "mpg", "wmv"],
	"DOCUMENTS": ["pdf", "doc", "txt", "docx", "rtf", "pptx", "ppt"]
}
ext_dir_list = []

usage = """\nHelp section for dorgpy.py -option <value>\n
-h:	help
-d:	directory to process (default ./)
-e: Organise by file extention (default True)
-t: Organise by file cretion year (default True)
-s:	bool, process sub-directory or not (default True)\n"""

def create_dir(path) :
	try:
		print("Creating", path)
		mode = 0o777
		oldmask = os.umask(000)
		os.mkdir(path, mode)
		os.chmod(path, mode)
		os.umask(oldmask)
	except:
		print("Path already there", path)

def move_file(dir, dest_dir, fname) :
	cur_file_path = os.path.join(dir, fname)
	dest = os.path.join(input_dir, dest_dir, fname)
	shutil.move(cur_file_path, dest)
	print("Moved File", cur_file_path, dest)

def dorg_year_fn(dir, entry) :
	info = entry.stat()
	file_time = time.gmtime(info.st_mtime)
	if file_time.tm_year not in year_list :
		year_list.append(file_time.tm_year)
		path = os.path.join(input_dir, str(file_time.tm_year))
		create_dir(path)
	move_file(dir, str(file_time.tm_year), entry.name)

def dorg_ext_fn(dir, entry) :
	fextn = ((entry.name.split('.'))[1]).lower()
	ftype = "MISC"
	for type in ext_list :
		for extnt in ext_list[type] :
			if extnt == fextn :
				ftype = type
	if ftype not in ext_dir_list :
		ext_dir_list.append(ftype)
		path = os.path.join(input_dir, ftype)
		create_dir(path)
	move_file(dir, str(ftype), entry.name)

def scan_dir_tree(dir) :
	print("Start scanning", dir, "\n")
	dir_entries = os.scandir(dir)
	for entry in dir_entries :
		if entry.name == 'dorgpy.py' :
			continue
		if entry.is_dir() :
			if process_subd :
				print('Is a Directory ->\n')
				sub_dir = os.path.join(dir, entry.name)
				scan_dir_tree(sub_dir)
				os.rmdir(sub_dir)
			continue
		if org_ext :
			dorg_ext_fn(dir, entry)
		elif org_year :
			dorg_year_fn(dir, entry)

def parse_arg(argv) :
	global process_subd, org_year, org_ext;
	optlist, args = getopt.getopt(argv, 'd:e:ht:s:')
	print("Option Given: ", optlist)
	for opt, arg in optlist :
		if opt == '-h' :
			print(usage)
			exit()
		elif opt == '-d' :
			print("Directory: ", arg)
			input_dir = arg
		elif opt == "-e" :
			org_ext = bool(int(arg))
		elif opt == "-t" :
			org_year = bool(int(arg))
		elif opt == '-s' :
			process_subd = bool(int(arg))
			print("Process Sub-Directory: ", arg, process_subd);
def main() :
	global input_dir, org_ext
	scan_dir_tree(input_dir)
	print(org_year, org_ext)
	if org_year == org_ext :
		org_ext = False
		input_dir = os.path.join(input_dir,'IMAGE')
		scan_dir_tree(input_dir)
	print(year_list)

if __name__ == "__main__" :
	arg = len(sys.argv)
	print(sys.argv)
	if arg > 1 :
		parse_arg(sys.argv[1:])
	main()
