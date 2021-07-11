import os, sys, json, requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from bin.crawler.config import powertofly_url
from bin.crawler.detail import JobDetail
from bin.crawler.log import logs

job_list_dict = powertofly_url["job_list"]
job_detail_dict = powertofly_url["job_detail"]

def GetUrl(url_dict,job_id=None,page=None):
    domain = url_dict['domain']
    path = url_dict['path']
    params = url_dict['params']
    params = "?" + '&'.join([key+"="+params[key].format(page=page) for key in params.keys()]) if params else ""
    url = domain+path.format(id=job_id)+params
    return url

def GetPageContent(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    res = requests.get(url, headers=headers)
    return res

def GetJobList(url):
    res = GetPageContent(url)
    soup = BeautifulSoup(res.text,'html.parser')
    soup = soup.find_all("div",{"class":"js-elem"})
    if soup:
        job_list = [elem.find("a")['href'] for elem in soup if elem.find("a")] 
    else :
        job_list = []
    return job_list

def GetJobDetail(url):
    job_id = url.split('/')[-1]
    res = GetPageContent(url)
    soup = BeautifulSoup(res.text,'html.parser')
    json_data = eval(soup.find('script',{"type":"application/ld+json"}).string.strip('\n').replace('null','\"\"'))

    job_detail = JobDetail(job_id, soup, json_data)
    job_data = job_detail.get_json()
    return job_data

def Write2Json(data):
    filename = data['JobId']
    print(filename)
    with open(f'./output/job_{filename}.json', 'w+') as json_file:
        json.dump(data,json_file,indent=4)

def WriteIn1Json(data):
    with open(f'./output/job_{int(start_time)}_{int(end_time)}.json', 'w+') as json_file:
        json.dump(data,json_file,indent=4)

def CheckId(job_path):
    job = "job_"+job_path.split('/')[-1]+".json"
    if job not in os.listdir('./output/'):
        return 0
    return 1

def CheckIdInJson(job_path,data):
    job = job_path.split('/')[-1]
    if int(job) not in [int(ds['JobId'])for ds in data]:
        return 0
    return 1

def CheckDate():
    pass

def FinishDate():
    pass

def main(start_time,end_time):
    data = []
    page = 1
    status = 1
    while status:
        try:
            url = GetUrl(job_list_dict,page=page)
            job_list = GetJobList(url)
            log.info(f"page:{page}, {len(job_list)} jobs")

            for job_path in job_list:
                # if CheckId(job_path):
                # if CheckIdInJson(job_path,data):
                    # continue
                job_detail_dict['path'] = job_path
                url = GetUrl(job_detail_dict,page=page)
                job_data = GetJobDetail(url)
                post_time = job_data['JobPostTime']
                
                if post_time>end_time:
                    pass
                elif (post_time<=end_time)&(post_time>=start_time):
                    # Write2Json(job_data)
                    data.append(job_data)
                elif post_time<start_time:
                    status = 0
                    break
                else:
                    pass

            page += 1
        except Exception as e:
            log.exception(f"{page}-{job_path}",str(e))
            os._exit(0)
    
    WriteIn1Json(data)
    log.info(f"crawled {page} page(s)")

if __name__=="__main__":

    log = logs(project_name = "powertofly crawler")
    os.environ["TZ"] = "UTC"

    try:
        start_time = (datetime.strptime(sys.argv[1], '%Y%m%d')-timedelta(hours=8)).timestamp()
        end_time = (datetime.strptime(sys.argv[2], '%Y%m%d')+timedelta(days=1)-timedelta(seconds=1)-timedelta(hours=8)).timestamp()
    except:
        dt = datetime.strptime(str((datetime.now()+timedelta(hours=8)-timedelta(days=1)).date()), '%Y-%m-%d')
        start_time = (dt-timedelta(hours=8)).timestamp()
        end_time = start_time + 3600*24*2 - 1
    
    log.info(str(start_time)+' - '+str(end_time))
    main(start_time,end_time)
    os._exit(0)
    