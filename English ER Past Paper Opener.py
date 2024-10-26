from time import sleep
from os import startfile


smap = {"m":"March","s":"Summer","w":"Winter"}

papers = '2' # paper code
sessions = 's'
variants = '123'

paper = True

start_year = 2024 #both inclusive
end_year = 2024

# driver code
for p in papers:
    for year in range(start_year,end_year+1):
        for s in sessions:
            try:
                input("Press enter for next examiner report")
                s_full = smap[s]
                startfile(rf'C:\Users\sahej\OneDrive\Desktop\Past_Paper_Database\English-9093\{year}\{s_full}\Examiner_Report.pdf')
                if not paper:   continue
                for variant in variants:
                    if s=='m' and variant!='2':   continue
                    input("Press enter for next paper")
                    startfile(rf'C:\Users\sahej\OneDrive\Desktop\Past_Paper_Database\English-9093\{year}\{s_full}\Question_Paper\Paper_{p}{variant}.pdf')
            except FileNotFoundError:
                print(f"File not found for {year} {s_full}")

input("Press enter to close")
input("Failsafe")