import sys
import os

process = sys.argv[1]
# this makes it so you don't kill the command process itselt
formattedProcess = '[' + process[0] + ']' + process[1:] 

os.system("kill $(ps aux | grep '{0}' | awk '{{print $2}}')".format(formattedProcess))
