from bs4 import BeautifulSoup
from datetime import datetime

class JobDetail:
    def __init__(self,job_id, soup, json_data):
        self.job_id = job_id
        self.job_title = json_data['title']
        self.job_fulldesc = json_data['description']
        self.job_posttime = json_data['datePosted']
        self.comp_name = json_data['hiringOrganization']
        self.comp_url = soup.find("div",{"class":"company-name"}).find("a")['href']
        self.job_location = self.mapping(json_data,'jobLocation')
        self.skills = json_data['skills']

    def column_transform(self):
        self.job_fulldesc = BeautifulSoup(self.job_fulldesc, "html.parser").text
        self.job_posttime = int(datetime.strptime(self.job_posttime,'%a, %d %b %Y %H:%M:%S %Z').timestamp())
        self.comp_name = self.comp_name['name']
        self.comp_url = "https://powertofly.com"+self.comp_url
        self.job_location = [obj['address'] for obj in self.job_location]
        self.skills = self.skills if self.skills else []

    def get_json(self,add_dict=None):
        self.column_transform()
        json_data = {
            "JobId":self.job_id,
            "JobTitle":self.job_title,
            "JobFullDesc":self.job_fulldesc,
            "JobPostTime":self.job_posttime,
            "CompName":self.comp_name,
            "CompUrl":self.comp_url,
            "JobLocation":self.job_location,
            "Skills":self.skills
        }
        if add_dict:
            for k,v in add_dict.items():
                json_data[k] = v
        return json_data
    
    def mapping(self,dict,key):
        try:
            return dict[key]
        except:
            return ""
