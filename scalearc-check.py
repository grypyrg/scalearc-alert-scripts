#!/usr/bin/python

# scalearc-check.py - Check ScaleArc(TM) Load Balancer status using the API


# Copyright (c) 2014, Kenny Gryp, Frederic Descamps

# Author  : Frederic Descamps <lefred@percona.com>
# Date    : 2014-11-20
# Version : 0.1

import sys
import json
import urllib2
import getopt
import datetime
from dateutil.parser import parse

def parse_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dhH:k:", ["debug", "help", "host=", "key="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    host = "localhost"
    debug = False
    for o, a in opts:
        if o in ("-H", "--host"):
	    host = a
        elif o in ("-d", "--debug"):
            debug = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-k", "--key"):
            apikey = a
        else:
            assert False, "unhandled option"
    if len(args) > 0:
    	command = args[0] 
    else:
	print "ERROR: a check command is required !"
        sys.exit(3)
    checks = [ 'events', 'clusters', 'ha', 'license' ]
    if command not in checks:
	print "ERROR: <%s> is not a supported command ! %s" % (command, checks)
        sys.exit(3)
    return (host, apikey, command, debug )

def doCall(url, debug):
    try: 
    	content = urllib2.urlopen(url).read()
    except urllib2.URLError, e:
        print "ERROR: %s" % e.args
        sys.exit(2)
    except urllib2.HTTPError, e:
        print "ERROR: %s" % e.code
        sys.exit(2)
    except:
	print "ERROR: unkown error"
        sys.exit(2)
 
    if debug: print content 
    return json.loads(content)

def eventcheck(content, debug):
    if debug: print "Events ->  total: %s  new: %s  events: %s" % (content["data"]["total"], 
                                                                   content["data"]["new_events"],
                                                                   content["data"]["events"])
    if content["data"]["total"] == 0:
	print "OK: No Event In ScaleArc"
        sys.exit(0)
    else:
	print "ERROR: Events were found in  ScaleArc"
        sys.exit(1)

def clusterscheck(content, debug):
    if len(content["data"]) < 1:
        print "ERROR: no cluster data"
	sys.exit(1)
    tot_rw = 0
    # check amount of Read + Write servers in the cluster
    for i in content["data"][0]["cluster_servers"]:
         if debug: print "Clusters -> %s role is %s" % (i['server_ip'], i['server_role'])
	 if i['server_role'] == "Read + Write":
		tot_rw += 1
    if tot_rw == 1:    
	print "OK: There is only one Read + Write node"
        sys.exit(0)
    elif tot_rw < 1:
	print "ERROR: There is no Read + Write node"
        sys.exit(1)
    else:
	print "ERROR: More that 1 node acting as Read + Write"
        sys.exit(1)

def hacheck(content, debug):
    if debug: print "HA ->  local node %s (%s) running as \"%s\"" % (content["data"]["local_hostname"],
								     content["data"]["local_ip"], 
								     content["data"]["local_runningas"])
    if debug: print "HA ->  remote node %s (%s) running as \"%s\"" % (content["data"]["remote_hostname"],
								     content["data"]["remote_ip"], 
								     content["data"]["remote_runningas"])
    if content["data"]["local_runningas"]+content["data"]["remote_runningas"] \
       == "Running as PrimaryRunning as Secondary" or \
       content["data"]["local_runningas"]+content["data"]["remote_runningas"] \
       == "Running as SecondaryRunning as Primary":
	print "OK: HA running with one Primary and one Secondary"
        sys.exit(0)
    else:
	print "ERROR: HA issue, we don't have one Primary and one Secondary" 
        sys.exit(1)

def licensecheck(content, debug):
    lic_date = parse(content["data"]["license_expires_on"])
    difference = lic_date - datetime.datetime.now()
    if debug: print "License expires on %s, this is in %s days" % (content["data"]["license_expires_on"],
	 							   difference.days)
    if difference.days < 31:
	print "ERROR: ScaleArc license expires in %s days" % difference.days
        sys.exit(1)
    else:
	print "OK: ScaleArc license is still valid for %s days" % difference.days
        sys.exit(0)

    

def main():
    (host, apikey, command, debug) = parse_args()
    url = "https://%s/api/%s?apikey=%s" % (host, command, apikey)
    if debug: print "url to call = %s" % url
    content=doCall(url, debug)
    if command == "events":
	eventcheck(content, debug)
    elif command == "clusters":
	clusterscheck(content, debug)
    elif command == "ha":
	hacheck(content, debug)
    elif command == "license":
	licensecheck(content, debug)


def usage():
    print "scalearc-check.py [-d] [-h] [-H hostname] -k <API_KEY> <command>"
    print ""
    print "    -d | --debug  enable debug messages"
    print "    -h | --help   display this screen"
    print "    -H | --host   set the hostname to connect"
    print "    -k | --key    API key"
    print "    <command>     check to perform, available commands are 'events',"
    print "                  'clusters', 'ha', 'license'" 
    print ""
    return 0

if __name__ == "__main__":
    main()
