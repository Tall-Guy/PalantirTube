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
    def createSearchTerms(self,gamelist):
        searchTerms = []
        for x in gamelist:
            searchTerms.append(x)
            searchTerms.append(x + " longplay")
            searchTerms.append(x + " gameplay")
            searchTerms.append(x + " review")
            searchTerms.append(x + " let's play")
            searchTerms.append(x + " walkthrough")
            searchTerms.append(x + " pt1")
            searchTerms.append(x + " part 1")
            searchTerms.append(x + " quick look")
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
        for z in range(numPages):
            print "Page ", z + 1, " of ", numPages
            for x in self.getChannelLinks():
                if not self.isOnList(x.get_attribute("href")):
                    self.saveLink(x.get_attribute("href"))
            
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
            

# This is the most important part.
# You have to list similar games here and keywords that
# relevant. The better you do this, the better the results
# will be. You can use google search semantics here so
# if you want two words together enclose them in \" \"
# Gosh I hope this is intelligible. 

gamelist = ["\"indie games\"","\"oldschool pvp\"","\"online pvp\"","\"new moba\"","\"online battle arena\""]
gamelist = gamelist + ["pc pvp", "pc steam pvp", "fantasy pvp"]
gamelist = gamelist + ["\"wow pvp\"", "\"wow classic\"", "\"vanilla pvp\"", "\"wow arena\""]
gamelist = gamelist + ["\"gw2 pvp\"", "\"guild wars pvp\"", "\"guild wars 2 pvp\"", "\"gw2 pvp\""]
gamelist = gamelist + ["bloodline champions", "battlerite", "blast out", "Bloodsports TV", "Bierzerkers", "Lawbreakers"]
gamelist = gamelist + ["gigantic", "Overpower", "Paragon"]

#gamelist = ["test"]

p = Palantir()
searchterms = p.createSearchTerms(gamelist)
numPages = 10

start = time.time()
i = 0.0
N = len(searchterms)

for x in searchterms:
    print "Searching for " + x
    p.openSearch(x, numPages)
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
    
