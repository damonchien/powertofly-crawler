import logging, os

class logs(object):

    def __init__(self,project_name):        
        self.name = str(project_name)
        self.logpath = 'log/'+str(project_name)+'.log'
        self.logfolder = self.logpath.split('/')[0]
        if not os.path.exists(self.logfolder):
            os.mkdir(self.logfolder)

        self.log = logging.getLogger(self.name)
        self.log.setLevel(logging.DEBUG)
        # 時間都是存機器的時間,記錄當下call method 的function_name, line_num, 預設的project_name, level, msg
        self.formatter = logging.Formatter('{\"time\":\"%(asctime)s\",\"function_name\":\"%(funcName)s\",\"line_num\":\"%(lineno)d\", \"project_name\":\"%(name)s\", \"level\":\"%(levelname)s\", \"msg\":\"%(message)s\"}',datefmt='%Y-%m-%d %H:%M:%S')
        # 時間都是存機器的時間,預設的project_name, level, msg
        # self.formatter = logging.Formatter('{\"time\":\"%(asctime)s\", \"project_name\":\"%(name)s\", \"level\":\"%(levelname)s\", \"msg\":\"%(message)s\"}',datefmt='%Y-%m-%d %H:%M:%S')
        #寫file
        self.fh = logging.FileHandler(self.logpath, 'a', 'utf-8')
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(self.formatter)
        self.log.addHandler(self.fh)
        #跟print一樣
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(self.formatter)
        self.log.addHandler(self.ch)

    def debug(self,msg):     
        self.log.debug(str(msg).replace('\'','').replace('\"','')) 

    def info(self,msg):
        self.log.info(str(msg).replace('\'','').replace('\"',''))

    def warning(self,msg):     
        self.log.warning(str(msg).replace('\'','').replace('\"',''))

    def error(self,msg):     
        self.log.error(str(msg).replace('\'','').replace('\"',''))

    def exception(self,msg,e):
        self.log.exception(str(msg).replace('\'','').replace('\"','')+' -> '+(str(e).replace('\'','').replace('\"','').replace('\n',' ')),exc_info=False)
      
    