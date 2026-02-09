import os
import json
from urllib.parse import urlparse

thirdPartycookie_counts = {}
thirdParty_counts = {}

def getCookieforSite(entry):
    
    #These cookies are ones that are sent/read. So requests for them or responses for them.
    request_cookies = entry['request']['cookies']
    response_cookies = entry['response']['cookies']
    if request_cookies:
        #print("\nRequest Cookies:")
        for cookie in request_cookies:
            #print(f"  {cookie['name']}: {cookie['value']}")
            cookie_name = cookie['name']
            thirdPartycookie_counts[cookie_name] = thirdPartycookie_counts.get(cookie_name, 0) + 1

    if response_cookies:
        #print("\nResponse Cookies:")
        for cookie in response_cookies:
            #print(f"  {cookie['name']}: {cookie['value']}")
            cookie_name = cookie['name']
            thirdPartycookie_counts[cookie_name] = thirdPartycookie_counts.get(cookie_name, 0) + 1

def getThirdParty(entries, firstParty):
    for entry in entries:
        request_url = entry['request']['url']
        someUrl = urlparse(request_url).hostname #see what website is requested upon entering some first party website.
        if firstParty.split(".")[0] not in someUrl: #will be google, or amazon. Must be a 3rd if true
            thirdParty_counts[someUrl] = thirdParty_counts.get(someUrl, 0) + 1
            getCookieforSite(entry)
            
        else: #If the firstparty name is in the requesting url, it's not a tld. This obviously has some short comings, amazon can redirect to amzn, or salesforce can go to a subdomain like sf
            continue

if __name__ == "__main__":

    dirpath = r"C:\Users\Raph\Desktop\152A\Project2\AllHars"
    for filename in os.listdir(dirpath): #make sure your folder only has my hars
        f = open(dirpath + "\\" + filename, 'r')
        data = json.load(f)
        entries = data['log']['entries']
        getThirdParty(entries,filename) 
        f.close()

 
        

    sorted_cookies = sorted(thirdPartycookie_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_3P  = sorted(thirdParty_counts.items(), key=lambda x: x[1], reverse=True)
    
    total_cookies = sum(count for _, count in sorted_cookies)
    total_thirdparties = sum(count for _, count in sorted_3P)

    print("\nTop 15 3P Cookie Counts of the 1000 HAR files:")
    for cookie_name, count in sorted_cookies[:15]:
        print(f"{cookie_name}: {count}")

    print("\nTotal Count of 3P Cookies: " + str(total_cookies))

    print("\n------------------------\n")

    print("Top 15 Third Parties of the 1000 HAR files:")
    for thirdparty_name, count in sorted_3P[:15]:
        print(f"{thirdparty_name}: {count}")

    print("\nTotal Count of third party domains: " + str(total_thirdparties))



