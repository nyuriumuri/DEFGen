# Digital Design 2 Second Project: DEF Generator



## Prerequisites : 

- Python3

- [Pyverilog]( https://github.com/PyHDI/Pyverilog/tree/develop/pyverilog)

## How to run:

```
python3 project2.py vpath lefpath pinpath [--aspect ratio] [--x xmargin] [--y ymargin]
```

For instance, you can generate a DEF file for `tests/spm_1.v` as follows:

```
 python3 project2.py tests/spm_1.v tests/lef.lef tests/pins.txt  --aspect 0.7 --x 10000 --y 10000
```

This will generate a DEF file `xyz.def` in the main directory with x and y margins of 1000 and an aspect ratio of 0.7

## Code Structure:

```bash
├── project2.py 						(main file)
├── getmn.py 							(contains logic for calculating die area)
├── getpinpos.py 						(contains logic for getting the position of each pin)
├── tests								(testcases folder)
│   ├── lef.lef							(lef file used in test cases)
│   ├── pins.txt						(pin file used in test cases)
│   ├── spm_1.v							(verilog test case)
│   ├── lut_s44.synthesis.v				(verilog test case)
│   ├── ocs_blitter.synthesis.v			(verilog test case)
└── lef_parser 							(contains lef parser library)
```

