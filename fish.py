from random import shuffle, randint
from statlib import stats
#from sets import Set

debugMode = 0
displayPops = 0

class Town(object):
	def __init__(self):
		self.Home = set([])
		self.Market = set([])
		self.Ocean = set([])
		self.Graveyard = set([])
		
		self.stock = 0
		
	def clone(self, oldTown):
		self.Home = oldTown.Home.copy()
		self.Market = oldTown.Market.copy()
		self.Ocean = oldTown.Ocean.copy()
		self.Graveyard = oldTown.Graveyard.copy()
		self.stock = oldTown.stock
	
	def morningCommute(self):
		tempHome = self.Home.copy()
			
		for mando in tempHome:
			if mando.manType == 0:
				if mando.fish == 0:
					self.Home.remove(mando)
					self.Market.add(mando)
			elif mando.manType == 1:
				if mando.fish > 0:
					self.Home.remove(mando)
					self.Market.add(mando)
				else:
					self.Home.remove(mando)
					self.Ocean.add(mando)
			elif mando.manType == 2:
				self.Home.remove(mando)
				self.Market.add(mando)
		
		if debugMode == 1: 
			print "After morning commute:"
			self.townStatus()
		
	def stockMarket(self):
		trainees = 0
		tempMarket = self.Market.copy()
		
		for mando in tempMarket:
			if mando.manType == 1:
				self.stock = self.stock + mando.dumpFish()
			elif mando.manType == 2:
				self.stock = self.stock + mando.dumpFish()
				self.Market.remove(mando)
				self.Ocean.add(mando)
				if [subman.manType for subman in self.Market].count(0) - trainees > 0:
					trainees = trainees + 1				
		
		for mando in tempMarket:
			if mando.manType == 0 and trainees > 0:
				self.Market.remove(mando)
				self.Ocean.add(mando)
				trainees = trainees - 1
					
		if debugMode == 1: 
			print "After stockMarket:"
			self.townStatus()
					
	def sellMarket(self):
		for mando in self.Market:
			if mando.fish == 0 and self.stock > 0:
				self.stock = self.stock - 1
				mando.getFish(1)
					
	def fishingDay(self, maxFish):
		for mando in self.Ocean:
			if mando.manType == 0:
				mando.trainFish(maxFish)
			if mando.manType >= 1:
				mando.goFish(maxFish)
	
	def returnHome(self):
		tempOcean = self.Ocean.copy()
		tempMarket = self.Market.copy()
		
		for mando in tempOcean:
			if mando.fish == 0 and self.stock > 0:
				mando.getFish(1)
				self.stock = self.stock - 1
			self.Ocean.remove(mando)
			self.Home.add(mando)
		for mando in tempMarket:
			self.Market.remove(mando)
			self.Home.add(mando)

		if debugMode == 1: 
			print "After returnHome:"
			self.townStatus()
		
	def assessHunger(self, deathHunger):
		tempHome = self.Home.copy()
		
		for mando in tempHome:
			mando.eat()
			if mando.hunger >= deathHunger:
				self.Home.remove(mando)
				self.Graveyard.add(mando)
	
	def townStatus(self):
		print "Stock is " + str(self.stock)
		print "Home contains " + str(len(self.Home)) + " total.  0: " + str([subman.manType for subman in self.Home].count(0)) + " 1: " + str([subman.manType for subman in self.Home].count(1)) + " 2: " + str([subman.manType for subman in self.Home].count(2))
		print "Market contains " + str(len(self.Market)) + " total.  0: " + str([subman.manType for subman in self.Market].count(0)) + " 1: " + str([subman.manType for subman in self.Market].count(1)) + " 2: " + str([subman.manType for subman in self.Market].count(2))	
		print "Ocean contains " + str(len(self.Ocean)) + " total.  0: " + str([subman.manType for subman in self.Ocean].count(0)) + " 1: " + str([subman.manType for subman in self.Ocean].count(1)) + " 2: " + str([subman.manType for subman in self.Ocean].count(2))		
		print "Graveyard contains " + str(len(self.Graveyard)) + " total.  0: " + str([subman.manType for subman in self.Graveyard].count(0)) + " 1: " + str([subman.manType for subman in self.Graveyard].count(1)) + " 2: " + str([subman.manType for subman in self.Graveyard].count(2))			

