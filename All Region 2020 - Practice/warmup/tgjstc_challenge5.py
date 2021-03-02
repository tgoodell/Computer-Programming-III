import urllib.request, urllib.error

report="Good and Bad URLs\n"+"-"*20+"\n"
file=open("url-list.txt")
for line in file:
    url=str(line.replace("\n",""))
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    try:
        con = urllib.request.urlopen(req)
    except:
        report+=url + " - bad.\n"
    else:
        report+=url + " - good.\n"

print(report)