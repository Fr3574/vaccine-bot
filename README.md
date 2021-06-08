# Vaccine-Bot

This bot is created to help you get an appointment in one of the german Covid-19 Vaccination stations connected to [impfterminservice.de](https://www.impfterminservice.de)

## Installation

First you need to clone this repo to your local machine.

```bash
git clone https://github.com/Fr3574/vaccine-bot.git
cd vaccine-bot
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the needed packages.

```bash
pip3 install selenium twilio
```

Next you need to download the right [geckodriver](https://github.com/mozilla/geckodriver/releases) for your system. After you downloaded and unziped it you need to move to the `geckodriver` to `/usr/local/bin`.

```bash
mv ~/Downloads/geckodriver /usr/local/bin
```

## Usage

Before running the bot you need first set the correct configurations in `config.ini`. You need to have a twilio account and whatsapp integration as explained [here](https://www.twilio.com/docs/sms/send-messages).

```
[Mode]
# GETCODE or GETDATE
MODE = GETCODE
# True or False
Headless = False

[Data]
# The Code you will get from the website, fill up if MODE = GETDATE
code = XXXX-XXXX-XXXX
 # if you have a code and MODE = GETDATE only use one entry, if not add as much as you want but make sure to seperate each entry by a /
locations = 68163 Mannheim, Maimarkthalle
federal_state = Baden-Württemberg

[Twilio]
account_sid = XXXXXXXXXXXXXXXXXXXXXXXX
auth_token = XXXXXXXXXXXXXXXXXXXXXXXX
twilio_number = +XXXXXXXXXXX
your_number = +XXXXXXXXXXXXXXXXXX
```

Finally you can run the app.

```bash
python3 main.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
