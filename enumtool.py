import requests
from argparse import ArgumentParser

# defines the colors on the console, taken from blender:
# https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def print_intro():
    print("────────────────────────────────────────────────────────────────────────────────────────────")
    print(" ██╗      ███████╗███╗   ██╗██╗   ██╗███╗   ███╗████████╗ ██████╗  ██████╗ ██╗           ██╗")
    print(" ╚██╗     ██╔════╝████╗  ██║██║   ██║████╗ ████║╚══██╔══╝██╔═══██╗██╔═══██╗██║          ██╔╝")
    print("  ╚██╗    █████╗  ██╔██╗ ██║██║   ██║██╔████╔██║   ██║   ██║   ██║██║   ██║██║         ██╔╝ ")
    print("  ██╔╝    ██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║   ██║   ██║   ██║██║   ██║██║         ╚██╗ ")
    print(" ██╔╝     ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║   ██║   ╚██████╔╝╚██████╔╝███████╗     ╚██╗")
    print(" ╚═╝      ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝      ╚═╝")
    print(" Automatic asset enumeration script, made with <3 by nothing4free                      " + color.OKBLUE + "v.0.1" + color.ENDC)
    print("────────────────────────────────────────────────────────────────────────────────────────────")


parser = ArgumentParser(description="Automatic asset enumeration script")
parser.add_argument('-s', '--search', type=str, dest="search", help="Company name")
args = parser.parse_args()
print_intro()

print("Now scanning for assets belonging to: " + args.search)
