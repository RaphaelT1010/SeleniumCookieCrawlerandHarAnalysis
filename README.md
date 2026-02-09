**Overview**

A Python script called seleniumcrawler.py accesses the top 1,000 websites of the internet via editedtop-1m.csv. The script would then collect its HTTP information via HAR files, using Selenium and browsermobproxy. A VIM could be used so a system could still do other things, as this script takes several hours. (instead, a second spare laptop was used)

Created a second Python script (called haranalysis.py) which analyzed these HAR files in order to extract the third-party cookies present and the counts of each one across all 1,000 websites.

Implemented error handling and robustness in the script (websites would sometimes be inaccessible from other countries, take too long to load, or a bad url)

GPT versions are included as further transparency (project was made in a course where ChatGPT versions were also required)

