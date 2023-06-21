from pyaiml21  import Kernel
from glob import glob

MyBot = Kernel()


aiml_files = glob("AIML FILES/*")
for files in aiml_files:
    MyBot.learn_aiml(files)


while True:
    text = input("Human : ")
    response = MyBot.respond(text,"USER_1")
    print("Bot : ",response)