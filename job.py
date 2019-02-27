# -*- coding:utf-8 -*-　＃
import csv
import pickle
import sys,os,io
import re
import requests

reload(sys)
sys.setdefaultencoding( "utf-8" )     #for Chinese 

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

baseurl = "https://www.chineseinsfbay.com/f/page_viewforum/f_29/items_36BAA3"   # 使用页面过滤器之后的部分结果页面地址


def page(url):  # 获取对应url的html 结果，并保存到page.txt中
    response = requests.get(url)
    response.encoding = 'utf-8'
    f = open("/Users/zhang/Downloads/page.txt","w")
    f.write(response.text)
    f.close()

def joblist(): # 从 page.txt 中逐行读取，使用re 正则表达式匹配单个工作详情的链接地址 
    f = open("/Users/zhang/Downloads/page.txt","r")
    lines = f.readlines()
    list = []
    job_urllist={}
    for line in enumerate(lines):   # 使用enumerate 读取到的每个line 结果为添加索引后的list如(32, '<div class="topline">\r\n')，所以具体的line 内容使用line[1]
        if re.match('              <a href="/f/page_viewtopic/t_[0-9]*.html" class="title">',line[1]):  # 使用re.match 获取符合规则的行，注意match 从行首完全匹配才算成功
            lists= line[1].strip()
            list.append(lists)    # 获取当前页面的每个工作信息的页面链接行，保存到list 中

    #list= ["/f/page_viewtopic/t_217340.html"]

    for i in range(len(list)) :   # 对于每行内容进行过滤，
        url = re.search('/f/page_viewtopic/t_[0-9]*.html',list[i]).group()    #提取具体的子页面的后缀链接
        title = re.sub('.*class="title">',"",list[i])   # 获取每个job 的名称描述，使用re.sub 去掉多余内容
        title = re.sub('</a><span></span>',"",title)  # 掐头去尾
        job_urllist.update({url:title})   # 保存为dictionary ，实际应用中不会使用到title 信息，可以和上一个for 循环合并只获取有用的子页面后缀链接即可

    for key in job_urllist:   # 打印信息，对于dictionary 需要自己写循环进行打印，此处打印调试方便 可以没有
        print key + " , " + job_urllist[key]

    f.close()
    os.remove("/Users/zhang/Downloads/page.txt")
    return job_urllist


def job(job_url):
    for key in job_url:   # 访问每个在列表中的工作详情页面 获取对应的信息，工作类型、性质、行业、描述、联系方式等
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
                thejoblist.append(thejob.job_type)   # 将工作的每项保存到list 数据
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
                break   # 工作详情描述在所有信息之后且与评论使用的正则命中规则相同，但描述在前，避免描述被评论覆盖，获取一次结果后跳出本次for 循环

        if judge(thejob) == True:      # 根据规则判断此次信息是否符合查找需求，如果符合保存到csv 文件
            finalejob = io.open("/Users/zhang/Downloads/final.csv","ab+")
            csv_write = csv.writer(finalejob, dialect='excel')
            csv_write.writerow(thejoblist)
            finalejob.close()
        else:
            continue
        f.close()

    return

def judge(job):  # 判断描述、title 中是否有命中过滤规则的词汇，有的话返回false 结果
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
    for line in enumerate(lines):  # 因为有多页结果，需要遍历每一页的工作，返回分页的链接后缀list
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


for i in range(0,len(urllist())):    #遍历每一页 每一页的每个工作，保存结果
    url = urllist()[i]
    print url
    page(url)
    joblists = joblist()
    job(joblists)















