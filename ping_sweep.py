"""
    Ping sweep a network subnet for all hosts.

    Display hostname and IP address of active hosts.
    Default behaviour is to not show non-responsive hosts.

    To Do:
        1) Figure out how to sort the output by IP.
           - with multiprocessing the pings with a response are coming
             back much faster, as a result the output is out of order.

"""

__version__ = "0.1.2"


import socket
import subprocess as sp
import multiprocessing as mp
import ipaddress as ip
import argparse
from platform import system as p_sys


def get_args():
    """
        Get the subnet (if it was passed) from the command line using argparse.

        In: None
        Return: subnet
    """
    subnet = ""

    parser = argparse.ArgumentParser(description="Ping hosts in a given subnet.")
    parser.add_argument("subnet", metavar="1.2.3.4/24", type=str,
                        help="subnet in the form of ipaddress and netmask: 10.0.0.0/24")
    parser.add_argument("--show", action="store_true",
                        help="show hosts which are not reachable")

    """
        Parses the arguments provided by the user and stores them in the
        argument name(s) provided. In this case subnet and hide were used
        as the argument name.
    """
    args = parser.parse_args()
    subnet = args.subnet
    show = args.show

    return subnet, show


def get_host_list(subnet):
    """
        Based on the subnet and mask passed in create a list of IP addresses
        that belong to the network. Excludes the network address and the
        broadcast address.

        In: str, subnet in form 10.0.0.0/24
        Return: list of IP addresses
    """
    if str(ip.IPv4Network(subnet).broadcast_address) == subnet:
        raise ValueError("Invalid Entry. Likely no netmask (ie. /24) entered.")

    try:
        return list(ip.ip_network(subnet).hosts())
    except ValueError:
        print(f"\n\nInvalid network ({subnet}) entered!\n\n")
        quit()


def ping_host(ping_params, host_ip, show):
    """
        Ping all the hosts!
    """
    status, result = sp.getstatusoutput("ping " + ping_params  + " " + str(host_ip))

    try:
        # socket.gethostbyaddr returns a tuple if a hostname is found.
        # No hostname found returns a socket.error
        host_info = socket.gethostbyaddr(str(host_ip))[0]
    except socket.error:
        host_info = "** UNKNOWN **"

    if show and ("unknown host" in result.lower()):
        print(f"{str(host_ip)}  :  Unknown Host  :  {host_info}")
    elif show and ("host unreachable" in result.lower()):
        print(f"{str(host_ip)}  :  Host Unreachable  :  {host_info}")
    elif (("host unreachable" not in result.lower()) and ("unknown host" not in result.lower())):
        print(f"{str(host_ip)}  :  Host Alive  :  {host_info}")


def main():
    """
        Time to get to work!
    """

    if p_sys().casefold() == "linux":
        ping_params = "-c 1"
    elif p_sys().casefold() == "windows":
        ping_params = "-n 1"
    elif p_sys().casefold() == "darwin":
        ping_params = "-c 1"

    subnet, show = get_args()
    jobs = []

    for host_ip in get_host_list(subnet):
        p = mp.Process(target=ping_host, args=(ping_params, str(host_ip), show))
        jobs.append(p)
        p.start()


# If this script is executed as a script the main block will be called
# Otherwise it can be imported in to other scripts. Yeah... I don't know why
# you'd want to do that either.
if __name__ == "__main__":
    main()
