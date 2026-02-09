import os
import json
import tldextract
from urllib.parse import urlparse

cookie_counts = {}
thirdParty_counts = {}

def getCookieforSite(entry):
    request_cookies = entry['request']['cookies']
    response_cookies = entry['response']['cookies']

    if request_cookies:
        for cookie in request_cookies:
            cookie_name = cookie['name']
            cookie_counts[cookie_name] = cookie_counts.get(cookie_name, 0) + 1

    if response_cookies:
        for cookie in response_cookies:
            cookie_name = cookie['name']
            cookie_counts[cookie_name] = cookie_counts.get(cookie_name, 0) + 1

def getThirdParty(entries, firstParty):
    for entry in entries:
        request_url = entry['request']['url']
        extractResult = tldextract.extract(urlparse(request_url).hostname) #Extract a bunch of info based on the url used in request
        extractedDomain = extractResult.domain #But get the actual domain, based on the request url.


        if firstParty.split(".")[0] not in extractedDomain: #firstparty.split(".")[0] will be google, yahoo, doubleclick, etc. If not in some extracted domain, must be a new domain.
            getCookieforSite(entry) #Get third party cookies
            thirdParty_counts[extractedDomain] = thirdParty_counts.get(extractedDomain, 0) + 1 #Will append based on extractedDomain, this is because tldextract (which should be correct) knows what properly is a different domain or not
        else:
            #print(extractedDomain + " IS FIRST PARTY TO "+ firstParty.split(".")[0])
            continue


if __name__ == "__main__":
    dirpath = r"C:\Users\Raph\Desktop\152A\Project2\AllHars"

    for filename in os.listdir(dirpath):
        f = open(os.path.join(dirpath, filename), 'r')
        data = json.load(f)
        entries = data['log']['entries']
        getThirdParty(entries, filename) 
        f.close()

    sorted_cookies = sorted(cookie_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_3P = sorted(thirdParty_counts.items(), key=lambda x: x[1], reverse=True)

    total_cookies = sum(count for _, count in sorted_cookies)
    total_thirdparties = sum(count for _, count in sorted_3P)

    print("\nTop 15 Cookie Counts of the 1000 HAR files:")
    for cookie_name, count in sorted_cookies[:15]:
        print(f"{cookie_name}: {count}")

    print("\nTotal Count of 3P Cookies: " + str(total_cookies))


    print("\n------------------------\n")

    print("Top 15 Third Parties of the 1000 HAR files:")
    for thirdparty_name, count in sorted_3P[:15]:
        print(f"{thirdparty_name}: {count}")

    print("\nTotal Count of third party domains: " + str(total_thirdparties))
