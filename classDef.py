import re
import array
import csv

global deciPat
global FILE_INFO
global DEV_INFO
global COND_INFO
global TIME_INFO
global CALI_INFO
global HIAC_INFO
global COMMENT_INFO
global TAG_INFO
global DATA_INFO
global UNKN_INFO

FILE_INFO       =1
DEV_INFO        =2
COND_INFO       =4
TIME_INFO       =8
CALI_INFO       =16
HIAC_INFO       =32
COMMENT_INFO    =64
TAG_INFO        =128
DATA_INFO       =256
UNKN_INFO       =512

decimal_pattern=re.compile(r'-?\d+\.\d*')

class sbdHead():
    def __init__(self):
        self.file=None
        # inner variable 
        self.state=0 # 1: file information
                # 2: hanwa,esd
                # 3: condition
                # 4: time
                # 5: calibration information
                # 6: unkown
                # 7: high accurancy
                # 8: comment
                # 20: data
                # -1: error format
        #file info     :1
        self.file_source=None
        self.version=None
        #device info    :2
        self.manufactory=None
        self.type=None
        #condition    :4
        self.pulse_width=None
        self.up_width=None
        self.bias=(None,None,None,None)
        #time        :8
        self.start_time=None
        self.end_time=None
        #calibration        :16
        self.cali_arg1=None
        self.cali_arg2=None
        self.short_file=None
        self.open_file=None
        self.base_file=None
        #unknown        :reversed
        #High Accurancy    :32:
        self.high_accurancy=False
        #Comment        :64
        self.comment=None
        #tag        :128
        self.tag=(None,None,None,None,None,None)
        #data        :256
        self.data=None
    
    def reset(self):
        self.file=None
        self.state=0 
        self.file_source=None
        self.version=None
        self.manufactory=None
        self.type=None
        self.pulse_width=None
        self.up_width=None
        self.bias=(None,None,None,None)
        self.start_time=None
        self.end_time=None
        self.cali_arg1=None
        self.cali_arg2=None
        self.short_file=None
        self.open_file=None
        self.base_file=None
        self.high_accurancy=False
        self.comment=None
        self.tag=(None,None,None,None,None,None)
        self.data=None
        
    def loadFileInfo(self,line):
        if not self.state&FILE_INFO:
            try:
                self.file_source=re.findall(r'^[^,]*\.sbd',line)[0]
                self.version=re.findall(r'\,([^,]*$)',line)[0]
                self.state=self.state|FILE_INFO
                return True
            except:
                pass
        return False
            
    def loadDevInfo(self,line):
        if self.state&FILE_INFO:
            if not self.state&DEV_INFO:
                try:
                    self.manufactory=re.findall(r'(^[^,]*)\,',line)[0]
                    self.type=re.findall(r'\,([^,]*$)',line)[0]
                    self.state=self.state|DEV_INFO
                    return True
                except:
                    pass
        return False
                
    def loadCond(self,line):
        if self.state&DEV_INFO:
            if not self.state&COND_INFO:
                try:
                    self.pulse_width=re.findall(r'^(\d+ns)',line)[0]
                    self.up_width=re.findall(r'\,(\d+ns)',line)[0]
                    self.bias=re.findall(r'\,(U1[^,]*|[^,*]$)',line)
                    self.state=self.state|COND_INFO
                    return True
                except:
                    pass
        return False
    
    def loadTime(self,line):
        if self.state&COND_INFO:
            if not self.state&TIME_INFO:
                try:
                    temp=re.split(r',',line)
                    if len(temp)==2:
                        self.start_time=temp[0]
                        self.end_time=temp[1]
                        self.state=self.state|TIME_INFO
                        return True
                except:
                    pass
        return False
    
    def loadCali(self,line):
        if self.state&TIME_INFO:
            if not self.state&CALI_INFO:
                try:
                    temp=re.split(r',',line)
                    if len(temp)==5:
                        self.cali_arg1=temp[0]
                        self.cali_arg2=temp[1]
                        self.short_file=temp[2]
                        self.open_file=temp[3]
                        self.base_file=temp[4]
                        self.state=self.state|CALI_INFO
                        return True
                except:
                    pass
        return False
    
    def loadUnknow(self,line):
        if self.state&CALI_INFO:
            if not self.state&TAG_INFO:
                try:
                    pass
                except:
                    pass
        return False
        
    def loadComment(self,line):
        if self.state&CALI_INFO:
            if not self.state&TAG_INFO:
                try:
                    pass
                except:
                    pass
        return False
                
    def loadHiAc(self,line):
        if self.state&CALI_INFO:
            if not self.state&TAG_INFO:
                try:
                    if re.match(r'^HighAccuracy,True',line) is not None:
                        self.high_accurancy=True
                        self.state=self.state|HIAC_INFO
                        return True
                except:
                    pass
        return False
    
    def loadTag(self,line):
        if self.state&CALI_INFO:
            if not self.state&TAG_INFO:
                try:
                    if re.match(r'^Point,Zap voltage',line) is not None:
                        self.tag=re.split(r',', line)
                        self.state=self.state|TAG_INFO
                        return True
                except:
                    pass
        return False
    
    def collectInfo(self,file_in):
        self.file=file_in
        if not self.loadFileInfo(file_in.readline()):
            return False
        self.loadDevInfo(file_in.readline())
        self.loadCond(file_in.readline())
        self.loadTime(file_in.readline())
        self.loadCali(file_in.readline())
        for line in file_in:
            if self.loadComment(line):
                continue
            if self.loadHiAc(line):
                continue
            if self.loadTag(line):
                return True

class sbdData(sbdHead):
    def __init__(self,head):
        self.head=head
        self.point=array.array('H')    
        self.zap=array.array('f')
        self.vol=array.array('f')
        self.cur=array.array('f')
        self.leak=array.array('f')
        self.count=0
    
    def reset(self):
        self.point=array.array('H')    
        self.zap=array.array('f')
        self.vol=array.array('f')
        self.cur=array.array('f')
        self.leak=array.array('f')
        self.count=0
    
    def loadData(self):
        if self.head.state&TAG_INFO:
            try:
                reader=csv.reader(self.head.file)
                for point,zap,vol,cur,leak in reader:
                    self.point.append(int(point))
                    self.zap.append(float(zap))
                    self.vol.append(float(vol))
                    self.cur.append(float(cur))
                    self.leak.append(float(leak))
                    self.count=self.count+1
            except:
                pass
        
            
class sbdFile():
    def __init__(self):
        self.head=sbdHead()
        self.data=sbdData(self.head)
    
    def reset(self):
        self.head.reset()
        self.data.reset()
    
    def load(self,file_in):
        self.head.collectInfo(file_in)
        self.data.loadData()
    
    