class Man(object):
	def __init__(self, id, input):
		self.id = id
		self.manType = input
		self.hunger = 0
		self.fish = 0
	
	def becomeType(self, newType):
		self.manType = newType
			
	def dumpFish(self):
		if self.fish > 1:
			stock = self.fish - 1
			self.fish = 1
			return stock
		else:
			return 0
			
	def getFish(self, numFish):
		self.fish = self.fish + numFish
		
	def trainFish(self, maxHarvest):
		x = randint(0, maxHarvest)
		if x > 1:
			self.getFish(x)
			self.becomeType(1)
		
	def goFish(self, maxHarvest):
		self.getFish(randint(0, maxHarvest))
		
	def eat(self):
		if (self.fish > 0):
			self.fish = self.fish - 1
			return 1
		elif (self.fish == 0):
			self.hunger = self.hunger + 1
			return 0

def main():
	
	townSize = 100
	duration = 100
	
	if debugMode == 1:
		iterations = 1
		trials = 1
	else:
		iterations = 100
		trials = 35
	
	fPercentBase = 0
	fPercentDelta = 0
	
	tPercentBase = 0
	tPercentDelta = 1
	
	deathHungerBase = 2
	deathHungerDelta = 0
	
	maxHarvestBase = 5
	maxHarvestDelta = 0
	
	previousMean = 0
	previousStDev = 0
		
	for iteration in range(iterations):
		fPercent = fPercentBase + (fPercentDelta * iteration)
		tPercent = tPercentBase + (tPercentDelta * iteration)
		deathHunger = deathHungerBase + (deathHungerDelta * iteration)
		maxHarvest = maxHarvestBase + (maxHarvestDelta * iteration)
			
		numFishers = int(fPercent * (townSize / 100))
		numTeachers = int(tPercent * (townSize / 100))
	
		survivingPops = []
		
		for trial in range(trials):
			Canvas = []
	
			# Create first two towns
			Canvas.append(Town())
	
			for i in range(numFishers):
				Canvas[0].Home.add(Man(i, 1))
			if numTeachers > 1:
				for i in range(numTeachers):
					Canvas[0].Home.add(Man(i, 2))
			for i in range(townSize - numFishers - numTeachers):
				Canvas[0].Home.add(Man(i, 0))
					
			for day in range(duration):	
		
				Canvas[day].morningCommute()
		
				Canvas[day].stockMarket()
		
				Canvas[day].sellMarket()
		
				Canvas[day].fishingDay(maxHarvest)
		
				Canvas[day].returnHome()
		
				if debugMode == 1: print "Before deathHunger on day " + str(day) + ", home population is " + str(len(Canvas[day].Home)) + " and there are " + str(len(Canvas[day].Market)) + " people hungry in the market"
		
				Canvas[day].assessHunger(deathHunger)
							
				if debugMode == 1: print "At the end of day " + str(day) + ", home population is " + str(len(Canvas[day].Home)) + " and there are " + str(len(Canvas[day].Market)) + " people hungry in the market"
		
				Canvas.append(Town())
				Canvas[day + 1].clone(Canvas[day])
		
			survivingPops.append(len(Canvas[day].Home))
	
		if displayPops == 1: print survivingPops
		
		currentMean = stats.mean(survivingPops)
		currentStDev = stats.stdev(survivingPops)
		
		if displayPops == 1:
			print str(currentMean) + ", " + str(currentStDev)
		else:
			print str(currentMean) + ", " 
		
		previousMean = currentMean
		previousStDev = currentStDev
		
	
if __name__ == "__main__":
	main()
	