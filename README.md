# dorgpy
# Directory Organiser

Move photos/videos from all sub-directories to new folders created with year when file is created.

# How to use:
python dorgpy.py

Help section for dorgpy.py -option <value>

  h:	help
  
  d:  directory to process (default ./)
  
  e:  Organise by file extention (default True)
  
  t:  Organise by file cretion year (default True)
  
  s:	bool, process sub-directory or not (default True)


# Prerequisite:
python3

# OS:
Windows10, linux, Ubuntu support is added

# Example
python dorgpy.py
python dorgpy.py -e 1 -t 0
python dorgpy.py -e 0 -t 1
python dorgpy.py -d <directory_path>
