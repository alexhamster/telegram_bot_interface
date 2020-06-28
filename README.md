# Telegram bot for channels

This is a bot for telegram channel suggestions wrote on **Python3**. The main goal of the bot is to provide one-sided communication between users and administrators of the channel.
It support additional features like a anti-spam, user banning, logging, and automatic free proxy collecting. Current version of bot is synchronous and single threaded.

## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip3 install pyTelegramBotAPI
pip3 install SQLAlchemy
pip3 install loguru
# for proxy support
pip3 install aiohttp
pip3 install proxybroker
```

## Configuration
1. Get bot token from [BotFather](https://telegram.me/BotFather)
2. In [BotFather](https://telegram.me/BotFather) write **/setjoingroups** and select **Enable**  
3. Create private channel and add bot as administrator
4. Init bot database(SQLite3): in bot root directory execute: 
```bash
$ python3 ./bot_orm/orm_model.py
```
5. Open **config.py** and paste **your** token from BotFather to *TOKEN*
```python
TOKEN = '123456789:FORE_EXAMPLE_hqzNIrx6hXTG5pMmCx00uh3w'
```
Now you need to get your channel id. Bot will send all from users to it.                                
6. In bot directory execute:
```bash
$ python3 ./run.py
```
7. In your telegram channel write command < **/init** >
, if all ok bot send id of your channel. For example: "Admin channel ID: **-1234567890**"
8.  Open **config.py** and paste the channel id to *OUT_CHANEL_ID*
```python
OUT_CHANEL_ID = -1234567890
```
9. Restart bot by execute:
```bash
$ python3 ./run.py
```
In case of no errors bot will redirect content (images, gifs, links) to your channel.
## Using proxy
To enable working through proxy in **run.py** call main() like that:
```python
if __name__ == '__main__':
    while True:
        logger.info('Starting new iteration of main')
        try:
            main(use_proxy=True, refresh_proxy_list=True)
        except Exception as e:
            logger.critical(repr(e))
```
## Usage
[Overview](https://media1.giphy.com/media/KHiVctel8gN3woiypX/giphy.gif)                                  
[How to ban](https://media2.giphy.com/media/Qvv5wVE1RXp2soggf2/giphy.gif)

## TODO
* Multiprocessing
* Caching with Redis 
* Duplicated content recognition with ML

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
## License
[MIT](https://choosealicense.com/licenses/mit/)
