# beanshell
A script to create plug-in beanshell scripts for NORSSTrack, buy querying space-track for provided sattelites

1. Modify the list of NORAD_ID's and associated variable name and colours in the plug_in_sats dictionary
2. Invoke the script - no parameters necessary

To provide space-track credentials:
  The invocation directory must have either the NORSSTRack configuration.properties file , or SLTrack.ini.
  configuration.properties will take precidence if both are available.

Usage: python3 create_script.py

output creates ./beanshell.bsh .    Move/rename this file to the NT_Setup/plugins/Active directory and restart NORSSTRack , 
or refresh plugins from the NORSTrack Plugins Menu option

Tested with python3.12
