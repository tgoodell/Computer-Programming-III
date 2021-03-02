import urllib.request, urllib.error
import re

def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print("| " + " | ".join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line)) + " |")

report=[]
file=open("url-list.txt")
for line in file:
    url=str(line.replace("\n",""))
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    try:
        con = urllib.request.urlopen(req)
    except:
        pass
    else:
        a=str(con.read())
        sites=(re.findall('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?',a))
        sitesPage=""
        for site in sites:
            site=list(site)
            proto,domain,page=site[0],site[1],site[2]
            sitesPage+=proto+"://"+domain+page+", "
        report.append((url,sitesPage))

finalReport="Hyperlink Report\n"+"-"*20+"\n"
count=1
for line in report:
    finalReport+="Website " + str(count) + ": " + line[0]+"\n"
    siteList=str(line[1:]).replace("(", "").replace(")", "").replace("'", "").replace("\n","")
    for site in siteList[:-2].split(", "):
        finalReport+="- "+site+"\n"
    count+=1
    # print(count)

print(finalReport)