import sys, pathlib
import argparse

# configure the argument parser for the cli usage
parser = argparse.ArgumentParser(description="Converter for the laser module of the Anycubic Mega Pro", add_help=True)
parser.add_argument('--input', '-i', type= pathlib.Path, action='store', help="Input file which should be converted", required=True)
parser.add_argument('--output', '-o', type= pathlib.Path, action='store', help="(optional) Output file where the result should be written to")
parser.add_argument('--home', action='store_true', help="(optional) Homing before program start", default=False)
parser.add_argument('--height', '-H', type=int, action='store', help="height of the workpiece [mm]", required=True)
parser.add_argument('--focus','-f', type=int, action='store', help="(optional) Focus height of the laser [mm]", default=50)



# Constants
HEADER = "\
; ---- MARLIN 2 ANYCUBIC MEGA PRO ---- \n\
; converted by lasermarlin2AnyCubMegaPro (https://github.com/bitSheriff/lasermarlin2AnycubMegaPro) "
CMD_HOMEING_ALL = "G28"
CMD_MARLIN_LASER = "M106"
CMD_ANYCUBIC_LASER = "G4 P0\nG6"
CMD_SETZERO_Z = "G92 Z0"
CMD_MOVE_Z = "G1 Z"


def getStartConfig(homeing, focus, workpiece):
    config = HEADER + "\n"
    height = focus + workpiece
    # move to home if wanted
    if homeing is True:
        config += CMD_HOMEING_ALL + "\n"
    # move z to right height
    config += str(CMD_MOVE_Z) + str(height) + "\n"
    # reset the zero position
    config += CMD_SETZERO_Z + "\n"
    return config

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

    # check if the given file was already converted
    if (inputStream.find(HEADER) != -1):
        print("The given file was already converted")
        exit()

    # get the generated string from the user arguments
    configString = getStartConfig(homeing=args.home, focus= args.focus, workpiece=args.height)

    # new gcode which will be written to the output file
    outputStream = ""
    # insert the configuration at beginning
    outputStream += configString
    # replace the generic marlin laser commands with the commands Anycubic uses
    outputStream += inputStream.replace(CMD_MARLIN_LASER, CMD_ANYCUBIC_LASER)

    # write the file to the output file 
    with outputFile.open('w+') as file:
        file.write(outputStream)