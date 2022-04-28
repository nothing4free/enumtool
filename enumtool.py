import requests
from argparse import ArgumentParser
import tldextract

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
    parser.add_argument('-a', '--as', type=str, dest="autonomous_system", help="Company name", required=True)
    parser.add_argument('-f', '--file', type=str, dest="file", help="The file to dump the domains to.", required=True)
    args = parser.parse_args()
    return args


def print_intro():
    print(" ───────────────────────────────────────────────────────────────────────────────────────────")
    print(" ██╗      ███████╗███╗   ██╗██╗   ██╗███╗   ███╗████████╗ ██████╗  ██████╗ ██╗           ██╗")
    print(" ╚██╗     ██╔════╝████╗  ██║██║   ██║████╗ ████║╚══██╔══╝██╔═══██╗██╔═══██╗██║          ██╔╝")
    print("  ╚██╗    █████╗  ██╔██╗ ██║██║   ██║██╔████╔██║   ██║   ██║   ██║██║   ██║██║         ██╔╝ ")
    print("  ██╔╝    ██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║   ██║   ██║   ██║██║   ██║██║         ╚██╗ ")
    print(" ██╔╝     ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║   ██║   ╚██████╔╝╚██████╔╝███████╗     ╚██╗")
    print(" ╚═╝      ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝      ╚═╝")
    print(" Automatic asset enumeration script, made with <3 by nothing4free                      v.0.1")
    print(" ───────────────────────────────────────────────────────────────────────────────────────────")


def get_prefixes(search_query):
    url = "https://api.bgpview.io/asn/" + search_query + "/prefixes"
    resp = requests.get(url=url)
    data = resp.json()
    cidr_prefixes = []
    for ipv4_prefix in data["data"]["ipv4_prefixes"]:
        cidr_prefixes.append(ipv4_prefix["prefix"])
    # print(cidr_prefixes)
    print(" [i] Found a total of " + str(len(cidr_prefixes)) + " CIDR prefixes.")
    return cidr_prefixes


def get_cidr_domains(cidr_prefixes):
    resp_list = []
    domains_list = []
    cidr_domains = []
    for prefix in cidr_prefixes:
        url = "https://sonar.omnisint.io/reverse/" + prefix
        resp = requests.get(url=url)
        resp_list.append(resp.json())

    for response in resp_list:
        for key, value in response.items():
            domains_list.append(value)

    for dom_list in domains_list:
        for element in dom_list:
            if len(element) >= 2:
                cidr_domains.append(element)

    return cidr_domains


def get_tlds(domains):
    tlds = []
    for domain in domains:
        tlds.append(tldextract.extract(domain).domain)
    tlds = list(set(tlds)) # deletes the duplicate domains from the list

    return tlds


def get_domains_by_tld(tlds):
    tld_list = []
    tld_domains = []
    for tld in tlds:
        url = "https://sonar.omnisint.io/tlds/" + tld
        resp = requests.get(url=url)
        tld_list.append(resp.json())

    for item in tld_list:
        for domain in item:
            tld_domains.append(domain)

    tld_domains = list(set(tld_domains)) # deletes the duplicates
    return tld_domains


def write_on_file(cidr_prefixes, domains, file):
    f = open(file, "w")
    f.write(" > CIDR prefixes found: " + str(len(cidr_prefixes)) + "\n")
    for prefix in cidr_prefixes:
        f.write(prefix + "\n")
    f.write("\n > Total domains found: " + str(len(domains)) + "\n")
    for domain in sorted(domains):
        f.write(domain + "\n")
    f.close()


# def get_subdomains(domains):
#     subdomains_list = []
#     subdomains = []
#     for domain in domains:
#         url = "https://sonar.omnisint.io/all/" + domain
#         resp = requests.get(url=url)
#         subdomains_list.append(resp.json())
#
#     for item in subdomains_list:
#         for subdomain in item:
#             subdomains.append(subdomain)
#
#     print(subdomains[0])
#     print(subdomains[100])
#     print(" amt: " + str(len(subdomains)))


def main():
    args = parse_args()
    print_intro()

    print(" [i] Now scanning for assets belonging to autonomous system " + args.autonomous_system)

    file = args.file
    cidr_prefixes = get_prefixes(args.autonomous_system)
    cidr_domains = get_cidr_domains(cidr_prefixes)
    tlds = get_tlds(cidr_domains)
    domains = get_domains_by_tld(tlds)
    for domain in cidr_domains:
        domains.append(domain)
    domains = list(set(domains))
    print(" [i] Found a total of " + str(len(domains)) + " domains.")
    write_on_file(cidr_prefixes, domains, file)
    print(" [i] Results successfully written to: " + file)
    print("     You can now use (the other tool) to individually search for subdomains.")
    print(" ───────────────────────────────────────────────────────────────────────────────────────────")


main()
