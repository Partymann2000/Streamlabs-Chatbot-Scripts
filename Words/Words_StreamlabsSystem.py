import clr
import sys
import json
import os
import ctypes
import codecs
import time

ScriptName = "Words Minigame"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Words Minigame for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.3.2"

configFile = "config.json"
wordsFile = "words.txt"
settings = {}
path = ""

wordsList = []
currentWord = ""
currentReward = 0

resetTime = 0

def ScriptToggled(state):
	return

def Init():
	global settings, wordsFile, wordsList, path

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"permission": "Everyone",
			"ignoreCaseSensitivity": True, 
			"newWordOnAnswer" : False, 
			"minReward": 1,
			"maxReward": 10,
			"minWordInterval": 10,
			"maxWordInterval": 20,			
			"responseAnnouncement": "Whoever writes $word first gets $reward $currency!",
			"wonResponse": "$user wrote $word first and won $reward $currency!"
		}

	wordsLocation = os.path.join(path, wordsFile) 

	try: 
		with codecs.open(wordsLocation, encoding="utf-8-sig", mode="r") as file:
			wordsList = [line.strip() for line in file if line.strip()]
	except:
		if os.path.isfile(wordsLocation): 
			wordsList = ["If you see this message save the file as UTF-8"]
		else: 
			with codecs.open(wordsLocation, encoding="utf-8-sig", mode="w+") as file:
				file.write('Put one word/message per line')
				wordsList = ['Open your "words.txt" file to add your own words"']
	
	return

def Execute(data):
	global currentWord, currentReward, resetTime

	if data.IsChatMessage() and ((data.Message == currentWord) or (settings["ignoreCaseSensitivity"] and (data.Message.lower() == currentWord.lower()))) and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		userId = data.User			
		username = data.UserName

		Parent.AddPoints(userId, username, currentReward)

		outputMessage = settings["responseWon"]	

		outputMessage = outputMessage.replace("$word", currentWord)
		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$reward", str(currentReward))
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())

		currentWord = ""
		currentReward = 0

		if settings["newWordOnAnswer"]:
			resetTime = time.time()	+ 10

		Parent.SendStreamMessage(outputMessage)
	return

def ReloadSettings(jsonData):
	Init()
	return

def OpenReadMe():
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)
	return

def OpenWordsFile():
	location = os.path.join(os.path.dirname(__file__), wordsFile)
	os.startfile(location)
	return


def Tick():
	global wordsList, resetTime, currentWord, currentReward

	if (settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"]):
		currentTime = time.time()

		if(currentTime >= resetTime):
			resetTime = currentTime + Parent.GetRandom((settings["minWordInterval"] * 60), (settings["maxWordInterval"] * 60) + 1)
			outputMessage = settings["responseAnnouncement"]

			currentReward = Parent.GetRandom(settings["minReward"], settings["maxReward"])
			currentWord = wordsList.pop(Parent.GetRandom(0, len(wordsList))) 

			if len(wordsList) == 0:
				try: 
					with codecs.open(os.path.join(path, wordsFile),encoding="utf-8-sig", mode="r") as file:
						wordsList = [line.strip() for line in file if line.strip()]
				except:
					wordsList = ["If you see this message save the file as UTF-8"]


			outputMessage = outputMessage.replace("$word", currentWord)
			outputMessage = outputMessage.replace("$reward", str(currentReward))
			outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())

			Parent.SendStreamMessage(outputMessage)
	return
