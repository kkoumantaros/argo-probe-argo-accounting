#!/usr/bin/env python
import argparse
import sys
import requests

class UserNameSpace(object):
    pass

class ProbeResponse:
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self):
        self.status_code = self.OK

    def writeOK(self, msg):
        print("OK - %s" % msg)
        self.status_code = self.OK

    def writeWARNING(self, msg):
        print("WARNING - %s" % msg)
        self.status_code = self.WARNING

    def writeCRITICAL(self, msg):
        print("CRITICAL - %s" % msg)
        self.status_code = self.CRITICAL

    def writeUNKNOWN(self, msg):
        print("UNKNOWN - %s" % msg)
        self.status_code = self.UNKNOWN

    def getStatusCode(self):
        return self.status_code


def check_status(args):
    probe = ProbeResponse()
    try:
        if args.probe_type == "default":
            response = requests.get("%s/status" % args.url, timeout=args.timeout)
            response.raise_for_status()

            status = response.json()["state"]

            if status == "RUNNING":
                probe.writeOK("Service available")

            else:
                probe.writeWARNING("Service not available: %s" % status)
        elif args.probe_type == "accounting":
            response = requests.get("%s/%s" % (args.url, args.path), timeout=args.timeout)
            response.raise_for_status()

            status = response.json()["status"]

            if status == "UP":
                probe.writeOK("Service available")

            else:
                probe.writeWARNING("Service not available: %s" % status)

    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
        ValueError,
        KeyError
    ) as err:
        probe.writeCRITICAL(str(err))

    except Exception as err:
        probe.writeUNKNOWN(str(err))

    sys.exit(probe.getStatusCode())


def main():
    parser = argparse.ArgumentParser(
        description="ARGO probe that checks service status.", add_help=False
    )
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument(
        "-t", "--timeout", type=int, dest="timeout", help="timeout",
        required=True
    )
    required.add_argument(
        "-u", "--url", type=str, dest="url", help="service url", required=True
    )
    optional.add_argument(
        "-T", "--type", type=str, dest="probe_type", default="default",
        choices=["default","accounting"], action="store",
        help="the type of probe"
    ) 
    optional.add_argument(
        "-h", "--help", action="help", default=argparse.SUPPRESS,
        help="show this help message and exit"
    )
    user_namespace = UserNameSpace()
    parser.parse_known_args(namespace=user_namespace)
    if user_namespace.probe_type == 'accounting':
        optional.add_argument(
            '--path',
            dest='path',
            action='store',
            required=True,
            help='The path on where to check the JSON'
        )
        args = parser.parse_args(namespace=user_namespace)

    check_status(args)


if __name__ == "__main__":
    main()
