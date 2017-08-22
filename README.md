# press-freedom-bot
simple sms bot built off spreadsheet
# story-hotline
playing &amp; collecting audio stories over phone calls

## About
TKTK

## Running this app locally (for development)
**1. Install OS level dependencies**
  - Python 3
  - MySQL

**2. Clone this repo**
  ```bash
  git clone https://github.com/buzzfeed-openlab/press-freedom-bot.git
  cd press-freedom-bot
  ```

**3. Install required python libraries**  

Optional but recommended: make a virtual environment

Install requirements:
```bash
pip install -r requirements.txt
```


**4. Create a MySQL database**

```bash
mysql -u root
```
& then
```bash
create database pfb;
```

If you're working locally, you're good to go. But if you're going to host this on a shared server you probably want to create a new user for this database so it isn't all `root`.

**5. Configure the app**

TODO: make this better

Two ways of doing this: (a) making a config file or (b) setting environment variables

*Option A*:  
Make the secret json config file, `hotline_app/config_vars_secret.json`
Then, edit the config file (MORE DOCUMENTATION DETAILS TO COME)

*Option B*:  
see the keys in `DEFAULT_SETTINGS` in `hotline_app/config.py` for the names of environment variables to set (MORE DOCUMENTATION DETAILS TO COME)

**6. Run the app**

  ```bash
  python application.py
  ```

**7. Initialize the database**

  Visit the `/initialize` route (e.g. `localhost:5000/intialize`) & enter admin credentials (`ADMIN_USER` & `ADMIN_PASS`). This will create the `story` table for storing responses.
