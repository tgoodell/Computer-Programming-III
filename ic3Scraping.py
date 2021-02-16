import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import ListedColormap
import seaborn as sns
from bs4 import BeautifulSoup

# Array Format
    # Year - 2016,2017,2018,2019 - No longer a thing
    # State
    # Crime Type
    # Categories
        # By Victim Count
        # By Victim Loss
        # By Subject Count
        # By Subject Loss
        # Age Group Count
        # Age Group Amount Loss

yearLookup=["2016", "2017", "2018", "2019"]
categoryLookup=["Victim Count", "Victim Loss", "Subject Count", "Subject Loss", "Age Group Count", "Age Group Amount Loss"]
ageRangeLookup=["Under 20", "20 - 29", "30 - 39", "40 - 49", "50-59", "Over 60"]
stateLookup=["Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisians", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Northern Mariana Islands", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "US Minor Outlying Islands", "Utah", "Vermont", "Virgin Islands", "Virginia", "Washington", "West Virgina", "Wisconsin", "Wyoming"]
crimeLookup=["Advanced Fee", "Auction", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Criminal Forums", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware/Virus", "Malware/Scareware", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Overpayment", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Spoofing", "Tech Support", "Terrorism", "Virus", "Social Media", "Virtual Currency"]
crimeLookup2019=["Advanced Fee", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Criminal Forums", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware/Virus", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Overpayment", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Spoofing", "Tech Support", "Terrorism", "Social Media", "Virtual Currency"]
crimeLookup2018=["Advanced Fee", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware/Virus", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Overpayment", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Spoofing", "Tech Support", "Terrorism", "Social Media", "Virtual Currency"]
crimeLookup2017=["Advanced Fee", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Criminal Forums", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware/Virus", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Overpayment", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Spoofing", "Tech Support", "Terrorism", "Social Media", "Virtual Currency"]
crimeLookup2016=["Overpayment", "Advanced Fee", "Auction", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Criminal Forums", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Tech Support", "Terrorism", "Virus", "Social Media", "Virtual Currency"]

# crimeData2016=np.zeros((len(stateLookup),len(crimeLookup2016),len(categoryLookup)))
# crimeData2017=np.zeros((len(stateLookup),len(crimeLookup2017),len(categoryLookup)))
# crimeData2018=np.zeros((len(stateLookup),len(crimeLookup2018),len(categoryLookup)))
# crimeData2019=np.zeros((len(stateLookup),len(crimeLookup2019),len(categoryLookup)))

crimeData=np.zeros((len(yearLookup)),(len(stateLookup),len(crimeLookup2019),len(categoryLookup)))

def fetchData(year,state):
    if year not in yearLookup:
        print("ERROR: Invalid year.")
        return

    if state not in stateLookup:
        print("ERROR: Invalid state.")
        return

    page=requests.get("http://www.ic3.gov/Media/PDF/AnnualReport/" + str(year) + "State/stats?s=" + str(stateLookup.index(state)+1))
    scrape=BeautifulSoup(page.content, "lxml")
    scrape=scrape.select("p")[0]
    badChars=["<p>", "</p>", "[", "]", "{", "}", ":", "c", "l","$"]
    scrape=str(scrape)
    for badChar in badChars:
        scrape=scrape.replace(badChar,"")

    scrape=scrape.split('"')

    while "," in scrape:
        scrape.remove(",")

    while "" in scrape:
        scrape.remove("")

    n=0
    while n<len(scrape):
       scrape[n]=scrape[n].replace(",","")
       n+=1

    scrape=[int(i) for i in scrape]

    return scrape

def addData(year,state):
    data=fetchData(year,state)
    print(state)
    n=0
    while n<len(data)-1:
        k=0
        if n<len(data)-12:
            if year=="2019":
                crimeData2019[stateLookup.index(state)][n%(len(crimeLookup2019))][n//(len(crimeLookup2019))]=data[n]
            elif year=="2018":
                crimeData2018[stateLookup.index(state)][n%(len(crimeLookup2018))][n//(len(crimeLookup2018))]=data[n]
            elif year=="2017":
                crimeData2017[stateLookup.index(state)][n%(len(crimeLookup2017))][n//37]=data[n]
            elif year=="2016":
                crimeData2016[stateLookup.index(state)][n%(len(crimeLookup2016))][n//(len(crimeLookup2016))]=data[n]
            else:
                print("Invalid year to add data. " + str(year) + " is not valid.")
        else:
            # where to add age info
            k+=1
        # print("Data: " + str(n))
        n+=1

def saveAllData():
    # np.delete(crimeData2016,crimeLookup2016.index("Social Media")+1)
    # np.delete(crimeData2017,crimeLookup2017.index("Social Media")+1)
    # np.delete(crimeData2018,crimeLookup2018.index("Social Media")+1)
    # np.delete(crimeData2019,crimeLookup2019.index("Social Media")+1)

    np.save("crimeData/crimeData2016.npy", crimeData2016)
    np.save("crimeData/crimeData2017.npy", crimeData2017)
    np.save("crimeData/crimeData2018.npy", crimeData2018)
    np.save("crimeData/crimeData2019.npy", crimeData2019)
    
def loadAllData():
    crimeData2016=np.load("crimeData/crimeData2016.npy")
    crimeData2017=np.load("crimeData/crimeData2017.npy")
    crimeData2018=np.load("crimeData/crimeData2018.npy")
    crimeData2019=np.load("crimeData/crimeData2019.npy")

    return crimeData2016,crimeData2017,crimeData2018,crimeData2019

def getDataPiece(year,state,crime,category):
    if category=="Age Group Count" or category=="Age Group Amount Loss":
        print("Retrieval not supported yet. Cannot produce " + category + ".")
    elif category in categoryLookup:
        if year=="2016":
            return crimeData2016[stateLookup.index(state)][crimeLookup2016.index(crime)][categoryLookup.index(category)]
        elif year=="2017":
            return crimeData2017[stateLookup.index(state)][crimeLookup2017.index(crime)][categoryLookup.index(category)]
        elif year=="2018":
            return crimeData2018[stateLookup.index(state)][crimeLookup2018.index(crime)][categoryLookup.index(category)]
        elif year=="2019":
            return crimeData2019[stateLookup.index(state)][crimeLookup2019.index(crime)][categoryLookup.index(category)]
        else:
            print("Invalid year. No data for " + str(year) + ".")
    else:
        print("Invalid category. " + str(category) + " is not found.")

def getAllStates(year):
    for state in stateLookup:
        addData(year,state)

def fetchAllData():
    for year in yearLookup:
        getAllStates(year)
        print(year)

def printDataForStateAndYear(year,state,category):
    if category not in categoryLookup:
        print("Invalid category " + str(category) + ". Cannot printout data for state and year.")
    else:
        if year=="2016":
            for crime in crimeLookup2016:
                print(str(crime) + " - " + str(getDataPiece(year,state,crime,category)))
        elif year=="2017":
            for crime in crimeLookup2017:
                print(str(crime) + " - " + str(getDataPiece(year,state,crime,category)))
        elif year=="2018":
            for crime in crimeLookup2018:
                print(str(crime) + " - " + str(getDataPiece(year,state,crime,category)))
        elif year=="2019":
            for crime in crimeLookup2019:
                print(str(crime) + " - " + str(getDataPiece(year,state,crime,category)))
        else:
            print("Invalid year " + str(year) + ". Cannot printout data for state and year.")

# addData("2019","Alabama")
# getAllStates("2019")
# fetchAllData()
# np.save("crimeData.npy",crimeData)
#
# crimeData=np.load("crimeData.npy")
# print(getDataPiece("2016", "Arkansas", "Social Media", "Victim Loss"))

# fetchAllData()
# saveAllData()

crimeData2016,crimeData2017,crimeData2018,crimeData2019=loadAllData()
# printDataForStateAndYear("2019","Arkansas","Victim Loss")


# objects = stateLookup
# y_pos = np.arange(len(objects))
performance = []
#
# n=0
# while n<len(stateLookup):
#    performance.append(crimeData2016[n][0][0])
#    n+=1
#
# x = []
# values=[]
# for state in stateLookup:
#     x.append(2016)
#     values.append(2)
# y = performance
# classes = stateLookup
#
# colours = ListedColormap(['r','b','g'])
# scatter = plt.scatter(x, y,c=values, cmap=colours)
# plt.legend(handles=scatter.legend_elements()[0], labels=classes)

# x = np.linspace(-1,1,100)
#
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
#
# #Plot something
# for state in stateLookup:
#     ax.plot(2016, performance[stateLookup.index(state)], color='red', ls="-", label=state)

# ax.plot(x,x, color='red', ls="-", label="$P_1(x)$")
# ax.plot(x,0.5 * (3*x**2-1), color='green', ls="--", label="$P_2(x)$")
# ax.plot(x,0.5 * (5*x**3-3*x), color='blue', ls=":", label="$P_3(x)$")

# ax.legend()
# plt.show()
x=[]
y=[]
classes=[]
colors=[]
n=0
while n<len(stateLookup):
   y.append(crimeData2016[n][0][0])
   x.append("2016")
   classes.append(stateLookup[n])

   n+=1
n=0
while n<len(stateLookup):
   y.append(crimeData2017[n][0][0])
   x.append("2017")
   classes.append(stateLookup[n])

   n+=1
n=0
while n<len(stateLookup):
   y.append(crimeData2018[n][0][0])
   x.append("2018")
   classes.append(stateLookup[n])

   n+=1
n=0
while n<len(stateLookup):
   y.append(crimeData2019[n][0][0])
   x.append("2019")
   classes.append(stateLookup[n])

   n+=1

fig, scatter = plt.subplots(figsize = (19,11))
sns.scatterplot(x=x, y=y, hue=classes,s=20)
plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0,fontsize=7)
plt.title("Advanced Fee Victim Count")
plt.xlabel("Year")
plt.ylabel("Number of Victims")
plt.savefig("mygraph.png")

def genChartForAllYears(crime):
    years=[]
    crimeSnippet=[]
    classes=[]

    for year in yearLookup:
        exec("crimeData")
        for state in stateLookup:
            y.append(crimeData2016[n][crimeLookup.index(crime)][0])
            x.append(year)
            classes.append(state)

# print(crimeData2016)

# printVictimLoss("2016","Arkansas")

# print(fetchData("2017","Arkansas"))


# s = str(s).replace("<p>","").replace("</p>","").replace("[","").replace("]","").replace("c","").replace("l","").replace(":","")
# s=np.array(s)
# # print(s[0])
# print(s)
# print(len(s))

# text=[[["1,561","3,523","54","124","2,206","235","1,966","161","0","132","1,983","6,612","32","1,928","2","2,163","38","392","1,937","400","593","271","793","5,476","8,018","2,186","2,325","5,377","2,707","303","125","2,376","2,890","1,775","11"],["3,925","4,427"],["$13,542,429","$263,280,775","$257,159","$5,251,582","$107,853,977","$6,064,748","$17,519,988","$793","$0","$164,652","$6,440,960","$26,675,566","$88,246","$29,053,752","$0","$2,692,596","$228,972","$3,617,279","$32,127,429","$37,819,776","$7,871,344","$215,843","$1,850,282","$0","$26,755,670","$5,480,991","$9,715,527","$17,672,566","$6,005,044","$1,448,357","$174,845","$56,285,319","$58,875,334","$7,706,581","$11,108"],["$11,864,875","$28,973,519"],["896","562","25","119","1,110","71","906","46","0","30","983","783","9","300","0","952","17","199","699","318","232","60","454","1,743","4,074","691","1,057","1,711","750","25","129","909","802","856","2"],["1,147","474"],["$7,547,188","$31,095,390","$99,110","$15,692,683","$46,198,807","$3,326,746","$7,637,627","$200","$0","$10,596","$4,485,530","$3,572,557","$1,658","$6,622,540","$0","$1,180,858","$107,055","$2,398,648","$11,709,827","$21,721,653","$2,190,447","$33,176","$1,661,202","$0","$27,009,645","$1,821,853","$5,440,103","$7,700,878","$2,345,166","$76,345","$374,772","$9,413,584","$12,050,817","$6,511,664","$0"],["$8,333,412","$5,367,577"]],[{"c":"1,433","l":"$6,253,235"},{"c":"6,164","l":"$23,629,945"},{"c":"7,303","l":"$54,257,512"},{"c":"7,875","l":"$92,849,219"},{"c":"6,142","l":"$119,963,383"},{"c":"8,594","l":"$166,648,923"}]]

# text=[int(s) for s in soup.split() if s.isdigit()]
# print(text[0][8][0])