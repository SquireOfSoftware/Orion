
#!/bin/bash
PID=`ps -ef | grep process1 | grep -v "grep" | awk '{print $2}'`
echo $PID
#to check PID is right
kill -9 $PID
