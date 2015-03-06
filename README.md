# amtrace-route

Traceroute implemented with python. Sends 3 UDP probes for each value of ttl, and records round trip times. Prints '*' for probes that didn't return before timing out. Has support for -m,-w,-p, -n, and -f options, which must be listed before the hostname.

-m max number of hops

-w waittime before timing out after sending a probe

-p port number UDP probes are addressed to

-n do not attempt to perform DNS reverse lookup on intermediate router ip addresses

-f first value for ttl
