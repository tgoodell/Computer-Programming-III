import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import ListedColormap
import seaborn as sns
from bs4 import BeautifulSoup
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

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
stateLookup=["Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Northern Mariana Islands", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "US Minor Outlying Islands", "Utah", "Vermont", "Virgin Islands", "Virginia", "Washington", "West Virgina", "Wisconsin", "Wyoming"]
statesToCount=("Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virgina", "Wisconsin", "Wyoming")
statePopLookup=[4903185,731545,55114,7278717,3017804,39512223,5758736,3565287,973764,705749,21477737,10617423,169721,1415872,1787065,12671821,6732219,3155070,2913314,4467673,4648794,1344212,6045680,6892503,9986857,5639632,2976149,6137428,1068778,1934408,3080156,1359711,8882190,2096829,19453561,10488084,762062,57917,11689100,3956971,4217737,12801989,3193694,1059361,5148714,884659,6829174,28995881,300,3205958,623989,104328,8535519,7614893,1792147,5822434,578759]
crimeLookup=["Advanced Fee", "Auction", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Criminal Forums", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware/Virus", "Malware/Scareware", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Overpayment", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Spoofing", "Tech Support", "Terrorism", "Virus", "Social Media", "Virtual Currency"]
crimeLookup2019=["Advanced Fee", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Criminal Forums", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware/Virus", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Overpayment", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Spoofing", "Tech Support", "Terrorism", "Social Media", "Virtual Currency"]
crimeLookup2018=["Advanced Fee", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware/Virus", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Overpayment", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Spoofing", "Tech Support", "Terrorism", "Social Media", "Virtual Currency"]
crimeLookup2017=["Advanced Fee", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Criminal Forums", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware/Virus", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Overpayment", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Spoofing", "Tech Support", "Terrorism", "Social Media", "Virtual Currency"]
crimeLookup2016=["Overpayment", "Advanced Fee", "Auction", "BEC/EAC", "Charity", "Civil Matter", "Confidence Fraud/Romance", "Corporate Data Breach", "Credit Card Fraud", "Crimes Against Children", "Criminal Forums", "Denial of Service/TDos", "Employment", "Extortion", "Gambling", "Government Impersonation", "Hacktivist", "Harassment/Threats of Violence", "Health Care Related", "IPR/Copyright and Counterfeit", "Identity Theft", "Investment", "Lottery/Sweepstakes/Inheritance", "Malware/Scareware", "Misrepresentation", "No Lead Value", "Non-payment/Non-Delivery", "Other", "Personal Data Breach", "Phishing/Vishing/Smishing/Pharming", "Ransomware", "Re-shipping", "Real Estate/Rental", "Tech Support", "Terrorism", "Virus", "Social Media", "Virtual Currency"]

crimeData2016=np.zeros((len(stateLookup),len(crimeLookup2016),len(categoryLookup)))
crimeData2017=np.zeros((len(stateLookup),len(crimeLookup2017),len(categoryLookup)))
crimeData2018=np.zeros((len(stateLookup),len(crimeLookup2018),len(categoryLookup)))
crimeData2019=np.zeros((len(stateLookup),len(crimeLookup2019),len(categoryLookup)))

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

def genScatterForAllYears(crime,category,filename="graph.png"):
    years=[]
    crimeSnippet=[]
    classes=[]

    if crime not in crimeLookup:
        print(str(crime) + " is not a valid crime.")
    if category not in categoryLookup:
        print(str(category) + " is not a valid category.")

    for year in yearLookup:
        if year=="2016":
            for state in stateLookup:
                crimeSnippet.append(calculatePerHundredThousand("2016",state,crime,category))
                years.append(year)
                classes.append(state)
        elif year=="2017":
            for state in stateLookup:
                crimeSnippet.append(calculatePerHundredThousand("2017", state, crime, category))
                years.append(year)
                classes.append(state)
        elif year=="2018":
            for state in stateLookup:
                crimeSnippet.append(calculatePerHundredThousand("2018",state,crime,category))
                years.append(year)
                classes.append(state)
        elif year=="2019":
            for state in stateLookup:
                crimeSnippet.append(calculatePerHundredThousand("2019",state,crime,category))
                years.append(year)
                classes.append(state)

    fig, scatter = plt.subplots(figsize = (19,11))
    sns.scatterplot(x=years, y=crimeSnippet, hue=classes,s=20)
    plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0,fontsize=7)
    plt.title(str(crime) + " " + str(category) + " for All Years")
    plt.xlabel("Year")
    plt.ylabel(category)
    plt.savefig(filename)

