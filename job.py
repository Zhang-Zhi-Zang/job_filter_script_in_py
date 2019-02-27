# -*- coding:utf-8 -*-　＃
import csv
import pickle
import sys,os,io
import re
import requests

reload(sys)
sys.setdefaultencoding( "utf-8" )

class m_job(object):

    def __init__(self,job_type,time_type,work_type,location,name,address,contact,email,phone,title,detail):
        self.job_type = job_type
        self.time_type = time_type
        self.work_type = work_type
        self.location = location
        self.name = name
        self.address = address
        self.contact = contact
        self.email = email
        self.phone = phone
        self.title = title
        self.detail = detail

baseurl = "https://www.chineseinsfbay.com/f/page_viewforum/f_29/items_36BAA3"


def page(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    f = open("/Users/zhang/Downloads/page.txt","w")
    f.write(response.text)
    f.close()

def joblist():
    f = open("/Users/zhang/Downloads/page.txt","r")
    lines = f.readlines()
    list = []
    job_urllist={}
    for line in enumerate(lines):
        if re.match('              <a href="/f/page_viewtopic/t_[0-9]*.html" class="title">',line[1]):
            lists= line[1].strip()
            list.append(lists)

    #list= ["/f/page_viewtopic/t_217340.html"]

    for i in range(len(list)) :
        url = re.search('/f/page_viewtopic/t_[0-9]*.html',list[i]).group()
        title = re.sub('.*class="title">',"",list[i])
        title = re.sub('</a><span></span>',"",title)
        job_urllist.update({url:title})

    for key in job_urllist:
        print key + " , " + job_urllist[key]

    f.close()
    os.remove("/Users/zhang/Downloads/page.txt")
    return job_urllist


def job(job_url):
    for key in job_url:
        page_job_filter = key
        url = baseurl + page_job_filter
        page(url)
        f = open("/Users/zhang/Downloads/page.txt", "r")
        lines = f.readlines()

        thejob = m_job("","","","","","","","","","","")
        thejoblist = []
        for line in enumerate(lines):
            if re.match('        <span><span style="color:#868686">类型: ', line[1]):
                thejob.job_type = re.sub('.* style="color:#868686">.* </span>',"",line[1])
                thejob.job_type = re.sub('</span>', "", thejob.job_type)
                thejoblist.append(thejob.job_type)
            elif re.match('        <span><span style="color:#868686">工作性质: ', line[1]):
                thejob.time_type = re.sub('.* style="color:#868686">.* </span>',"",line[1])
                thejob.time_type = re.sub('</span>', "", thejob.time_type)
                thejoblist.append(thejob.time_type)
            elif re.match('        <span><span style="color:#868686">行业: ', line[1]):
                thejob.work_type = re.sub('.* style="color:#868686">.* </span>',"",line[1])
                job.work_type = re.sub('</span>', "", thejob.work_type)
                thejoblist.append(thejob.work_type)
            elif re.match('        <span><span style="color:#868686">工作地点: ', line[1]):
                thejob.address = re.sub('.*span style="color:#868686">.* </span>',"",line[1])
                thejob.address = re.sub('</span>', "", thejob.address)
                thejoblist.append(thejob.address)
            elif re.match('        <span><span style="color:#868686">名称: ', line[1]):
                thejob.name = re.sub('<span><span style="color:#868686">.* </span>',"",line[1])
                thejob.name = re.sub('</span>', "", thejob.name)
                thejoblist.append(thejob.name)
            elif re.match('''        	<div class = 'frm_rent frm_contact'>''', line[1]):
                thejob.contact = re.sub('''.*frm_contact'><img src = \'''',"",line[1])
                thejob.contact = re.sub('\'></div>', "", thejob.contact)
                thejoblist.append(thejob.contact)
            elif re.match('''        	<div class = 'frm_rent frm_email'>''', line[1]):
                thejob.email = re.sub('''.*frm_contact'><img src = \'''',"",line[1])
                thejob.email = re.sub('\'></div>', "", thejob.email)
                thejoblist.append(thejob.email)
            elif re.match('''        	<div class = 'frm_rent frm_phone'>''', line[1]):
                thejob.phone = re.sub('''.*frm_contact'><img src = \'''',"",line[1])
                thejob.phone = re.sub('\'></div>', "", thejob.phone)
                thejoblist.append(thejob.phone)
            elif re.match('''        <div class="post_title">''', line[1]):
                thejob.title = re.sub('''        <div class="post_title">.*">''',"", line[1])
                thejob.title= re.sub('</h1></span></div>', "", thejob.title)
                thejoblist.append(thejob.title)
            elif re.match('''.*class='real-content''', line[1]):
                thejob.detail = re.sub('''		<p class='real-content' style='width: 790px;'>''',"", line[1])
                thejob.detail= re.sub('&nbsp;</p>', "", thejob.detail)
                thejob.detail = re.sub('<br>', "\n", thejob.detail)
                thejob.detail = re.sub('&nbsp', "", thejob.detail)
                thejob.detail = re.sub('</span>', "", thejob.detail)
                thejob.detail = re.sub('</p>', "", thejob.detail)
                thejoblist.append(thejob.detail)
                break

        if judge(thejob) == True:
            finalejob = io.open("/Users/zhang/Downloads/final.csv","ab+")
            csv_write = csv.writer(finalejob, dialect='excel')
            csv_write.writerow(thejoblist)
            finalejob.close()
        else:
            continue
        f.close()

    return

def judge(job):
    save = True
    dictlist = ['报税','SSN','按摩','工卡','保姆','幼儿园','销售','社会安全号']
    for i in range(0,len(dictlist)):
        if re.search(dictlist[i],job.detail):
            save = False
        if re.search(dictlist[i],job.title):
            save = False
    if re.search('招聘',job.job_type) == False:
        save = False
    return save



def urllist():
    page(baseurl)
    f = open("/Users/zhang/Downloads/page.txt", "r")
    lines = f.readlines()
    sizeint = 0
    urllists=[]
    urllists.append(baseurl)
    for line in enumerate(lines):
        if re.search('onclick="forumPageJumpTo',line[1]):
            size = re.sub('.*id="jumpto" size="',"",line[1])
            size = re.sub('"',"",size).strip()
            sizeint = int(size)
    for i in range(1,sizeint+1):
        start = i * 15
        pageurl = "/start_" + str(start)
        url = baseurl + pageurl
        urllists.append(url)
    return urllists


for i in range(0,len(urllist())):
    url = urllist()[i]
    print url
    page(url)
    joblists = joblist()
    job(joblists)















