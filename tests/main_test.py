import unittest
from bin.crawler.main import GetUrl, GetPageContent

class MainTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_GetUrl(self):
        job_list_dict = {
            "domain":"https://powertofly.com",
            "path":"/jobs",
            "params":{
                "sort_by_published":"True",
                "keywords":"%22Software+Engineering%22+OR+Developer+OR+Engineer+OR+%22Backend+Developer%22+OR+%22Frontend+Developer%22+OR+%22Fullstack+Developer%22+OR+%22Mobile+Developer%22+OR+%22Game+Developer%22+OR+%22Engineering+Manager%22",
                "page":"{page}"
            }
        }
        url = GetUrl(job_list_dict,page=1)
        expected = "https://powertofly.com/jobs?sort_by_published=True&keywords=%22Software+Engineering%22+OR+Developer+OR+Engineer+OR+%22Backend+Developer%22+OR+%22Frontend+Developer%22+OR+%22Fullstack+Developer%22+OR+%22Mobile+Developer%22+OR+%22Game+Developer%22+OR+%22Engineering+Manager%22&page=1"
        self.assertEqual(url,expected)

    def test_GetPageContent(self):
        url = "https://powertofly.com"
        res = GetPageContent(url)
        self.assertEqual(res.status_code,200)

    def test_GetJobList(self):
        pass

    def test_GetJobDetail(self):
        pass

    def test_Write2Json(self):
        pass

    def test_CheckId(self):
        pass

if __name__ == '__main__':
    unittest.main()