::@ECHO OFF
scrcpy -e --bit-rate 1M --max-size 720
PAUSE

::adb tcpip 5555
::adb connect 192.168.0.207

::scrcpy --max-size 1366
::scrcpy -m 1366  # short version

::scrcpy --bit-rate 2M
::scrcpy -b 2M  # short version

::scrcpy -s 044d769ff0c7540a