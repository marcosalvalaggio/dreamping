from icmplib import ping

response = ping('192.168.10.4', count=1, timeout=0.1)
print(response)
print(response.avg_rtt)