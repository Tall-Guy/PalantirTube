# -*- coding: utf-8 -*-

import SeleniumControl
import time
import random
import datetime

# Hope I don't get sued by J.R.R
class Palantir:
    def __init__(self):
        self.s = SeleniumControl.SeleniumControl()
    
    
# This is entirely optional and you can skip this.
    def createSearchTerms(self,game):
        searchTerms = []
        # game = game + " game"
        searchTerms.append(game + " gameplay")
        searchTerms.append(game + " top")
        searchTerms.append(game + " analysis")
        searchTerms.append(game + " best plays")
        searchTerms.append(game + " review")
        searchTerms.append(game + " first look")
        searchTerms.append(game + " let's play")
        searchTerms.append(game + " impressions")
        searchTerms.append(game + " quick look")
        # searchTerms.append(game)
        # searchTerms.append(game + " longplay")
        # searchTerms.append(game + " tutorial")
        # searchTerms.append(game + " how to")
        # searchTerms.append(game + " walkthrough")
        # searchTerms.append(game + " pt1")
        # searchTerms.append(game + " part 1")
        return searchTerms
            
       
# This function gets all channel links from a search page.       
    def getChannelLinks(self):
        channellinks = self.s.driver.find_elements_by_css_selector('.yt-simple-endpoint.style-scope.yt-formatted-string')
        # print channellinks
        return channellinks
        
        
# Main function.
    def openSearch(self,searchterm,numPages):
        # Initialize Selenium Driver.
        self.s.noProxy()
        # Open youtube and search for keyword provided.
        url = "https://www.youtube.com/results?q=" + searchterm + "&sp=CAMSBAgFEAE%253D";
        
        self.s.openUrl(url)

        # Scrape links from first ten pages.
        emptyPages = 0
        limit = 1
        for z in range(numPages):
            found = 0
            print "Page ", z + 1, " of ", numPages
            for x in self.getChannelLinks():
                if not self.isOnList(x.get_attribute("href")):
                    found = 1
                    self.saveLink(x.get_attribute("href"))
            if found == 0:
                emptyPages = emptyPages + 1
                print "Empty - Strike ", emptyPages, " of ", limit
                if emptyPages >= limit:
                    print "Not worth continuing this search"
                    break;
            
            self.nextPage()
            time.sleep(random.randint(5,6) + random.random())
        
    def nextPage(self):
        el = self.s.driver.find_elements_by_class_name("yt-uix-button-content")
        for x in el:
            if x.text.find("Nast") != -1:
                x.click()
            else:
                pass

    def saveLink(self,link):
        print link
        f = open("data/YoutubeChannels.Oink",'a')
        f.write(link+"\n")
        f.close()
        
    def isOnList(self,link):
        f = open("data/YoutubeChannels.Oink",'r')
        data = f.read().split("\n")
        f.close()
        
        if link in data:
            return True
        return False
        
    def numEntries(self):
        f = open("data/YoutubeChannels.Oink",'r')
        data = f.read().split("\n")
        f.close()

        return len(data)
            

# This is the most important part.
# You have to list similar games here and keywords that
# relevant. The better you do this, the better the results
# will be. You can use google search semantics here so
# if you want two words together enclose them in \" \"
# Gosh I hope this is intelligible. 

gamelist = []#["\"indie games\"","\"oldschool pvp\"","\"online pvp\"","\"new moba\"","\"online battle arena\""]
#gamelist = gamelist + ["pc pvp", "pc steam pvp", "fantasy pvp"]
#gamelist = gamelist + ["\"wow pvp\"", "\"wow classic\"", "\"vanilla pvp\"", "\"wow arena\""]
#gamelist = gamelist + ["\"gw2 pvp\"", "\"guild wars pvp\"", "\"guild wars 2 pvp\"", "\"gw2 pvp\""]
#gamelist = gamelist + ["bloodline champions", "battlerite", "blast out", "Bloodsports TV", "Bierzerkers", "gigantic", "Overpower", "Lawbreakers"]
gamelist = gamelist + ["Paragon"]

#gamelist = ["test"]

p = Palantir()

i = 0.0
N = len(gamelist)
start = time.time()
for game in gamelist:
    
    searchterms = p.createSearchTerms(game)
    numPages = 10

    print "Beginning Searches for " + game
    for x in searchterms:
        currentEntries = p.numEntries()
        print "Searching for " + x
        p.openSearch(x, numPages)
        if currentEntries == p.numEntries():
            print "Not worth continuing searching for ", game
            break
        
    i = i + 1
    progress = i / N
    print "Progress: ", progress * 100.0, "%"
    now = time.time()
    elapsed = now - start
    elapsedSTR = str(datetime.timedelta(seconds=elapsed))
    print "Time Elapsed: ", elapsedSTR.split(".")[0]
    estimatedTotal = elapsed / progress
    remaining = estimatedTotal - elapsed
    eta = str(datetime.timedelta(seconds=remaining))
    print "ETA: ", eta.split(".")[0]

print "Done!"
    
