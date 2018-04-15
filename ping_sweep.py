"""
    Ping sweep a network subnet for all hosts.
    
    Display hostname and IP address of active hosts.

    To Do:
        1) Figure out how to sort the output by IP.
           - with multiprocessing the pings with a response are coming
             back much faster, as a result the output is out of order.
        2) Add Windows support.

"""

__version__ = "0.1.1"


import socket
import subprocess as sp
import multiprocessing as mp
import ipaddress as ip
import argparse


def get_args():
    """
        Get the subnet (if it was passed) from the command line using argparse.
        
        In: None
        Return: subnet
    """
    subnet = ""

    parser = argparse.ArgumentParser(description="Ping hosts in a given subnet.")
    parser.add_argument("subnet", metavar = "1.2.3.4/24", type = str, 
                        help = "subnet in the form of ipaddress and netmask: 10.0.0.0/24")
    parser.add_argument("--hide", action = "store_true", 
                        help = "hide hosts which are not reachable")


    """
        Parses the arguments provided by the user and stores them in the
        argument name(s) provided. In this case subnet and hide were used
        as the argument name.
    """
    args = parser.parse_args()
    subnet = args.subnet
    hide = args.hide

    return subnet,hide


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


def ping_host(x, hide):
    """
        Ping all the hosts!
    """
    _, result = sp.getstatusoutput("ping -c1 " + str(x))

    try:
        host_info = socket.gethostbyaddr(str(x))[0]
    except:
        host_info = "** UNKNOWN **"

    if not hide and ("unknown host" in result.lower()):
        print(f"{str(x)}  :  Unknown Host  :  {host_info}")
    elif not hide and ("host unreachable" in result.lower()):
        print(f"{str(x)}  :  Host Unreachable  :  {host_info}")
    elif ("time" in result.lower()) and not (("host unreachable" in result.lower()) or ("unknown host" in result.lower())):
        print(f"{str(x)}  :  Host Alive  :  {host_info}")


def main():
    """
        Time to get to work!
    """

    subnet, hide = get_args()
    jobs = []

    for x in get_host_list(subnet):
        try:
            host_info = socket.gethostbyaddr(str(x))[0]
        except:
            host_info = ""
        p = mp.Process(target=ping_host, args=(str(x), hide))
        jobs.append(p)
        p.start()


# If this script is executed as a script the main block will be called
# Otherwise it can be imported in to other scripts. Yeah... I don't know why
# you'd want to do that either.
if __name__ == "__main__":
    main()