def genHorizontalBarGraph(year,crimez,category,filename="graph2.png"):
    plt.rcdefaults()
    states = statesToCount
    crimeSnippet = []

    for state in statesToCount:
        sumState=0
        for crime in crimeLookup2019:
            sumState+=calculatePerHundredThousand(year, state, crime, category)
        crimeSnippet.append(sumState / 4 * 10)

    crimeSnippet,states=zip( *sorted( zip(crimeSnippet, states) ) )
    crimeSnippet=crimeSnippet[::-1]
    states=states[::-1]

    # df = pd.DataFrame({'statez': states, 'y_poz': crimeSnippet})
    # df.sort_values('y_poz', inplace=True)
    plt.subplots(figsize=(19, 11))

    plt.barh(states, crimeSnippet)
    plt.title("Estimated " + str(crime) + " " + str(category) + " in the United States" + " - " + year, fontsize=20)
    plt.ylabel("States")
    plt.xlabel(category + " per 100,000 People")
    plt.savefig(filename)

def calculatePerHundredThousand(year,state,crime,category):
    return getDataPiece(year,state,crime,category)/statePopLookup[stateLookup.index(state)]*100000

def genAllBarCharts(year):
    for crime in crimeLookup:
        genHorizontalBarGraph(year, crime, "Victim Count",filename="graphs/" + str(crime).replace("/", "-") + "-graph.png")
        print(crime)

# crimeData2016,crimeData2017,crimeData2018,crimeData2019=loadAllData()
# genChartForAllYears("Identity Theft","Victim Loss")

def printReport(year,crime,category):
    states = statesToCount
    crimeSnippet = []

    for state in statesToCount:
        sumState = 0
        for crime in crimeLookup2019:
            sumState += calculatePerHundredThousand(year, state, crime, category)
        crimeSnippet.append(sumState / 4 * 10)

    crimeSnippet,states=zip( *sorted( zip(crimeSnippet, states) ) )
    crimeSnippet=crimeSnippet[::-1]
    states=states[::-1]

    for state in states:
        print(state + ": " + str(crimeSnippet[states.index(state)]))

crimeData2016,crimeData2017,crimeData2018,crimeData2019=loadAllData()

crimeSnippet=[]
for state in statesToCount:
    sumState=0
    for crime in crimeLookup2019:
        sumState += calculatePerHundredThousand("2019", state, crime, "Victim Count")
    crimeSnippet.append(sumState/2*5)

states=statesToCount

crimeSnippet,states=zip( *sorted( zip(crimeSnippet, states) ) )
crimeSnippet=crimeSnippet[::-1]
states=states[::-1]

for state in states:
    print(state + ", " + str(crimeSnippet[states.index(state)]))

plt.subplots(figsize=(19, 11))

plt.barh(states, crimeSnippet)
plt.title("Estimated Cybercrime in the United States, 2019", fontsize=20)
plt.ylabel("States")
plt.xlabel("Victim Count per 100,000 People")
plt.savefig("all-graph.png")

print("\subsection{State-level Cybercrime Data}\n")
print("\\begin{center}")
print("\\begin{tabular}{|l|l|}")
print("\hline")
print("State & Estimated Victim Count in 2019 PHT \\\ \hline")

for state in states:
    print(state + " & " + str(crimeSnippet[states.index(state)]) + " \\\ \hline")
print("\end{tabular}")
print("\end{center}")
print("\n\\newpage")

# volume=crimeData2019
#
# x = np.arange(volume.shape[0])[:, None, None]
# y = np.arange(volume.shape[1])[None, :, None]
# z = np.arange(volume.shape[2])[None, None, :]
# x, y, z = np.broadcast_arrays(x, y, z)

# Turn the volumetric data into an RGB array that's
# just grayscale.  There might be better ways to make
# ax.scatter happy.

