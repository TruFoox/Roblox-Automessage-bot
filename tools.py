import os

print("Please Select a Tool")
print("")
print("1. UPC2C")
print("2. Cookie checker")
print("3. Privacy settings updater")
print("4. C+Email2C")
print("5. Non-verified email remover")
print("")
option = input("Tool Number: ")
print("")

if option == "1":
    os.system("python converter.py") 
elif option == "2":
    os.system("python cookiechecker.py") 
elif option == "3":
    os.system("python updater.py") 
elif option == "4":
    os.system("python emailremover.py") 
elif option == "5":
    os.system("python verifyfinder.py") 
else:
    print("Invalid tool number")
    input("Press Enter to close")
#All these tools are currently hidden