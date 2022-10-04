<img src="https://i.imgur.com/ix547Un.png" alt="icon" width="256" hight="256"/>


# Probebahncard-Generator

This script would have generate you several thousand eCoupons during the probebahncard lottery.
Unfortunately the script is not working anymore because the lottery was closed on 30.09.2022 and all eCoupons expired on this date.

Therefore this repository is only for educational purposes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirement frameworks.

```bash
pip install -r requirements.txt
```
## Settings
1. Change the ```CATCHALL``` to your **catch all domain like** ```test.com``` or to a **gmail address** like ```probebahn@gmail.com```.
2. Set the right ```IMAPSERVER``` of your mail, for gmail its ```imap.gmail.com``` for example.
3. Set the ```EMAIL``` and ```PASSWORD``` of your mail account.

```env
CATCHALL=GMAIL-ADRESS-OR-DOMAIN
IMAPSERVER=SERVER_OF_THE_CATCHALL_MAIL
EMAIL=CATCHALL_EMAIL
PASSWORD=CATCHALL_PASSWORD
```
## Usage
1. Get proxys and put them into the proxies.txt file with the ```user:password@ip:port``` format.
2. Change your .env file with your own data.
3. Run the bot with ```python3 gen.py```.
4. Get your codes from the codes folder, the name of the textfile is the discount. (100.txt == 100% discount codes)


## License
[MIT](https://choosealicense.com/licenses/mit/)