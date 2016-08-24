pattern-detect
--------------


Installation
-----------------------------------
after unzipping pattern-detect.tar.gz, "cd" into the directory pattern-detect where file setup.py rests. simply type following command in the terminal:

	python setup.py install

NOTICE:
If you get stuck at the this process for too long(more than 30 min), it is because this package needs to download its dependent package(pillow) from internet and your network speed is low. To solve this, firstly get out of this process(press CTRL+Z). Secondly install the dependency seperately, type following command in the terminal:

	pip install pillow

After success on installing the dependency, repeat previous step.


Usage(Command Line)
-----------------------------------
0)change mode of Shell script

	chmod +x prepare_data.sh

After doing this, you won't need this operation any further.

1)Prepare your data

put all your image files(.pdf) at the same directory. Type following in the terminal:

	./prepare_data.sh /path/to/the/directory

This process converts all the PDF files to the JPEG files and puts them at the same directory.

2)Detect

general usage of command:
	
	detect-pattern [--verbose] src_dir dst_dir gbb_dir

where src_dir is the directory which includes all the JPEG files of graphs, dst_dir is the directory to store all the target graphs after detection and gbb_dir is the directory to store the other non-target graphs. --verbose is the mode which prints out the detailed information.

e.g.

	detect-pattern --verbose ~/graph/ ~/target_graph/ ~/gbb_graph


Usage(Python Package)
-----------------------------------
To use (with caution), simply do::
	
	>>>import pattern-detect
	>>>img_path = "/path/to/the/JPG/image"
	>>>pattern-detect.detect(img_path, verbose=True)
