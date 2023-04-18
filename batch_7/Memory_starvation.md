Notes about memory starvation 

Intentionally triggered in SIT 

Using the SIT_URLS_memory_test.txt URLs and 64 simultaneous accesses, the server eventually failed. At least one
of the host's docker containers failed and the bes.log shows a failure to fork due to low memory.

One of the VMs became unusable - could not be accessed using SSM for a long time. No idea what was going on with that.
Eventually, I did connect with SSM, got logged in and copied the bes.log to the sit-logs bucket. The other VM had two
exited docker containers. The logs from them were copied to the batch_7 directory.

The tests ran until there were 100 HTTP 500 errors returned. The failures fall into several categories:
86 - Hyrax - Internal Error (500)
15 - Bad Gateway (502)

All the 502 errors are the same:

    <head><title>502 Bad Gateway</title></head>
    <body>
    <center><h1>502 Bad Gateway</h1></center>
    </body>
    </html>

The 500 errors from Hyrax are a mix of issues:

63 - 'Failed to create array ...' e.g., 
fileout.netcdf - Failed to create array of Float32 for eff_scatter: NetCDF: HDF error

12 - 'Problem with data transfer' 
    ERROR - Problem with data transfer. Message: cURL_error_buffer: &#39;Failed writing body (18446744073709551615 != 2940)&#39; cURL_message: &#39;Failed writing received data to disk/application&#39; (code: 23) CURLINFO_EFFECTIVE_URL: https://cmr.earthdata.nasa.gov/search/granules.umm_json_v1_4?collection_concept_id=C2146321631-POCLOUD&amp;granule_ur=cyg06.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32
    ERROR - Problem with data transfer. Message: cURL_error_buffer: &#39;OpenSSL SSL_read: SSL_ERROR_SYSCALL, errno 14&#39; cURL_message: &#39;Failure when receiving data from the peer&#39; (code: 56) CURLINFO_EFFECTIVE_URL: https://podaac-ops-cumulus-protected.s3.us-west-2.amazonaws.com/CYGNSS_L1_V3.1/cyg06.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32.nc?A-userid=jhrg&amp;X-Amz-Algorithm=AWS4-HMAC-SHA256&amp;X-Amz-Credential=...;X-Amz-Expires=3459&amp;X-Amz-Security-Token=...
    ERROR - Problem with data transfer. Message: cURL_error_buffer: &#39;Failed writing body (3494 != 16384)&#39; cURL_message: &#39;Failed writing received data to disk/application&#39; (code: 23) CURLINFO_EFFECTIVE_URL: https://podaac-ops-cumulus-protected.s3.us-west-2.amazonaws.com/CYGNSS_L1_V3.1/cyg06.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32.nc.dmrpp?A-userid=jhrg&amp;X-Amz-Algorithm=AWS4-HMAC-SHA256&amp;X-Amz-Credential=...
    ERROR - Problem with data transfer. Message: cURL_error_buffer: &#39;Failed writing body (3494 != 16384)&#39; cURL_message: &#39;Failed writing received data to disk/application&#39; (code: 23) CURLINFO_EFFECTIVE_URL: https://podaac-ops-cumulus-protected.s3.us-west-2.amazonaws.com/CYGNSS_L1_V3.1/cyg06.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32.nc.dmrpp?A-userid=jhrg&amp;X-Amz-Algorithm=AWS4-HMAC-SHA256&amp;X-Amz-Credential=...;X-Amz-Date=20230417T193403Z&amp;X-Amz-Expires=3467&amp;X-Amz-Security-Token=... 
    ERROR - Problem with data transfer. Message: cURL_error_buffer: &#39;Could not resolve host: podaac-ops-cumulus-protected.s3.us-west-2.amazonaws.com&#39; cURL_message: &#39;Couldn&#39;t resolve host name&#39; (code: 6) CURLINFO_EFFECTIVE_URL: https://podaac-ops-cumulus-protected.s3.us-west-2.amazonaws.com/CYGNSS_L1_V3.1/cyg07.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32.nc.dmrpp?A-userid=jhrg&amp;X-Amz-Algorithm=AWS4-HMAC-SHA256&amp;X-Amz-Credential=...;X-Amz-Date=20230417T193430Z&amp;X-Amz-Expires=3052&amp;X-Amz-Security-Token=...    

3 - DMR++ parse error: No document element found

6 - Failed to read data: STL Error: Resource temporarily unavailable





