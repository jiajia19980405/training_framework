import json
import os
from tqdm import tqdm
import fitz
import shutil

'''
S1 拿到整个文件夹,以及对应的pdf
S2 打开pdf 寻找对应关键字
S3 记录出现的pdf标题,cp到新文件夹
S4 保存,导出一个json
'''

def handle_dir(path, year):
    papers = os.listdir(path + '/' + year)
    papers = [p for p in papers if not p.startswith('.')]
    kw = ['dataset', 'data set', "andro-zoo database",
          "cve database",
          "mnist database",
          "ip2location database",
          "maxmind database",
          "geolocation database",
          "nationalvulnerability database",
          "netacuityedge database",
          "election database",
          "bluetoothsniffing, database",
          "mib database",
          "jpegﬁle database",
          "lfw database",
          "lfw:a database",
          "forchheim database",
          "dresden database",
          "alaska2 database",
          "thealaska2 database",
          "pyroomacoustics database",
          "acousticalsound database",
          "ip2proxy database",
          "nist-4 database",
          "nist4 database",
          "clamavvirus database",
          "osv database"]
    founds = []
    files = []

    for paper in tqdm(papers):
        pdf = fitz.open(path + '/' + year + '/' + paper)
        is_found = False
        switch = False
        for page in range(pdf.page_count):
            if not is_found:
                this_page_text = pdf.get_page_text(page).replace('\n', ' ').lower()
                if page == 0:
                    switch = True
                    this_page_text = this_page_text[max(this_page_text.find('abstract—'), 0):]
                elif 'references' in this_page_text:
                    switch = False
                if switch:
                    for k in kw:
                        if k in this_page_text:
                            founds.append(paper)
                            is_found = True
                            break


    if not os.path.exists(path + '/' + year + '_res_papers'):
        os.makedirs(path + '/' + year + '_res_papers')

    for f in founds:
        shutil.copy(path + '/' + year + '/' + f, path + '/' + year + '_res_papers/' + f)

    return founds, len(founds), len(papers)

path = '/Users/dla/Desktop/PAPER_EXTRACT/'
conference = '46_JOC'
years = os.listdir(path + conference)
years = [year for year in years if year.startswith('20')]
years.sort()
print(years)
for year in years:
    founds, sum_find, sum_all = handle_dir(path + conference, year)

    if not os.path.exists('./res_json'):
        os.makedirs('./res_json')

    # S4 保存整体结果
    with open('./res_json/{}_{}_final_contains.json'.format(conference, year), 'w+') as f:
        f.write(json.dumps(founds))

    with open('./res_json/counters.json', 'a+') as f:
        f.write('{}_{} has {}/{} papers contains the kw\n'.format(conference, year, sum_find, sum_all))
        print('{}_{} has {}/{} papers contains the kw\n'.format(conference, year, sum_find, sum_all))


def get_outline(path):
    pdf = fitz.open(path)
    book_marks = pdf.get_toc()