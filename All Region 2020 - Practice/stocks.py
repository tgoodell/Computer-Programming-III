def printStockInfo(filename):
    try:
        file=open(filename)
    except FileNotFoundError:
        print("ERROR: File '" + filename + "' does not exist.")
        return -1

    lines=file.readlines()[2:]

    out=""

    separator="+" + "-"*29 + "+" + "-" * 29 + "+" + "-" * 29 + "+" + "-" * 29 + "+" + "-" * 29 + "+" + "-" * 30 + "+\n"
    out+=separator + "| Date\t\t\t|\tClose/Last\t|\tVolume\t\t|\tOpen\t\t|\tHigh\t\t|\tLow\t\t |\n" + separator

    for line in lines:
        out+="| " + line.replace(",","\t\t|\t").replace("\n","") + "\t\t |\n"

    out+=separator

    return out.expandtabs(tabsize=10)

print(printStockInfo("gme.csv"))
print(printStockInfo("msft.csv"))