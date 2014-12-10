ScaleArc Alert Scripts
======================

This script does some basic checks to find out the status of a ScaleArc machine.


net-snmpd
---------

If you want to integrate with net-snmpd, add the following to /etc/snmp/snmpd.conf:

```
exec  scale_lic /usr/bin/scalearc-check.py -k KEY license 
exec  scale_ev /usr/bin/scalearc-check.py -k KEY events 
exec  scale_ha /usr/bin/scalearc-check.py -k KEY ha 
exec  scale_clu /usr/bin/scalearc-check.py -k KEY clusters 
```

You can then fetch the result over SNMP:

```
[root@test ~]# snmpwalk -v 2c -c public localhost .1.3.6.1.4.1.2021.8 
UCD-SNMP-MIB::extIndex.1 = INTEGER: 1 
UCD-SNMP-MIB::extIndex.2 = INTEGER: 2 
UCD-SNMP-MIB::extIndex.3 = INTEGER: 3 
UCD-SNMP-MIB::extIndex.4 = INTEGER: 4 
UCD-SNMP-MIB::extNames.1 = STRING: scale_lic 
UCD-SNMP-MIB::extNames.2 = STRING: scale_ev 
UCD-SNMP-MIB::extNames.3 = STRING: scale_ha 
UCD-SNMP-MIB::extNames.4 = STRING: scale_clu 
UCD-SNMP-MIB::extCommand.1 = STRING: /usr/bin/scalearc-check.py -k KEY license 
UCD-SNMP-MIB::extCommand.2 = STRING: /usr/bin/scalearc-check.py -k KEY events 
UCD-SNMP-MIB::extCommand.3 = STRING: /usr/bin/scalearc-check.py -k KEY ha 
UCD-SNMP-MIB::extCommand.4 = STRING: /usr/bin/scalearc-check.py -k KEY clusters 
UCD-SNMP-MIB::extResult.1 = INTEGER: 0 
UCD-SNMP-MIB::extResult.2 = INTEGER: 0 
UCD-SNMP-MIB::extResult.3 = INTEGER: 1 
UCD-SNMP-MIB::extResult.4 = INTEGER: 1 
UCD-SNMP-MIB::extOutput.1 = STRING: OK: ScaleArc license is still valid for 322 days 
UCD-SNMP-MIB::extOutput.2 = STRING: OK: No Event In ScaleArc 
UCD-SNMP-MIB::extOutput.3 = STRING: ERROR: HA issue, we don't have one Primary and one Secondary 
UCD-SNMP-MIB::extOutput.4 = STRING: ERROR: no cluster data 
UCD-SNMP-MIB::extErrFix.1 = INTEGER: noError(0) 
UCD-SNMP-MIB::extErrFix.2 = INTEGER: noError(0) 
UCD-SNMP-MIB::extErrFix.3 = INTEGER: noError(0) 
UCD-SNMP-MIB::extErrFix.4 = INTEGER: noError(0) 
UCD-SNMP-MIB::extErrFixCmd.1 = STRING:  
UCD-SNMP-MIB::extErrFixCmd.2 = STRING:  
UCD-SNMP-MIB::extErrFixCmd.3 = STRING:  
UCD-SNMP-MIB::extErrFixCmd.4 = STRING:  
```
