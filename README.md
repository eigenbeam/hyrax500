## Instructions

1. Create a file named `token.txt` and add your EDL user token to it

2. Install dependencies

        $ pip install -r requirements.txt

3. Run with 16 concurrent requests:

        $ python hy500.py token.txt 16 500.txt

## Output

You'll see the HTTP status codes of each request batch. If there are 500 errors
for any in the batch, the URL and content of the response will be printed.
