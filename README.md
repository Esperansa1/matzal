# Sigit-Matzal
This is a website to manage all students in the course - where they are, and when, and export a matzal.
You can set the status of each student, and export a text / see a fancy site of the matzal. The hantar also has special permissions such as resetting all statuses.

## Background
Shauli suggested course Sigit will use a website to manage their Matzal whilst learning from home.

The super-classified team, also known as "HaTzevet" got straight to it.

## Deployment
The site is based on flask, and requires a few other libraries as specified in `requirements.txt`. The site been tested to work on python versiosn `>=3.10.5`.

To run the server:
```bash
pip install -r requirements.txt
python3 server.py
```