import re

def printStockInfo(filename):
    try:
        file=open(filename)
    except FileNotFoundError:
        print("ERROR: File '" + filename + "' does not exist.")
        return -1

    lines=file.readlines()[2:]

    out=""

    sep=("+" + "-"*15)*6 + "+\n"
    out+=sep
    headings=["Date","Close/Last","Volume","Open","High","Low"]
    x=("|(:^15s)"*6+"|").format(*headings)
    out+=sep

    for line in lines:
        out+="| " + line.replace(",","\t\t|\t").replace("\n","") + "\t\t |\n"

    out+=sep

    return out.expandtabs(tabsize=10)

# print(printStockInfo("gme.csv"))
# print(printStockInfo("msft.csv"))

# w = uppercase,lowercase, and nums
re.findall("(\w+) (\d\d):(\d\d) $(\d+.\d*)",info)