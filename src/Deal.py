from colorama import init, Fore

def signalprint():
    init(autoreset=True)
    print(Fore.GREEN + '>>>',end='')


def RQI_Rank(RQI,Level):
    if Level==1:
        if RQI>=4.10 and RQI<=4.98:
            return 1
        elif RQI>=3.60 and RQI<4.10:
            return 2
        elif RQI>=2.50 and RQI<3.60:
            return 3
        elif RQI>=0 and RQI<2.50:
            return 4
    if Level in (2,3):
        if RQI>=3.60 and RQI<=4.98:
            return 1
        elif RQI>=3.00 and RQI<3.60:
            return 2
        elif RQI>=2.40 and RQI<3.00:
            return 3
        elif RQI>=0 and RQI<2.40:
            return 4
    if Level==4:
        if RQI>=3.40 and RQI<=4.98:
            return 1
        elif RQI>=2.80 and RQI<3.40:
            return 2
        elif RQI>=2.20 and RQI<2.80:
            return 3
        elif RQI>=0 and RQI<2.20:
            return 4


def PCI_Rank(PCI,Level):
    if Level==1:
        if PCI>=90 and PCI<=100:
            return 1
        elif PCI>=75 and PCI<90:
            return 2
        elif PCI>=65 and PCI<75:
            return 3
        elif PCI>=0 and PCI<65:
            return 4
    if Level in (2,3):
        if PCI>=85 and PCI<=100:
            return 1
        elif PCI>=70 and PCI<85:
            return 2
        elif PCI>=60 and PCI<70:
            return 3
        elif PCI>=0 and PCI<60:
            return 4
    if Level==4:
        if PCI>=80 and PCI<=100:
            return 1
        elif PCI>=65 and PCI<80:
            return 2
        elif PCI>=60 and PCI<65:
            return 3
        elif PCI>=0 and PCI<60:
            return 4


def PQI_Rank(PQI,Level):
    if Level==1:
        if PQI>=90 and PQI<=100:
            return 1
        elif PQI>=75 and PQI<90:
            return 2
        elif PQI>=65 and PQI<75:
            return 3
        elif PQI>=0 and PQI<65:
            return 4
    if Level in (2,3):
        if PQI>=85 and PQI<=100:
            return 1
        elif PQI>=70 and PQI<85:
            return 2
        elif PQI>=60 and PQI<70:
            return 3
        elif PQI>=0 and PQI<60:
            return 4
    if Level==4:
        if PQI>=80 and PQI<=100:
            return 1
        elif PQI>=65 and PQI<80:
            return 2
        elif PQI>=60 and PQI<65:
            return 3
        elif PQI>=0 and PQI<60:
            return 4