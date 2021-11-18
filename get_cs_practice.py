import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}


def get_filename():
    file_name = input()
    try:
        if file_name.split(".")[1] != "pdf":
            print("请输入的时候带上.pdf后缀")
            get_filename()
    except IndexError:
        print("请输入的时候带上.pdf后缀")
        get_filename()
    return file_name


file_name = get_filename()

url = "https://papers.xtremepape.rs/CAIE/AS%20and%20A%20Level/Computer%20Science%20(9608)/" + file_name
r = requests.get(url, stream=True, headers=headers)
content = r.text
try:
    if content.split("%")[1].split("-")[0] != "PDF":
        print("请输入一个正确的文件名，文件没有找到")
except IndexError:
    print("请输入一个正确的文件名，文件没有找到")
with open(file_name, 'wb') as f:
    for chunk in r:
        f.write(chunk)
print("完成")
