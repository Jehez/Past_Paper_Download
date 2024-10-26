from requests import get
from bs4 import BeautifulSoup
from time import perf_counter as pc
from os import makedirs
from os.path import dirname
from time import sleep

website_root = "https://pastpapers.co/cie/" # dont change
root_path = r"C:\Users\sahej\OneDrive\Desktop\Past_Paper_Database" # change for local machine

subjects = ["Mathematics-9709","Mathematics-Further-9231","Physics-9702","Chemistry-9701","English-9093"] #take from pastpapers.co/cie website: exact copy
subject_codes = [9709,9231,9702,9701,9093]

needed_papers = { # needed papers for each subject
    "Mathematics-9709":[3,4],
    "Mathematics-Further-9231":[1,2,4],
    "Physics-9702":[4,5],
    "Chemistry-9701":[4,5],
    "English-9093":[1,2]
}

def get_paper_page_links(link):
    link = website_root+link
    response = get(link)
    data = BeautifulSoup(response.text,'html.parser')

    tags = data.find_all('a',class_="clearfix")
    all_links = []

    for tag in tags:
        year_info = tag.text
        if "20" not in year_info: continue
        year_info = tag.text[6:-3]
        link = tag['href']
        if "Feb" in link or "Mar" in link or "May" in link or "Jun" in link or "Oct" in link or "Nov" in link:
            all_links.append(link)
        else:
            all_links += get_paper_page_links(link)
    return all_links

def download_from_url(url, download_path,delay=5):
    with open(download_path, 'wb') as f:
        response = get(url, headers={'Accept-Encoding': 'identity, deflate, compress, gzip', 'Accept': '*/*','Connection': 'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'}) # no stream=True, that could be an issue
        f.write(response.content)
        response.close()
        sleep(delay)

def download_papers(link,subject,needed_paper_nums):
    link = website_root+link
    response = get(link)
    data = BeautifulSoup(response.text,'html.parser')

    tags = data.find_all('label',class_="headingwrap")

    for tag in tags:
        paper_code = tag.text[:-4].lower()

        if "label" in paper_code or len(paper_code)<4:   continue

        code_check = False
        for s_code in subject_codes:
            code_check = code_check or paper_code.startswith(str(s_code))
        if not code_check:  continue

        paper_info = paper_code.split('_')

        if paper_info[2] not in ['qp','ms','gt','er']:   continue # change if other docs are needed, ex: ci, pm etc., add file save format

        if paper_info[2] in ['qp','ms'] and '+' not in paper_code and len(paper_info)==4:
            paper_type = int(paper_info[3][0])
            if paper_type not in needed_paper_nums: continue
        
        paper_path = root_path+"\\"+subject+"\\20"+paper_info[1][1:]+"\\"
        
        if paper_info[1][0]=='m':   paper_path+="March\\"
        if paper_info[1][0]=='s':   paper_path+="Summer\\"
        if paper_info[1][0]=='w':   paper_path+="Winter\\"

        if paper_info[2]=='qp': paper_path+="Question_Paper\\Paper_"+paper_info[-1]+".pdf"
        elif paper_info[2]=='gt':   paper_path+="Grade_Threshold.pdf"
        elif paper_info[2]=='er':   paper_path+="Examiner_Report.pdf"
        else:
            if '+' in paper_code or len(paper_info)==3:   paper_path+="Combined_Marking_Scheme.pdf"
            else:   paper_path+="Marking_Scheme\\Paper_"+paper_info[-1]+".pdf"
        
        makedirs(dirname(paper_path),exist_ok=True)
        paper_url = link.replace("?dir=","")+"/"+tag.text
        download_from_url(paper_url,paper_path,delay=15)

        print("Downloaded",paper_code)

print("Started")
start = pc()
for sub in subjects:
    paper_page_links = get_paper_page_links("?dir=A-Level/"+sub)
    print("Got",len(paper_page_links),"paper page links for",sub)
    for l in paper_page_links:
        download_papers(l,sub,needed_papers[sub])
end = pc()
print(f"Finished downloading in {(end-start)/60} mins")