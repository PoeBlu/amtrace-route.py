#!/usr/bin/python

import socket
import sys
import getopt
import time

def main():

    #default port address for UDP packets
    port_number=33434
 
    #default timeout value in seconds 
    waittime=5

    #default max number of hops
    max_hops=30
    icmp=socket.getprotobyname("icmp")
    udp=socket.getprotobyname("udp")

    #default starting ttl
    ttl=1 

    #default flag is true for mapping ip addresses to hostnames
    map_flag=True
    #get options
    #options come before hostname
    args=sys.argv[1:]
    try:
        optlist, args=getopt.getopt(args,'nm:w:p:f:')
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    for opt, arg in optlist:
        if opt=='-m':
            max_hops=int(arg)
        if opt=="-w":
            waittime=int(arg)
        if opt=="-p":
            port_number=int(arg)
        if opt=="-f":
            ttl=int(arg)
        if opt=="-n":
            map_flag=False
    socket.setdefaulttimeout(waittime)
    dest_name=args[0]
    dest_addr=socket.gethostbyname(dest_name)
        
    while True:
        times=[]
        for x in xrange(0,3):
            recv_socket=socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            send_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
            send_socket.setsockopt(socket.SOL_IP,socket.IP_TTL,ttl)
            recv_socket.bind(("",port_number))
            #begin timer
            t=time.time()
            send_socket.sendto("",(dest_name,port_number))
            cur_addr=None
            try:
                # returns tuple containing data and address
                _ , cur_addr=recv_socket.recvfrom(512)
                #finish time in ms
                t=(time.time()-t)*1000

                #address itself was a tuple, first element is ipv4 address
                cur_addr=cur_addr[0]
                try:
                    #socket.gethostbyaddr performs reverse DNS lookup and returns triplet, with the first element being the hostname
                    cur_name=socket.gethostbyaddr(cur_addr)[0]
                except socket.error:
                    #traceroute prints ip address twice if unable to resolve hostname
                    cur_name=cur_addr
            except socket.timeout:
                pass
            finally:
                send_socket.close()
                recv_socket.close()

            if cur_addr is not None:
                cur_host="%s (%s)" %(cur_name, cur_addr)
            else:
                #icmp messages never received from intermediate routers
                cur_host="*"
            times.append(t)

        #if the socket times out, t still equals time since the epoch, which is always larger than 1000000
        upper=1000000
        print " %d" % ttl,
        if map_flag or cur_host=='*':
            print " %s"% cur_host,
        else:
            print " %s"% cur_addr,
        if times[0]<upper:
            print "  %f ms" % times[0],
        else:
            print " * ",
        if times[1]<upper:
            print "  %f ms" % times[1],
        else:
            print " * ",
        if times[2]<upper:
            print "  %f ms" % times[2]
        else:
            print " * "
        ttl+=1
        if cur_addr==dest_addr or ttl >max_hops:
            break

if __name__=="__main__":
    main()

