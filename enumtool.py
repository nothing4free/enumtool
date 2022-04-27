import requests
from argparse import ArgumentParser
import json

# defines the colors on the console, taken from blender:
# https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py


class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def parse_args():
    parser = ArgumentParser(description="Automatic asset enumeration script")
    parser.add_argument('-a', '--as', type=str, dest="autonomous_system", help="Company name")
    args = parser.parse_args()
    return args


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


def get_prefixes(search_query):
    url = "https://api.bgpview.io/asn/" + search_query + "/prefixes"
    resp = requests.get(url=url)
    data = resp.json()
    cidr_prefixes = []
    for ipv4_prefix in data["data"]["ipv4_prefixes"]:
        cidr_prefixes.append(ipv4_prefix["prefix"])
    # print(cidr_prefixes)
    return cidr_prefixes


def get_cidr_domains(cidr_prefixes):
    resp_list = []
    domains = []

    for prefix in cidr_prefixes:
        url = "https://sonar.omnisint.io/reverse/" + prefix
        resp = requests.get(url=url)
        resp_list.append(resp.json())

    for response in resp_list:
        for key, value in response.items():
            domains.append(value)

    print(domains)

def main():
    args = parse_args()
    print_intro()
    print("[" + color.OKBLUE + "i" + color.ENDC + "] Now scanning for assets belonging to: " + args.autonomous_system)
    cidr_prefixes = get_prefixes(args.autonomous_system)
    get_cidr_domains(cidr_prefixes)


main()
