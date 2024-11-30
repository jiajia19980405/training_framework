import PyPDF2
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


def handle_book(path, book_name):
    file = open(path + '/' + book_name, 'rb+')
    reader = PyPDF2.PdfFileReader(file)
    pdf = fitz.open(path + '/' + book_name)
    outline = reader.outlines
    papers_cate = []
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

    def single_layer_get(bookmark_list, reader):
        lis = []
        for item in bookmark_list:
            if isinstance(item, PyPDF2.generic._data_structures.Destination):
                page_num = reader.getDestinationPageNumber(item)
                lis.append(page_num)
        return lis

    def save_pdf(sp, ep, title):
        writer = PyPDF2.PdfFileWriter()
        for page_num in range(sp, ep):
            page_in = reader.pages[page_num]
            writer.appendPagesFromReader(reader)

        with open(path + '/' + book_name + '_res_papers/' + title.replace('/', '') + '.pdf', 'wb') as wf:
            writer.write(wf)

    def save_pdf2(sp, ep, title):
        new_doc = fitz.open()
        # 添加指定范围内的页面到新文档
        #for page_num in range(sp, ep):
        new_doc.insert_pdf(pdf, from_page=sp, to_page=ep)
        new_doc.save(path + '/' + book_name + '_res_papers/' + title.replace('/', '') + '.pdf')

    def get_paper_obj(index, lis, papers_cate, starts, err_titles):
        titles = [t['title'] for t in papers_cate]
        title = '_'.join(reader.getPage(lis[index]).extractText().split(' ')[:10]).replace('\n', '')[:40]
        if title in titles:
            return
        paper_end = lis[index + 1]
        papers_cate.append({'title': title, 'start': lis[index], 'end': paper_end, 'in_reviwer': lis[index] - starts + 1})
        try:
            save_pdf2(lis[index], lis[index+1] - 1, title)
        except Exception as e:
            err_titles.append(title)


    # S1 拿到所有起始页面
    papers_start_pages = []
    for line in outline:
        papers_start_pages.extend(single_layer_get(line, reader))
    papers_start_pages.append(reader.numPages)

    # S2 保存含有dataset / data set的页码
    start_page = papers_start_pages[0]
    founds = []
    print('start to find in each paper\n')
    for page in tqdm(list(range(start_page, papers_start_pages[-1]))):
        this_page_text = reader.getPage(page).extractText().replace('\n', '').lower()
        if 'dataset' in this_page_text or 'data set' in this_page_text:
            founds.append(page)


    if not os.path.exists(path + '/' + book_name + '_res_papers'):
        os.makedirs(path + '/' + book_name + '_res_papers')

    # S3 判断区间
    #print('start_save\n')
    for page in founds:
        index = binary_search(page, papers_start_pages)
        get_paper_obj(index, papers_start_pages, papers_cate, starts=papers_start_pages[0], err_titles=err_titles)

    # S4 保存整体结果
    with open(path + '/' + book_name + '_res_papers/final_contains.json', 'w+') as f:
        f.write(json.dumps(papers_cate))

    with open(path + '/' + book_name + '_res_papers/final_err.json', 'w+') as f:
        f.write(json.dumps(err_titles))

handle_book('/Users/admin/Downloads/', 'sec20-full_proceedings.pdf')