# -*- coding: utf-8 -*-

import SeleniumControl
import time
import random
import datetime
class Palantir:
    def __init__(self):
        self.s = SeleniumControl.SeleniumControl()
    
        
    # Main function. Browses the channel and checks for
    # social media urls and whether there is an email or not.
    
    def browseChannel(self,channel):
        # self.s.openUrl(channel + "/videos/")
        # time.sleep(1)

        # I removed score calculation, maybe someone can add 
        # this, it needs some work. Like counting keywords from
        # all videos on a channel or something.

        #score = self.calculateScore()
        self.s.openUrl(channel + "/about")
        time.sleep(1)
                
        subs = self.getSubs()
        print "Subs: ", subs
        
        views = self.getViews()
        print "Views: ", views
        
        joined = self.getJoined()
        print "Joined: ", joined
        
        emaillink = self.hasEmail()       
        if emaillink == "has email":
            emaillink = channel + "/about"
        else:
            emaillink = "-"

        print "Email: " + emaillink

        location = self.getLocation()
        print "Location: " + location
                
        # Get links
        links = self.getLinks()
        websiteURL = "-"
        facebookURL = "-"
        twitterURL = "-"
        googlePlusURL = "-"
        discordURL = "-"
        redditURL = "-"
        
        for link in links:
            name = link[0].lower()
            url = link[1]
            if name == "website":
                websiteURL = url
            elif "facebook" in name:
                facebookURL = url
            elif "twitter" in name:
                twitterURL = url
            elif "google" in name:
                googlePlusURL = url
            elif "discord" in name:
                discordURL = url
            elif "reddit" in name:
                redditURL = url

        print "Website: ", websiteURL
        print "Facebook: ", facebookURL
        print "Twitter: ", twitterURL
        print "Google+: ", googlePlusURL
        print "Discord: ", discordURL
        print "Reddit: ", redditURL

        savestring = channel + ";" + str(subs) + ";" + str(views) + ";" + str(joined) + ";" + emaillink + ";" + location + ";" + websiteURL + ";" + facebookURL + ";" + twitterURL + ";" + googlePlusURL + ";" + discordURL + ";" + redditURL
        
        self.saveLink(savestring)
    
    
    # This is really important. You have to input
    # the string on the mail label here.
    
    def hasEmail(self):
        if self.s.driver.page_source.find("View email address") != -1:
            return "has email"
        return "no email"
   
   
    def getLocation(self):
        el = self.s.driver.find_elements_by_xpath("//div[@id='details-container']/table/tbody/tr[2]/td[2]/yt-formatted-string")
        for x in el:
            if x.text != "":
                return x.text
        return "-"
   
   
   # Gets all the links from about section.
    def getLinks(self):
        links = []
        el = self.s.driver.find_elements_by_xpath("//div[@id='link-list-container']/a")
        for x in el:
            name = x.text
            url = x.get_attribute("href")
            http = "%3A%2F%2F"
            if http not in url:
                continue
            url = "http://" + url.split("%3A%2F%2F")[1]
            url = url.split("&redir_token=")[0]
            url = url.split("&event=")[0]
            url = url.replace("%2B", "+")
            url = url.replace("%2D", "-")
            url = url.replace("%2F", "/")
            url = url.replace("%3D", "=")
            url = url.replace("%3F", "?")
            #print url
            link = []
            link.append(name)
            link.append(url)
            links.append(link)
        return links

  
    # Fetches the subscriber count.
    def getSubs(self):
        e = self.s.driver.find_element_by_id("subscriber-count");
        if e.text != "":
            return e.text.replace("subscribers","").replace(" ", "")
            
    # Fetches the total views.
    def getViews(self):
        e = self.s.driver.find_element_by_xpath('//div[@id="right-column"]/yt-formatted-string[3]')
        if e.text != "":
            return e.text.replace("views","").replace(" ", "")
        
    # Fetches when joined
    def getJoined(self):
        e = self.s.driver.find_element_by_xpath('//div[@id="right-column"]/yt-formatted-string[2]')
        if e.text != "":
            return e.text.replace("Joined ","")
        
    # Turns the page.  
    def nextPage(self):
        el = self.s.driver.find_elements_by_class_name("yt-uix-button-content")
        for x in el:
            if x.text.find("Nast") != -1:
                x.click()
            else:
                pass

    # File I/O
    def saveLink(self,link):
        f = open("data/YoutubeChannelsParsed.Oink",'a')
        f.write(link+"\n")
        f.close()
        
    
p = Palantir()
f = open("data/YoutubeChannels.Oink",'r')
p.s.noProxy()

channels = f.read().split("\n")
f.close()
start = time.time()

i = 0.0
N = len(channels) - 1
for x in range(0, N):
    print "[", i + 1, "/", N,  "]: ", channels[x]
    p.browseChannel(channels[x])
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
        
        

