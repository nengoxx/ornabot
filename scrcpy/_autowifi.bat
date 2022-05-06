::@ECHO OFF

::scrcpy -d --max-size 720 --bit-rate 1M

adb tcpip 5555
adb connect 192.168.1.137:5555
scrcpy -e --bit-rate 1M --max-size 720

PAUSE