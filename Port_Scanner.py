#!/usr/bin/python

import socket, sys, time, datetime, argparse, os

flag = 0
os.system('clear')

line = "*" * 100
desc = line + '\nThis is a Simple Port Scanner!!!! \n' + line + "\n" 

parser = argparse.ArgumentParser(description = desc, formatter_class = argparse.RawTextHelpFormatter)
parser.add_argument('host', metavar='H', help="Host Name You Wanna Scan")
parser.add_argument('startport', metavar='P1', nargs='?', help='Start Scanning From This Port')
parser.add_argument('endport', metavar='P2', nargs='?', help='Scan Until This Port')
args = parser.parse_args()

host = args.host
ip = socket.gethostbyname(host)

if args.startport and args.endport:
	start_port = int(args.startport)
	end_port = int(args.endport)

else:
	flag = 1

open_ports = []

common_ports = {
	'21': 'FTP',
	'22': 'SSH',
	'23': 'TELNET',
	'25': 'SMTP',
	'53': 'DNS',
	'69': 'TFTP',
	'80': 'HTTP',
	'109': 'POP2',
	'110': 'POP3',
	'123': 'NTP',
	'137': 'NETBIOS-NS',
	'138': 'NETBIOS-DGM',
	'139': 'NETBIOS-SSN',
	'143': 'IMAP',
	'156': 'SQL-SERVER',
	'389': 'LDAP',
	'443': 'HTTPS',
	'546': 'DHCP-CLIENT',
	'547': 'DHCP-SERVER',
	'995': 'POP3-SSL',
	'993': 'IMAP-SSL',
	'2086': 'WHM/CPANEL',
	'2087': 'WHM/CPANEL',
	'2082': 'CPANEL',
	'2083': 'CPANEL',
	'3306': 'MYSQL',
	'8443': 'PLESK',
	'10000': 'VIRTUALMIN/WEBMIN'
}

starting_time = time.time()
print "=" * 40+ "\n\tSimple Port Scanner..!!!\n" + "=" * 40

if flag:
	print "Scanning for Most Common Ports on %s" %(host)
else:
	print "Scanning %s from port %s - %s" %(host, start_port, end_port)
print "Scanning Started at %s"%(time.strftime("%I:%M:%S %p"))

def check_port(host, port, result=1):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.5)
		c = sock.connect_ex((host,port))
		if c == 0:
			result = c
		sock.close()

	except Exception, e:
		pass

	return result

def get_service(port):
	port = str(port)

	if port in common_ports:
		return common_ports[port]
	else:
		return 0

try:
	print "Scanning in Process......"
	print "Connecting to Port:"

	if flag:
		for p in sorted(common_ports):
			sys.stdout.flush()
			p = int(p)
			print p,
			response = check_port(host, p)
			if response == 0:
				open_ports.append(p)
				sys.stdout.write('\b' * len(str(p)))

	else:
		for p in range(start_port, end_port+1):
			sys.stdout.flush()
			print p,
			response = check_port(host, p)
			if response == 0:
				open_ports.append(p)
			if not p == end_port:
				sys.stdout.write('\b' * len(str(p)))

	print "\nScanning completed at %s" %(time.strftime("%I:%M:%S %p"))
	ending_time = time.time()
	total_time = ending_time - starting_time
	print "*" * 40 + "\n\tScan Report: %s \n" %(host) + "*" * 40

	if total_time <= 60:
		total_time = str(round(total_time, 2))
		print "Scan Took %s seconds" %(total_time)
	else:
		total_time = total_time / 60
		print "Scan Took %s Minutes" %(total_time)
		
	if open_ports:
		print "Open Ports: "
		for i in sorted(open_ports):
			service = get_service(i)
			if not service:
				service = "Unknown service"
			print "\t%s %s: Open" % (i, service)
	else:
		print "Sorry, No open ports found.!!"
 

except KeyboardInterrupt:
	print "You pressed Ctrl+C. Exiting "		
	sys.exit(1)