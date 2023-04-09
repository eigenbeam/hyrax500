
This run using the URLs in 500.txt started at 1057 MDT and ended at 2306 - 12 hours and 9 minutes (729m).

The requests were for subsets of HDF5 files, packages as NetCDF4 files.

Each batch of requests contains 193 URLs and there were 447 request sets (made in chunks of 16 URLs each).
The total number of requests was 86,271. There were 38 errors returned, each with the same message about 
failing to parse the DMR. There was one client side error that stopped the test program. The error rate
for this run was: 0.044%.

I did not look at the VMs. I started a second batch of tests on UAT that is identical _except_ that the 
requests will be made in chunks of 32 and the exception that stopped the client will be trapped and the 
client will record it and continue the test. Those tests started at about 1100 MDT.
