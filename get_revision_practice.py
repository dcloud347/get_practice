import requests
import pdfplumber
from PyPDF2 import PdfFileWriter, PdfFileReader
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}


def get_answer(file, questions, output):
    page_list = []
    result = []
    with pdfplumber.open(file) as pdf:
        for page in range(1, len(pdf.pages)):
            page_list.append(pdf.pages[page].extract_text())
    for question in questions:
        for page in range((len(page_list))):
            for i in page_list[page].split("\n"):
                line = i.strip()
                try:
                    if line[0] == question:
                        result.append(page + 1)
                        break
                except IndexError:
                    continue
    result = set(result)
    result = list(result)
    question_pages = result
    input2 = PdfFileReader(open(file, "rb"))

    def add_pdf(index):
        pages = input2.getNumPages()
        map(int, index)
        for i in range(pages):
            if i in index:
                output.addPage(input2.getPage(i))
        return output

    return add_pdf(question_pages)


def get_pdf(file, questions, output):
    def get_question(name, questions):
        list = []
        with pdfplumber.open(name) as pdf:
            for page in range(len(pdf.pages)):
                if page != 0:
                    list.append(pdf.pages[page].extract_text()[2:])
                else:
                    list.append(pdf.pages[page].extract_text())
        result = []
        questions_ = []
        for question in questions:
            questions_.append(question)
            questions_.append(str(int(question) + 1))
        for question in questions_:
            for page in range(1, len(list)):
                if question == list[page].lstrip()[0]:
                    result.append(page)
                    break
        for i in range(1, len(result), 2):
            result[i] = int(result[i]) - 1
        return result

    question_pages = get_question(file, questions)
    input1 = PdfFileReader(open(file, "rb"))

    def add_pdf(index):
        pages = input1.getNumPages()
        map(int, index)
        for i in range(pages):
            if i in index:
                output.addPage(input1.getPage(i))
        return output

    return add_pdf(question_pages)


data = []


def get_filename():
    endstr = "end"  # 重新定义结束符
    str = ""
    print("请输入文件名(输入完成请以end结尾)(默认下载markscheme)")
    print("示例:")
    print('''9608/11 Jun 18 Q4, Q7
9608/11 Jun 17 Q2
9608/12 Jun 18 Q2
9608/12 Jun 17 Q2c
9608/13 Jun 18 Q5, Q7
9608/12 Jun 16 Q1, Q3, 6
9608/11 Nov 17 Q5
9608/11 Nov 18 Q1a
9608/12 Nov 17 Q6
9608/13 Jun 17 Q3a, b, Q6a, b
9608/32 Jun 17 Q3a, b, Q6a
9608/31 Jun 18 Q7
9608/32 Jun 18 Q6a, b
9608/31 Nov 17 Q6a, b
9608/31 Jun 16 Q6
9608/31 Jun 17 Q3a, b, 6
9608/32 Jun 17 Q3a, b
9608/32 Jun 17 Q6
9608/32 Jun 18 Q7
9608/31 Nov 17 Q5ai
9608/31 Nov 17 Q6
9608/32 Nov 17 Q5a
9608/32 Nov 17 Q6
end''')
    print("请认真阅读以上指示")
    print("在此输入")
    for line in iter(input, endstr):  # 每行接收的东西
        str += line + " "  # 换行
    files = str.split("9608")
    files.pop(0)
    list = []

    for i in files:
        file = i.split(" ")
        end = file[0].strip("/")
        n = 3
        questions = []
        while file[n] != ' ':
            try:
                if file[n][0] == 'Q':
                    questions.append(file[n][1])
            except IndexError:
                break
            n += 1
        middle = file[1]
        if (middle == "Jun"):
            middle = "s"
        elif (middle == "Nov"):
            middle = "w"
        middle2 = file[2]
        list.append("9608" + "_" + middle + middle2 + "_qp_" + end + ".pdf")
        data.append(["9608" + "_" + middle + middle2 + "_qp_" + end + ".pdf", questions,"9608" + "_" + middle + middle2 + "_ms_" + end + ".pdf"])
        list.append("9608" + "_" + middle + middle2 + "_ms_" + end + ".pdf")
    return list


files_list = get_filename()
print("总共有" + str(len(files_list)) + "个文件")
print("正在下载")
length = len(files_list)
n = 0
for i in files_list:
    if os.path.isfile(i):
        print("文件已有")
        continue
    url = "https://papers.xtremepape.rs/CAIE/AS%20and%20A%20Level/Computer%20Science%20(9608)/" + i
    r = requests.get(url, stream=True, headers=headers)
    content = r.text
    try:
        if content.split("%")[1].split("-")[0] != "PDF":
            print("请输入一个正确的文件名，文件没有找到")
            n += 1
            continue
    except IndexError:
        print("请输入一个正确的文件名，文件没有找到")
        n += 1
        continue
    with open(i, 'wb') as f:
        for chunk in r:
            f.write(chunk)
    n += 1
    print(str((n / length) * 100) + "%完成")
print("所有文件传输完成")
answer1 = input("是否要截取问题并打包?是请输入y,否请输入n")
if answer1 == "y":
    print("正在整理")
    output1 = PdfFileWriter()
    output2 = PdfFileWriter()
    for file_info in range(len(data)):
        if file_info == 0:
            output1 = get_pdf(data[file_info][0], data[file_info][1], output1)
            output2 = get_answer(data[file_info][2], data[file_info][1], output2)
        else:
            output1 = get_pdf(data[file_info][0], data[file_info][1], output1)
            output2 = get_answer(data[file_info][2], data[file_info][1], output2)
    outputStream1 = open("Practice-output.pdf", "wb")
    outputStream2 = open("Answers-output.pdf", "wb")
    output1.write(outputStream1)
    output2.write(outputStream2)
elif answer1 == "n":
    pass
else:
    print("是否要截取问题并打包?是请输入y,否请输入n")
print("完成")
input("回车退出程序")
