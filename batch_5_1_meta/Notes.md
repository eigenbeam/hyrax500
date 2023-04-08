After several iteration, we have a set of fixes that address significant issues with our server.

Information about a run of the hyrax500 tester against a UAT deployment that submitted 78,400 URLs in 
parallel batches of 16. The source URLs to use for the data retrieval operations are in UAT_URLS_500.txt.
There were 88 failures (0.11 %) which is in line with the S3 failure rate. 

These URLs are from the UAT collection C1234714691-EEDTEST and from UAT CMR, a REST URL resolves to:

"relatedUrls": [
    {
      "url": "https://harmony.uat.earthdata.nasa.gov/service-results/harmony-uat-eedtest-data/C1234714691-EEDTEST/ATL03_20200714235814_03000802_005_01.h5",
      "type": "GET DATA",
      "mimeType": "application/x-hdfeos"
    },
    {
      "url": "https://opendap.uat.earthdata.nasa.gov/collections/C1234714691-EEDTEST/granules/SC:ATL03.005:225836084",
      "type": "USE SERVICE API",
      "subtype": "OPENDAP DATA"
    }
  ],

From the log files, it's clear we are using the 'GET DATA' URL and that it's likely going through the 
Harmony serve for these tests. Thus, maybe some of the errors we see are based on our server's interaction
with the Harmony service and not with S3.

NB: I'll rerun the tests using Kevin's origin set of URLs (in the 500.txt) file.

After that test ended with an asyncio.TimeoutError error in the hyrax500 tester code, I looked at the
two instances on UAT. There was only one docker container running on each instance and each had been 
running for 17-18 hours (consistent with the most recent UAT deployment).

Information from each machine is below and in four log files names *-m[1,2].log here. The bes-error...
log files were made using 'grep error' (since I don't know how to get files out of the Docker images
and off out the AWS instances).

Summary:

Since this is UAT, Harmony is using the server, too, and it's accesses show up in the logs.

The cleanup script seems to work; no temp files were left behind.

The DMR++ parse errors are all paired with an S3 retry. 

The hyrax500 tester recorded 88 total errors, but only one client-side error (a asyncio.TimeoutError).

Info from M1:

Some information from the machines:
[root@c04cc6b44d7d /]# ls -l /var/log/bes/
total 111360
-rw-r--r-- 1 bes  bes  114009199 Apr  8 12:12 bes.log
-rw-r--r-- 1 root root     16663 Apr  8 16:02 cleanup.log
[root@c04cc6b44d7d /]# grep error var/log/bes/bes.log | wc -l
188
[root@c04cc6b44d7d /]# grep error var/log/bes/bes.log > bes-error.log
[root@c04cc6b44d7d /]# ls -l /tmp
total 8
drwxr-xr-x 2 bes  bes    6 Apr  8 13:32 bes_rr_tmp
drwxr-xr-x 1 root root  26 Apr  7 22:32 hsperfdata_root
drwxr-x--- 2 bes  bes    6 Apr  8 12:12 hyrax_fonc
-rwx------ 1 root root 291 Feb 15 21:13 ks-script-q478qgfz
-rwx------ 1 root root 701 Feb 15 21:13 ks-script-xwi1grfe
[root@c04cc6b44d7d /]# ls -l /tmp/bes_rr_tmp/
total 0
[root@c04cc6b44d7d /]# ls -l /tmp/hyrax_fonc/
total 0
[root@c04cc6b44d7d /]# grep -v '^#.*$' /var/log/bes/cleanup.log | wc -l
64

Info from M2:

root@e37dc70f9df5 /]# ls -l /var/log/bes/
total 112796
-rw-r--r-- 1 bes  bes  115486389 Apr  8 12:12 bes.log
-rw-r--r-- 1 root root     14416 Apr  8 15:39 cleanup.log
[root@e37dc70f9df5 /]# grep error var/log/bes/bes.log | wc -l
141
[root@e37dc70f9df5 /]# grep error var/log/bes/bes.log > bes-error.log
[root@e37dc70f9df5 /]# ls -l /tmp
total 8
drwxr-xr-x 2 bes  bes    6 Apr  8 13:39 bes_rr_tmp
drwxr-xr-x 1 root root  26 Apr  7 22:39 hsperfdata_root
drwxr-x--- 2 bes  bes    6 Apr  8 12:12 hyrax_fonc
-rwx------ 1 root root 291 Feb 15 21:13 ks-script-q478qgfz
-rwx------ 1 root root 701 Feb 15 21:13 ks-script-xwi1grfe
[root@e37dc70f9df5 /]# ls -l /tmp/bes_rr_tmp/
total 0
[root@e37dc70f9df5 /]# ls -l /tmp/hyrax_fonc/
total 0
[root@e37dc70f9df5 /]# grep -v '^#.*$' /var/log/bes/cleanup.log | wc -l
51