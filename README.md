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

