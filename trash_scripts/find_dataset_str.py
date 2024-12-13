import json
import os
from tqdm import tqdm
import fitz
from collections import Counter

'''
S1 拿到目录 -- 只要页码
S2 对每一篇检索 dataset/ data set 关键字，记录出现的页码，去重
S3 判断落的区间，拿到对应的文章标题，切出来对应的文章
S4 保存，导出一个json
'''


def handle_book(path, book_name, year, conference, mark=None, level_f=None):
    pdf = fitz.open(path + '/' + book_name)
    papers_cate = json.load(
        open(path + '/res_json/{}_{}_final_contains.json'.format(conference, year))) if os.path.exists(
        path + '/res_json/{}_{}_final_contains.json'.format(conference, year)) else []
    err_titles = []
    save_page_arr = []

    def binary_search(number, lis):
        left, right = 0, len(lis) - 1
        while left <= right:
            mid = (left + right) // 2
            if lis[mid] <= number < lis[mid + 1]:
                return mid
            elif number < lis[mid]:
                right = mid - 1
            else:
                left = mid + 1
        return -1

    def single_layer_get(bookmark_list, year, mark):
        lis = []
        for level, title, page in bookmark_list:
            if title.startswith(mark + year + '-'):
                lis.append(page)
        return lis

    def single_layer_get_by_level(bookmark_list, level_f=None):
        lis = []
        for level, title, page in bookmark_list:
            text = pdf.get_page_text(page).lower()
            if level == level_f and 'abstract' in text:
                lis.append(page)
        lis.append(pdf.page_count)
        lis = [i - 1 for i in lis]
        return lis

    def auto_get_pages(bookmark_list, level_f):
        lis = []
        pages = []
        print('start to find begin page')
        for level, title, page in book_marks:
            text = pdf.get_page_text(page - 1).lower().replace('\n', '').replace(' ', '')
            if level == level_f:
                pages.append(page - 1)
            if level == level_f and 'abstract.' in text and title.replace(' ', '').lower() in text:
                lis.append(page - 1)
        lis.append(pdf.page_count)
        pages.append(pdf.page_count)
        return lis, [(pages[i], pages[i + 1]) for i in range(len(pages)) if
                     pages[i] in lis and pages[i] != pdf.page_count]

    def match_rule(text, text_next):
        return 'abstract.' in text and ('1 introduction' in text or '1 introduction' in text_next)

    def match_rule2(text, text_next):
        return 'abstract' in text and ('1 introduction' in text or '1 introduction' in text_next)

    def stupid_scan():
        lis = []
        flag = False
        tmp = -1
        for i in range(pdf.page_count - 1):
            text = pdf.get_page_text(i).replace('\n', ' ').lower()
            text_next = pdf.get_page_text(i + 1).replace('\n', ' ').lower()
            if match_rule2(text, text_next):
                flag = True
                tmp = i
            elif 'references' in text and flag:
                flag = False
                lis.append(tmp)
        lis.append(pdf.page_count)
        return lis[:-1], [(lis[i], lis[i + 1]) for i in range(len(lis) - 1)]

    def save_pdf2(sp, ep, title):
        new_doc = fitz.open()
        # 添加指定范围内的页面到新文档
        new_doc.insert_pdf(pdf, from_page=sp, to_page=ep)
        new_doc.save(path + '/' + year + '_res_papers/' + title.replace('/', '') + '.pdf')

    def get_paper_obj(si, papers_cate, starts, err_titles):
        titles = [t['title'] for t in papers_cate]
        title = '_'.join(pdf.get_page_text(si[0]).split(' ')[:10]).replace('\n', '')[:40]
        if title in titles:
            return
        papers_cate.append({'title': title, 'start': si[0], 'end': si[1], 'in_reviwer': si[0] - starts + 1})
        try:
            save_pdf2(si[0], si[1] - 1, title)
        except Exception as e:
            err_titles.append(title)

    # kw = ['dataset', 'data set', 'database']
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

    # S1 拿到所有起始页面
    # book_marks = pdf.get_toc()

    papers_start_pages, save_interval = stupid_scan()
    print(path, ' ', book_name)
    print(papers_start_pages)
    print(len(papers_start_pages))
    '''
    papers_start_pages, save_interval = auto_get_pages(book_marks, level_f = level_f)
    print(path, ' ',book_name)
    print(papers_start_pages)
    print(len(papers_start_pages)-1)
    '''
    # papers_start_pages = single_layer_get(book_marks, year, mark = mark)

    # S2 保存含有dataset / data set的页码
    start_page = papers_start_pages[0]
    founds = []
    print('start to find in each paper in {}\n'.format(book_name))
    switch = False
    for page in tqdm(list(range(start_page, papers_start_pages[-1]))):
        this_page_text = pdf.get_page_text(page).replace('\n', '').lower()
        if page in papers_start_pages:
            switch = True
            this_page_text = this_page_text[max(this_page_text.find('abstract.'), 0):]
        elif 'references' in this_page_text:
            switch = False
        if switch:
            for it in kw:
                if it in this_page_text:
                    founds.append(page)
                    break

    if not os.path.exists(path + '/' + year + '_res_papers'):
        os.makedirs(path + '/' + year + '_res_papers')

    # S3 判断区间
    print('start to save\n')
    for page in tqdm(founds):
        index = binary_search(page, papers_start_pages)
        si = [s for s in save_interval if s[0] == papers_start_pages[index]][0]
        get_paper_obj(si, papers_cate, starts=papers_start_pages[0], err_titles=err_titles)

    return papers_cate, err_titles, len(papers_cate), len(papers_start_pages)


path = '/Users/dla/Desktop/PAPER_EXTRACT/'
conference = '05_USENIX_Security_Symposium'
years = os.listdir(path + conference)
years = [year for year in years if year.startswith('20')]
years.sort()
print(years)
for year in years:
    books = []
    papers_cate = []
    err_titles = []
    sum_find = 0
    sum_all = 0
    if os.path.exists(path + '/' + conference + '/' + year):
        books = os.listdir(path + '/' + conference + '/' + year)
        books = [b for b in books if b.endswith('.pdf')]
        books.sort()
    for book_name in books:
        papers_cate_t, err_titles_t, sum_find_t, sum_all_t = handle_book(path + '/' + conference + '/' + year,
                                                                         book_name, year, conference, level_f=1)
        papers_cate.extend(papers_cate_t)
        err_titles.extend(err_titles_t)
        sum_find += sum_find_t
        sum_all += sum_all_t

    if not os.path.exists('./res_json'):
        os.makedirs('./res_json')

    # S4 保存整体结果
    with open('./res_json/{}_{}_final_contains.json'.format(conference, year), 'w+') as f:
        f.write(json.dumps(papers_cate))
    if len(err_titles) != 0:
        with open('./res_json/{}_{}_final_err.json'.format(conference, year), 'w+') as f:
            f.write(json.dumps(err_titles))

    with open('./res_json/counters.json', 'a+') as f:
        f.write('{}_{} has {}/{} papers contains the kw\n'.format(conference, year, sum_find, sum_all))
        print('{}_{} has {}/{} papers contains the kw\n'.format(conference, year, sum_find, sum_all))


def get_outline(path):
    pdf = fitz.open(path)
    book_marks = pdf.get_toc()