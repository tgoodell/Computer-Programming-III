import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# Array Format
    # Year - 2016,2017,2018,2019
    # State
    # Crime Type
    # Stats - Tuple (By Victim Count, By Victim Loss, By Subject Count, By Subject Loss)

crimeData=np.zeros((4,57,36,4))
yearLookup=["2016", "2017", "2018", "2019"]
stateLookup=["Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisians", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Northern Mariana Islands", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "United States Minor Outlying Islands", "Utah", "Vermont", "Virgin Islands", "Virginia", "Washington", "West Virgina", "Wisconsin", "Wyoming"]
crimeLookup=['Advanced Fee', 'Identity Theft', 'BEC/EAC', 'Investment', 'Charity', 'Lottery/Sweepstakes/Inheritance', 'Civil Matter', 'Malware/Scareware/Virus', 'Confidence Fraud/Romance', 'Misrepresentation', 'Corporate Data Breach', 'No Lead Value', 'Credit Card Fraud', 'Non-payment/Non-Delivery', 'Crimes Against Children', 'Other', 'Criminal Forums', 'Overpayment', 'Denial of Service/TDos', 'Personal Data Breach', 'Employment', 'Phishing/Vishing/Smishing/Pharming', 'Extortion', 'Ransomware', 'Gambling', 'Re-shipping', 'Government Impersonation', 'Real Estate/Rental', 'Hacktivist', 'Spoofing', 'Harassment/Threats of Violence', 'Tech Support', 'Health Care Related', 'Terrorism', 'Social Media', 'Virtual Currency']

print(crimeLookup.index("Charity"))

# print(len(stateLookup))

elimDiscriptors="*These descriptors relate to the medium or tool used to facilitate the crime, and are used by the IC3 for tracking purposes only. They are available only after another crime type has been selected."

# data=pd.read_html("http://www.ic3.gov/Media/PDF/AnnualReport/2019State/StateReport.aspx#?s=5")
# pd.read_html(requests.get("http://www.ic3.gov/Media/PDF/AnnualReport/2019State/StateReport.aspx#?s=5").content)[0].to_csv("data.csv")

# data[0].to_csv("data.csv")

def generateData(year,state):
    pd.read_html(requests.get("http://www.ic3.gov/Media/PDF/AnnualReport/" + str(year) + "State/StateReport.aspx#?s=" + str(stateLookup.index(state))).content)[0].to_csv("data.csv")

def addData(fileArray,year,state):
    newData=np.array([])

    for item in fileArray:
        newData=np.append(newData,item)

    prettyData=[]

    n=0
    while n<len(newData):
        if n%5==0 or newData[n]==elimDiscriptors or newData[n]=="Descriptors*" or newData[n]=="nan":
            pass
        else:
            prettyData.append(newData[n])
        n+=1

    dataStats=[]
    nameStats=[]

    n=0
    while n<len(prettyData):
        if n%2==1:
            dataStats.append(prettyData[n])
        else:
            nameStats.append(prettyData[n])
        n+=1

    n=0
    while n<len(dataStats):
        crimeData[yearLookup.index(year)][stateLookup.index(state)][crimeLookup.index(nameStats[n])][0]=dataStats[n]
        n+=1

# generateData(2019,"Arkansas")
# result=pd.read_csv('data.csv', sep=',').dropna()
# result=np.array(result)
# addData(result,"2019","Arkansas")
#
# generateData(2019,"Alabama")
# result=pd.read_csv('data.csv', sep=',').dropna()
# result=np.array(result)
# addData(result,"2019","Alabama")
#
# print(crimeData[3][0][4][0])
# print(crimeData[3][4][4][0])

# URL=f'https://www.ic3.gov/Media/PDF/AnnualReport/2019State/StateReport.aspx#?s=11'
df = pd.read_html("https://www.ic3.gov/Media/PDF/AnnualReport/2018State/stats?s=11")
# df=requests.get(URL)
# soup = BeautifulSoup(df.content, 'html.parser')
print(df)