# # Do the plotting in a single call.
# fig = plt.figure(figsize=(19, 11))
# ax = fig.gca(projection='3d')
# ax.scatter(x.ravel(),y.ravel(),z.ravel())
#
# plt.title("2019 Cybercrime Data Array Format",fontsize=20)
# plt.ylabel("Cybercrimes",fontsize=10)
# plt.xlabel("States",fontsize=10)
# ax.set_zlabel("Category",fontsize=10)
#
# plt.savefig("3dgraph.png")



# printReport("2019","Confidence Fraud/Romance", "Victim Count")
#
# print(len(crimeLookup2019))

# if True:
#     plt.rcdefaults()
#     states = statesToCount
#     crimeSnippet = []
#
#     for state in statesToCount:
#         sumState = 0
#         for crime in crimeLookup2019:
#             sumState += calculatePerHundredThousand("2019", state, crime, "Victim Loss")
#         crimeSnippet.append(sumState / 4 * 10)
#
#     crimeSnippet,states=zip( *sorted( zip(crimeSnippet, states) ) )
#     crimeSnippet=crimeSnippet[::-1]
#     states=states[::-1]
#
#     # df = pd.DataFrame({'statez': states, 'y_poz': crimeSnippet})
#     # df.sort_values('y_poz', inplace=True)
#     plt.subplots(figsize=(19, 11))
#
#     plt.barh(states, crimeSnippet)
#     plt.title("Estimated " + str("All Crime") + " " + str("Victim Loss") + " in the United States" + " - " + "2019", fontsize=20)
#     plt.ylabel("States")
#     plt.xlabel("Victim Loss" + " per 100,000 People")
#     plt.savefig("graph3.png")

# print("\subsection{Charts}")
# for crime in crimeLookup2019:
#     print("\subsubsection{" + crime + "}\n")
#     print("\\begin{figure}[h!]")
#     print("\centering")
#     print("\includegraphics[width=1\\textwidth]{bar-charts/" + str(crime).replace("/", "-") + "-graph.png}")
#     print("\caption{Estimated " + crime + " Cybercrime in 2019}")

# for crime in crimeLookup2019:
#     print("\subsection{" + crime + "}\n")
#     print("\\begin{center}")
#     print("\\begin{tabular}{|l|l|}")
#     print("\hline")
#     print("State & Estimated " + crime + " Victim Count in 2019 PHT \\\ \hline")
#     crimeSnippet = []
#     states = statesToCount
#     for state in statesToCount:
#         crimeSnippet.append(calculatePerHundredThousand("2019", state, crime, "Victim Count")/4*10)
#     crimeSnippet, states = zip(*sorted(zip(crimeSnippet, states)))
#     crimeSnippet = crimeSnippet[::-1]
#     states = states[::-1]
#     for state in states:
#         print(state + " & " + str(crimeSnippet[states.index(state)]) + " \\\ \hline")
#     print("\end{tabular}")
#     print("\end{center}")
#     print("\n\\newpage")

# am=calculatePerHundredThousand("2019","Arkansas","Identity Theft","Victim Count")
#
# print(am)
# print(am/4*10*statePopLookup[stateLookup.index("Arkansas")]/100000)
# print(getDataPiece("2019","Arkansas","Identity Theft","Victim Count"))

# labels = crimeLookup2019
# sizes = np.zeros((len(crimeLookup2019)))
# colors = (len(crimeLookup2019))*"red"
# explode=[]
#
# for state in statesToCount:
#     n=0
#     while n<len(crimeLookup2019):
#         sizes[n]+=crimeData2019[stateLookup.index(state)][n][0]
#         n+=1
#
# for n in range(len(crimeLookup2019)):
#     explode.append(0.1)
#
# # Plot
# plt.subplots(figsize=(19, 11))
# plt.pie(sizes, shadow=False, startangle=90, labels=labels,autopct='%1.1f%%',explode=explode)
# # plt.legend(patches, labels, loc="best")
# plt.title('Population Density Index')
#
# plt.axis('equal')
# plt.savefig("pie.png")





# addData("2019","Alabama")
# getAllStates("2019")
# fetchAllData()
# np.save("crimeData.npy",crimeData)
#
# crimeData=np.load("crimeData.npy")
# print(getDataPiece("2016", "Arkansas", "Social Media", "Victim Loss"))

# fetchAllData()
# saveAllData()


# printDataForStateAndYear("2019","Arkansas","Victim Loss")


# objects = stateLookup
# y_pos = np.arange(len(objects))
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