## NOTES

There are 10 unique granules in SIT_URLS_DAP_500.txt. They are:

(base) jgallag4@GSLAL2023031970 hyrax500-2 % sed 's@.*\(collections.*\)\.dap.*@\1@g' < SIT_URLS_DAP_500.txt | sort -u

collections/C2146321631-POCLOUD/granules/cyg02.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32
collections/C2146321631-POCLOUD/granules/cyg03.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32
collections/C2146321631-POCLOUD/granules/cyg03.ddmi.s20180802-000000-e20180802-235959.l1.power-brcs.a31.d32
collections/C2146321631-POCLOUD/granules/cyg04.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32
collections/C2146321631-POCLOUD/granules/cyg06.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32
collections/C2146321631-POCLOUD/granules/cyg06.ddmi.s20180802-000000-e20180802-235959.l1.power-brcs.a31.d32
collections/C2146321631-POCLOUD/granules/cyg07.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32
collections/C2146321631-POCLOUD/granules/cyg07.ddmi.s20180802-000000-e20180802-235959.l1.power-brcs.a31.d32
collections/C2146321631-POCLOUD/granules/cyg08.ddmi.s20180801-000000-e20180801-235959.l1.power-brcs.a31.d32
collections/C2146321631-POCLOUD/granules/cyg08.ddmi.s20180802-000000-e20180802-235959.l1.power-brcs.a31.d32

## Instructions

1. Create a file named `token.txt` and add your EDL user token to it

  To list EDL tokens your user already has:

        $ ./edl.sh -r

  To create a new EDL token for your user:

        $ ./edl.sh -c

  To delete an EDL token for your user:

        $ ./edl.sh -d <token>

2. Install dependencies

        $ pip install -r requirements.txt

3. Run with 16 concurrent requests:

        $ python hy500.py token.txt 16 500.txt base_name

## Output

You'll see the HTTP status codes of each request batch. If there are 500 errors
for any in the batch, the URL and content of the response will be printed.
Valid responses will be saved to files named 'base_name'_N where N is the run
number.

Unlike the original version of hy500, this version runs in an infinite loop, 
cycling through the URLs in the third argument forever.

