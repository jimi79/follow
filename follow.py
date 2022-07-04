#!/usr/bin/python3

# we store the last day, check every minutes
# we indicate the tendency for the last hour, between 0 and 10%, more red or green
# meaning i need some rgb, in 256 colors
# and also a fake thing to test


import time
import random
import os
import math

debug = False

class Value:

	def __init__(self, date, value):
		self.date = date
		self.value = value

def getGrayScale(val):
	return min(255, 232 + (255 - 232) * val / 100)

def getColor(r, g, b): # with r g b from 0 to 100
	b = int(b / 100 * 6)
	b = min(b, 5)
	r = int(r / 100 * 6)
	r = min(r, 5)
	g = int(g / 100 * 6)
	g = min(g, 5)
	isNeutral = (b + g + r == 0)
	color = 16 + b + g * 6 + r * 36
	return color, isNeutral

class Check:

	def __init__(self):
		self.history = []
		self.diffTicksAgo = 10
		self.maxChange = 5

	def getRandomValue(self):
		if len(self.history) == 0:
			oldval = 1000
		else:
			oldval = self.history[-1].value
		r = math.pow(random.random(), 32)
		if random.random() < 0.5:
			r = -r
		diffInPercent = r * self.maxChange / 100
		return oldval + oldval * diffInPercent

	def getEscape(self, bg, fg):
		return "\033[48;5;%dm\033[38;5;%dm" % (bg, fg)

	def run(self):
		if debug:
			newval = self.getRandomValue()
		else:
			newval = self.getCurrentValue()
		if len(self.history) < self.diffTicksAgo:
			oldval = 1000
			diffInPercent = 0
		else:
			oldval = self.history[-self.diffTicksAgo].value
#wrong, i want the diff with the value 60 ticks ago, one hour
			diffInPercent = (newval - oldval) / oldval
		self.history.append(Value(time.time, newval))
		self.history = self.history[-1000:]
		diffPercentColor = diffInPercent * 100 / self.maxChange * 100
		diffPercentColor = min(100, abs(diffPercentColor))
		bgcolor = 0
		fgcolor = 7
		isNeutral = True
		if diffInPercent < 0: 
			bgcolor, isNeutral = getColor(diffPercentColor, 0, 0)
			if diffPercentColor > 80:
				fgcolor = 0
		if diffInPercent > 0: 
			bgcolor, isNeutral = getColor(0, diffPercentColor, 0)
			if diffPercentColor > 30:
				fgcolor = 0
		if not isNeutral:
			print("\007", end = "")

		#print("%0.2f (%0.2f %%) " % (newval, 100 * diffInPercent), end = "", flush = True)
		print(self.getEscape(bgcolor, fgcolor), end = "")
		#print("%0.2f (%0.2f %%) " % (newval, 100 * diffInPercent), end = "", flush = True)
		print("%0.2f " % (newval), end = "", flush = True)
		#print("line %d, %0.2f, before %0.2f, diff %0.2f%%" % (len(self.history), newval, oldval, diffInPercent * 100))
	
	def getCurrentValue(self):
		output = os.popen("curl --silent https://blockchain.info/ticker | jq '.USD.last'")
		#output = os.popen("cat b | jq '.USD.last'")
		return float(output.read())

def run():
	check = Check()
	while True:
		check.run()
		if debug:
			time.sleep(0.2)
		else:
			time.sleep(60)
		#time.sleep(1)

def test():
	for i in range(0, 101):
		print("\033[38;5;%dmA" % (getGrayScale(i)), end = "")
	print("")
	for i in range(0, 101):
		print("\033[38;5;%dmA" % (getColor(0, 0, i)), end = "")
	print("")
	for i in range(0, 101):
		print("\033[38;5;%dmA" % (getColor(0, i, 0)), end = "")
	print("")
	for i in range(0, 101):
		print("\033[38;5;%dmA" % (getColor(i, 0, 0)), end = "")
		#print(getColor(i, 0, 0))

#test()
run()