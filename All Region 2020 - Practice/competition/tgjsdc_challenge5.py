inputFile=open("gear_specs.csv")


# ['Gear Train', 'Position', 'Number of Teeth', 'Diameter (cm)']
for line in inputFile:
    (line.replace("\n","").split(","))
    # if



# {
#     “Gear Train 1”: {
#         “Gear Ratio”: 1.5,
#         “Gear Train Type”: “Torque”
#     },
#     “Gear Train 2”: {
#         “Gear Ratio”: 0.5,
#         “Gear Train Type”: “Speed”
#     },
#     “Gear Train 3”: {
#         “Gear Ratio”: 1.0,
#         “Gear Train Type”: “Balanced”
#     }
