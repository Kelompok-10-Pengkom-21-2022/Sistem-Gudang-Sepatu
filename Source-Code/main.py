import os
from function import _inputInt, _inputStr, readFile, writeFile, menuDisplay, showShoes, charLoop, tableHeader, oneCell, showOneShoe, _, buy, add

shoes = []
shoesCount = 0
file = None

# ======================================  MAIN PROGRAM ======================================

close = False
readFile()
doMain = 0
while not close :
    doMain = menuDisplay(_("main"))
    if doMain == 1:
        showShoes("all")
        os.system("pause")
    elif doMain == 2:
        doSearch = menuDisplay(_("search"))
        if doSearch == 0:
            continue
        elif doSearch == 1:
            showShoes("series")
        elif doSearch == 2:
            showShoes("collection")
        os.system("pause")
    elif doMain == 3:
        doBuy = menuDisplay(_("buy"))
        if doBuy == 0:
            continue
        elif doBuy == 1:
            buy()
            writeFile()
            os.system("pause")
    elif doMain == 4:
        doAdd = menuDisplay(_("add"))
        if doAdd == 0:
            continue
        elif doAdd == 1:
            add("new")
        elif doAdd == 2:
            add("stock")
        os.system("pause")                    
    elif doMain == 0:
        print()
        print("=====================================================================")
        print("                             Thank You! 👋😇")
        print("=====================================================================")

        close = True

# ======================================  CLOSE ======================================

