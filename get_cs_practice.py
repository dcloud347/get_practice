import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}


def get_filename():
    file_name = input("请输入要找的文件名(+.pdf)")
    try:
        if file_name.split(".")[1] != "pdf":
            print("请输入的时候带上.pdf后缀")
            get_filename()
    except IndexError:
        print("请输入的时候带上.pdf后缀")
        get_filename()
    return file_name



def get_subject ():
    print("例如:Computer Science", "Biology", "Business", "Chemistry", "Economics", "Mathematics", "Further Math",
          "Physics")
    dict = {"Computer Science": "Computer%20Science%20(9608)/", "Biology": "Biology%20(9700)/",
            "Business": "Business%20(9609)/",
            "Chemistry": "Chemistry%20(9701)/", "Economics": "Economics%20(9708)/",
            "Mathematics": "Mathematics%20(9709)/",
            "Further Math": "Mathematics%20-%20Further%20(9231)/", "Physics": "Physics%20(9702)/"}
    subject = input("请输入学科名(首字母大写)")
    try:
        subject_dict = dict[subject]
        return subject_dict
    except KeyError:
        print("学科名称不匹配")
        get_subject()
subject_name = get_subject()
file_name = get_filename()
url = "https://papers.xtremepape.rs/CAIE/AS%20and%20A%20Level/"+subject_name+ file_name
r = requests.get(url, stream=True, headers=headers)
content = r.text
try:
    if content.split("%")[1].split("-")[0] != "PDF":
        print("请输入一个正确的文件名，文件没有找到")
        quit()
except IndexError:
    print("请输入一个正确的文件名，文件没有找到")
    quit()
with open(file_name, 'wb') as f:
    for chunk in r:
        f.write(chunk)
print("完成")
input()
