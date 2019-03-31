#!/usr/bin/env python
""" Tool to check if username is available or unavailable """

from urllib.request import urlopen
import argparse
import csv
import os
import datetime

__author__ = "Tony Benoy"
__copyright__ = "Copyright 2019, Tony Benoy"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "me@tonybenoy.com"

fileloc = str(os.getcwd()) + "/history"

def response(host,username,verbose,nolog):
    if host[-1] != "/":
        host = host + "/"
    if host[0:4] != "http":
        host = "https://" + host

    try:
        conn = urlopen(host+username)
        if verbose:
            print("Url checked : " + host + username +" " + str(conn.getcode()))        
        if nolog:
            file = open(fileloc,"a") 
            file.write(str(datetime.datetime.now()) + " " + host + username + " " + ("Unavailable" if str(conn.getcode()) == "200"  else "Error!")) 
            file.close()
        return "Unavailable" if str(conn.getcode()) == "200"  else "Error! Run again with -v to check respose"
    except Exception as e:
        if verbose:
            print("Url checked : " + host + username +" " + str(e))
        if nolog:
            file = open(fileloc,"a") 
            file.write(str(datetime.datetime.now()) + " "+ host + username + " " + ("Available" if str(e)[11:14] == "404" else "Error!")) 
            file.close()
        return "Available" if str(e)[11:14] == "404" else "Error! Run again with -v to check respose"

parser =  argparse.ArgumentParser(description="Tool to find if username exists.")
parser.add_argument("-H", "--host", type=str, help="Host to check the username in.")
parser.add_argument("-u", "--username",type=str, help="Username to check.")
parser.add_argument("-g", "--github",action="store_true", help="Check on github.")
parser.add_argument("-i", "--instagram",action="store_true", help="Check on instagram.")
parser.add_argument("-f", "--facebook",action="store_true", help="Check on facebook.")
parser.add_argument("-s", "--soundcloud",action="store_true", help="Check on facebook.")
parser.add_argument("-a", "--all",action="store_true", help="Check on all available sites.")
parser.add_argument("-v", "--verbose",action="store_true", help="Check on all available sites.")
parser.add_argument("-p", "--prefix",type=str, help="Add Prefix to username.")
parser.add_argument("-o", "--postfix",type=str, help="Add Postfix to username.")
parser.add_argument("-U", "--usercsv",help="Use CSV for mutiple usernames.")
parser.add_argument("-c", "--hostcsv",help="Use CSV for multiple hosts.")
parser.add_argument("-l", "--nolog",action="store_false", help="Prevent logging of the search.")
parser.add_argument("--logfile",help="Custom logfile location.")
args = parser.parse_args()

if args.logfile:
    fileloc = args.logfile
if args.username and args.host:
    if args.prefix:
        args.username = args.prefix + args.username
    if args.postfix:
        args.username = args.username + args.postfix 
    print(response(args.host , args.username , args.verbose,args.nolog))

if (args.username and args.facebook) or (args.username and args.all):    
    print(response("https://facebook.com/" , args.username, args.verbose,args.nolog))

if (args.username and args.instagram) or (args.username and args.all):
    print(response("https://instagram.com/" , args.username, args.verbose,args.nolog))

if (args.username and args.github) or (args.username and args.all):
    print(response("https://github.com/" , args.username, args.verbose,args.nolog))

if (args.username and args.soundcloud) or (args.username and args.all) :
    print(response("https://soundcloud.com/" , args.username, args.verbose,args.nolog))

if args.hostcsv and args.username:
    with open(args.hostcsv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for host in row:
                if args.prefix:
                    args.username = args.prefix + args.username
                if args.postfix:
                    args.username = args.username + args.postfix 
                print(response(host , args.username , args.verbose,args.nolog))

if args.usercsv and (args.host or args.instagram or args.facebook or args.soundcloud or args.github):
    with open(args.usercsv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for username in row:
                if args.github:
                    print(response("https://github.com" , username , args.verbose,args.nolog))
                if args.facebook:
                    print(response("https://facebook.com" , username , args.verbose,args.nolog))
                if args.instagram:
                    print(response("https://instagram.com" , username , args.verbose,args.nolog))
                if args.soundcloud:
                    print(response("https://soundcloud.com" , username , args.verbose,args.nolog))
                if args.prefix:
                    username = args.prefix + username
                if args.postfix:
                    username = username + args.postfix 
                if args.host:
                    print(response(args.host, username, args.verbose,args.nolog))

if args.usercsv and args.hostcsv:
    with open(args.usercsv) as usercsv_file:
        usercsv_reader = csv.reader(usercsv_file, delimiter=',')
        for userrow in usercsv_reader:
            for username in userrow:
                with open(args.hostcsv) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        for host in row:
                            print(response(host, username, args.verbose,args.nolog))
