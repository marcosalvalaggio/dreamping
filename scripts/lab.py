import subprocess
import re

IP = '192.168.0.1'

result = subprocess.check_output(['arp', '-a', IP])
result = result.decode('utf-8')
print(result)
mac_pattern = re.compile(r'(\b[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b')
match = mac_pattern.search(result)
if match:
    print(match.group(0))
else: 
    print(None)


