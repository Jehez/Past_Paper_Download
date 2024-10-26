from time import sleep
from os import startfile

# fixed data
subjects = ["Mathematics-9709","Mathematics-Further-9231","Physics-9702","Chemistry-9701","English-9093"]
smap = {"m":"March","s":"Summer","w":"Winter"}

# parameters
ind = 1
name = subjects[ind]

papers = '4' # paper code
sessions = 's'
variants = '123'

start_year = 2024 #both inclusive
end_year = 2024

wait = True
qp = True
ms = True

# driver code
for p in papers:
    for year in range(start_year,end_year+1):
        for s in sessions:
            for variant in variants:
                if s=='m' and variant!='2':   continue
                if ind==1 and s=='m':   continue
                s_full = smap[s]
                if wait:    input(f"Press enter for {year} {s_full} paper {p}{variant}")
                try:
                    if qp:
                        startfile(rf'C:\Users\sahej\OneDrive\Desktop\Past_Paper_Database\{name}\{year}\{s_full}\Question_Paper\Paper_{p}{variant}.pdf')
                        sleep(1)
                    if ms:
                        startfile(rf'C:\Users\sahej\OneDrive\Desktop\Past_Paper_Database\{name}\{year}\{s_full}\Marking_Scheme\Paper_{p}{variant}.pdf')
                        sleep(1)
                except Exception as e:
                    print(f"{year} {s_full} paper {p}{variant} not available")
                    #print(e)
                    continue

#failsafe (program ending closes browser window)
input("Press enter to close")
input("Failsafe")