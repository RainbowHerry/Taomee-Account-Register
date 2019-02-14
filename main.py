import urllib.request
import urllib.parse
import json
import random
import http.cookiejar
import tkinter
from PIL import Image,ImageTk
#请勿拿去商用，谢谢！
url = 'http://account-httpd.61.com/index.php'
cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

def get_icon():
    req_icon = urllib.request.Request(url=r"http://www.61.com/favicon.ico")
    reqo_icon = opener.open(req_icon).read()
    filename = r"icon.ico"
    f = open(filename,"wb")
    f.write(reqo_icon)
    f.close()
def get_captcha():
    req_auth = urllib.request.Request(url='http://account-httpd.61.com/index.php?cmd=1101&type=4&rnd='+str(random.random()))
    reqo_auth = opener.open(req_auth).read()
    filename = r"captcha.jpg"
    f = open(filename,"wb")
    f.write(reqo_auth)
    f.close()
def show_captcha(captcha_shower):
    get_captcha()
    im=Image.open("captcha.jpg")
    img=ImageTk.PhotoImage(im)
    captcha_shower.configure(image=img)
    captcha_shower.image=img
def register(code,password):
    values = {
    'gid': "7",
    'cmd': '1102',
    'seccode': code,
    'cfmpwd': password,
    'pwd': password,
    "tad":"none"
    }
    data = urllib.parse.urlencode(values).encode('utf-8')
    request = urllib.request.Request(url, data, headers)
    html = opener.open(request).read().decode('utf-8')
    return json.loads(html)
def register_btn(codeSV,passwordSV,captcha_shower,results):
    code=codeSV.get()
    password=passwordSV.get()
    result=register(code,password)
    if(result["result"]==0):
        results.insert(1.0,"米米号:"+str(result["userid"])+"\n")
    else:
        results.insert(1.0,"注册失败！[error code:"+str(result["result"])+"]\n")
    show_captcha(captcha_shower)
    codeSV.set("")

get_icon()
root = tkinter.Tk()
root.title("米米号注册机")
root.geometry("220x250+"+str(int(root.winfo_screenwidth()/2-110))+"+"+str(int(root.winfo_screenheight()/2-125)))
root.columnconfigure(0,weight=5,minsize=30)
root.columnconfigure(1,weight=20,minsize=50)
root.columnconfigure(2,weight=0,minsize=20)
root.rowconfigure(0,weight=0)
root.rowconfigure(1,weight=0)
root.rowconfigure(2,weight=1)
root.iconbitmap(r"icon.ico")
aut=tkinter.StringVar()
pswd=tkinter.StringVar()
tkinter.Label(root,text="验证码:").grid(column=0,row=0,sticky=tkinter.W+tkinter.N+tkinter.S+tkinter.E)
tkinter.Label(root,text="密码:").grid(column=0,row=1,sticky=tkinter.W+tkinter.N+tkinter.S+tkinter.E)
tkinter.Entry(root,textvariable=aut).grid(column=1,row=0,sticky=tkinter.W+tkinter.E)
tkinter.Entry(root,textvariable=pswd).grid(column=1,row=1,sticky=tkinter.W+tkinter.E)
captcha_shower=tkinter.Label(root)
captcha_shower.grid(column=2,row=0,sticky=tkinter.W+tkinter.N+tkinter.S+tkinter.E)
txt=tkinter.Text(root)
txt.grid(column=0,row=2,columnspan=3,sticky=tkinter.W+tkinter.N+tkinter.S+tkinter.E)
tkinter.Button(root,text="注册",command=lambda captcha_shower=captcha_shower,code=aut,password=pswd,results=txt:register_btn(code,password,captcha_shower,results)).grid(column=2,row=1,sticky=tkinter.W+tkinter.N+tkinter.S+tkinter.E)
show_captcha(captcha_shower)
root.mainloop()
