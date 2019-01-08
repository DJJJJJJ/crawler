import requests,pdfkit,os,re
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders

def save_as_pdf(url,name):
    os.chdir(r'E:\DJ\py_project\crawler\zhihu')
    file_name=str(name)+'.pdf'
    if os.path.exists(file_name) or os.path.exists(file_name.replace('XnewX','')):
        pass
    else:
        print(file_name)
        try:
            pdfkit.from_url(url, file_name)
            print('success')
        except Exception as e:
            print(e)
            print('failed')

def rename(name):
    rstr = r'[\/\\\:\*\?\<\>\|]'
    new_name = re.sub(rstr, "", name)
    new_name=new_name.replace('·','')
    return new_name

def send_email():
    path = r'E:\DJ\py_project\crawler\zhihu'
    name_list=[]
    for file in os.listdir(path):
        if 'XnewX' in file:
            name_list.append(file)
            time.sleep(10)
            file_path = os.path.join(path,file)
            msg = MIMEMultipart()
            msg['Subject'] = 'convert'  #邮件标题
            msg['From'] = _user #显示发件人
            msg['To'] = _to #接收邮箱
            attfile = file_path
            basename = os.path.basename(file_path)
            fp = open(attfile,'rb')
            att = MIMEText(fp.read(),'base64','gbk')
            att['Content-Type'] = 'application/octer-stream'
            att.add_header('Content-Disposition', 'attachment',filename=('gbk', '', basename))
            encoders.encode_base64(att)
            msg.attach(att)
            s = smtplib.SMTP_SSL("smtp.qq.com", 465,timeout = 30)#连接smtp邮件服务器,qq邮箱端口为465
            s.login(_user, _pwd)#登陆服务器
            s.sendmail(_user, _to, msg.as_string())#发送邮件
            s.close()
    for name in name_list:
        try:
            os.rename(name, name.replace('XnewX', ''))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    _user = "1521804976@qq.com"
    _pwd = "mabieleccfkyhaca"
    _to = "8615211177226@kindle.cn"
    header = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36'}
    url='http://daily.zhihu.com/'
    response=requests.get(url=url,headers=header)
    html=BeautifulSoup(response.text,'lxml')
    contents=html.find_all('a',attrs={'class':'link-button'})
    for content in contents:
        new_url=url.replace('/','')+content['href']
        name=content.select('span')[0].text+'XnewX'
        name=rename(name)
        save_as_pdf(new_url,name)
    send_email()
