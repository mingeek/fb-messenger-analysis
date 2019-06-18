# fb-messenger-analysis

A sentiment analysis of FB Messenger conversations

- Download Facebook data (https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav)

- Place your Facebook messages in your current directories "/messages/" folder. The Facebook messages when downloaded are in separate folders. Copy all of those folders into the /messages/ folder.

- install Python (currently uses Python 3.5, not sure about compatability with other version of Python)

- pip install -r requirements.txt

- python3 analyze.py

* This does NOT handle duplicate names. I.E. If there are two people named Alex Kim, the first one will be overridden. It's more work than it's worth at this point to deal with a duplicate identity when parsing the HTML. Maybe in the future I'll fix it, but for now that's a known bug (not that anybody's encountered it)
