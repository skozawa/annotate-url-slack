import sys
import os
sys.path.append(os.getcwd())

from slackbot.bot import Bot
def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
