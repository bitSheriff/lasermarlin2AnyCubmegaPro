import sys, pathlib
import argparse

# configure the argument parser for the cli usage
parser = argparse.ArgumentParser(description="Arguments for the converter.")
parser.add_argument('--input', '-i', type= pathlib.Path, action='store', help="Input file which should be converted", required=True)
parser.add_argument('--output', '-o', type= pathlib.Path, action='store', help="(optional) Output file where the result should be written to")






if __name__ == '__main__':
    # pares the given arguments
    args = parser.parse_args()
    # get the name of the input file (required)
    inputFile = args.input
    # get the name of the optional output file
    if args.output is None:
        # if output file is not given, it is the same as the input
        outputFile = inputFile
    else:
        outputFile = args.output

    # gcode from the input file 
    inputStream = ""

    with inputFile.open('r') as file:
        inputStream = file.read()

    print(inputStream)