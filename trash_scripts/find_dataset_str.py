import json
import os
from tqdm import tqdm
import fitz

'''
S1 拿到目录 -- 只要页码
S2 对每一篇检索 dataset/ data set 关键字，记录出现的页码，去重
S3 判断落的区间，拿到对应的文章标题，切出来对应的文章
S4 保存，导出一个json
'''


def handle_book(path, book_name, year, mark='sec'):
    pdf = fitz.open(path + '/' + book_name)
    papers_cate = json.loads(open(path + '/' + book_name + '_res_papers/final_contains.json','r+').read())
    err_titles = []

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

    def single_layer_get(bookmark_list, year, mark='sec'):
        lis = []
        for level, title, page in bookmark_list:
            if title.startswith(mark + year + '-'):
                lis.append(page)
        return lis

    def save_pdf2(sp, ep, title):
        new_doc = fitz.open()
        # 添加指定范围内的页面到新文档
        if ep - sp > 20:
            ep = sp + 20 # bug: bad item
        new_doc.insert_pdf(pdf, from_page=sp, to_page=ep)
        new_doc.save(path + '/' + book_name + '_res_papers/' + title.replace('/', '') + '.pdf')

    def get_paper_obj(index, lis, papers_cate, starts, err_titles):
        titles = [t['title'] for t in papers_cate]
        title = '_'.join(pdf.get_page_text(lis[index]).split(' ')[:10]).replace('\n', '')[:40]
        if title in titles:
            return
        papers_cate.append({'title': title, 'start': lis[index], 'end': lis[index + 1], 'in_reviwer': lis[index] - starts + 1})
        try:
            save_pdf2(lis[index], lis[index+1] - 1, title)
        except Exception as e:
            err_titles.append(title)

    kw = ['dataset', 'data set', 'andro-zoo database','cve database','mnist database','vulnerability database', 'ip2location database', 'maxmind database','geolocation database','nationalvulnerability database','netacuityedge database','election database','bluetoothsniffing database','mib database','jpegfile database','lfw database','forchheim database','dresden database','alaska2 database','pyroomacoustics database','acousticalsound database','ip2proxy database']

    # S1 拿到所有起始页面
    book_marks = pdf.get_toc()
    papers_start_pages = single_layer_get(book_marks, year, mark = mark)
    papers_start_pages.append(pdf.page_count)
    papers_start_pages = [i - 1 for i in papers_start_pages]

    # S2 保存含有dataset / data set的页码
    start_page = papers_start_pages[0]
    founds = []
    full_texts = []
    print('start to find in each paper\n')
    switch = False
    for page in tqdm(list(range(start_page, papers_start_pages[-1]))):
        this_page_text = pdf.get_page_text(page).replace('\n', '').lower()
        if page in papers_start_pages:
            switch = True
            this_page_text = this_page_text[max(this_page_text.find('introduction'),0):] #过滤标题
        elif 'references' in this_page_text:
            switch = False
        if switch:
            for it in kw:
                if it in this_page_text:
                    founds.append(page)
                    break

    if not os.path.exists(path + '/' + book_name + '_res_papers'):
        os.makedirs(path + '/' + book_name + '_res_papers')

    # S3 判断区间
    for page in founds:
        index = binary_search(page, papers_start_pages)
        get_paper_obj(index, papers_start_pages, papers_cate, starts=papers_start_pages[0], err_titles=err_titles)

    # S4 保存整体结果
    with open(path + '/' + book_name + '_res_papers/final_contains.json', 'w+') as f:
        f.write(json.dumps(papers_cate))

    with open(path + '/' + book_name + '_res_papers/final_err.json', 'w+') as f:
        f.write(json.dumps(err_titles))

    print('{} has {}/{} papers contains the kw'.format(book_name, len(papers_cate), len(papers_start_pages) - 1))

years = [str(20 + i) for i in range(5)]
book_names = ['sec20_full_proceedings.pdf', 'sec21_full_proceedings.pdf', 'sec22_full_proceedings.pdf', 'sec23_full_proceedings.pdf', 'sec24_full_proceedings.pdf']
for i, book_name in enumerate(book_names):
    if years[i] == '24':
        handle_book('/Users/admin/Downloads', book_name, years[i], mark='usenixsecurity')
    else:
        handle_book('/Users/admin/Downloads', book_name, years[i])
