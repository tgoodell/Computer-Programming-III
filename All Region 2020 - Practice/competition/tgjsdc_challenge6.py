print("Welcome!")
print("This program accepts a Hexilian temperature measurement and provides Earth measurements in Kelvin, Celsius, and Fahrenheit.")
print("-"*10 + "\n")

repeat=True
while repeat:
    hexilian=input("Please provide a whole number Hexilian Temperature reading: ")

    # Error Catching

    kelvin=int(str(int(hexilian,10)),6)/3
    celsius=kelvin-273
    fahrenheit=9/5*celsius+32

    if kelvin-int(kelvin)<0.5:
        kelvin=int(kelvin)
    else:
        kelvin-int(kelvin+1)
        
    if celsius-int(celsius)<0.5:
        celsius=int(celsius)
    else:
        celsius-int(celsius+1)
        
    if fahrenheit-int(fahrenheit)<0.5:
        fahrenheit=int(fahrenheit)
    else:
        fahrenheit-int(fahrenheit+1)

    print("Hexilian: " + str(hexilian))
    print("Kelvin: " + str(kelvin))
    print("Celsius: " + str(celsius))
    print("Fahrenheit: " + str(fahrenheit))

    badRepeatAnswer=True
    while badRepeatAnswer:
        repeatAnswer=input("Would you like to enter another list of integers (Y/N)? ")

        if repeatAnswer=="Y" or repeatAnswer=="y":
            badRepeatAnswer=False
            print("\nAwesome!\n---\n")
        elif repeatAnswer=="N" or repeatAnswer=="n":
            badRepeatAnswer=False
            repeat=False
        else:
            print("Invalid answer.")