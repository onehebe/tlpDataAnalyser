import numpy as np

global PAT_S
global PAT_L
global PAT_R
global PAT_UKN

global POL_POS
global POL_NEG

PAT_S=1
PAT_D=2
PAT_R=3
PAT_UKN=0

POL_POS=True
POL_NEG=False

class analyser():
    def __init__(self):
        self.pattern=PAT_UKN
        self.type=''
        self.trig_vol=0
        self.trig_cur=0
        self.trig2_vol=0
        self.trig2_cur=0
        self.polarity=POL_POS
        
        self.zap_array=None
        self.cur_array=None
        self.vol_array=None
        self.leak_array=None
        
        self.TR1_MIN_RATIO=1.8
        self.TR1_MAX_RATIO=2.2
        self.VZRAT_TOLER=3
        self.LEAK_RATIO_MIN=0.8
        self.LEAK_RATIO_MAX=1.2
        self.LEAK_TOLER=5
        self.SNAPBACK_RATIO=0.8
        
        self.point1_index=0
        self.point2_index=0
        
    
    def reset(self):
        self.pattern=PAT_UKN
        self.type=''
        self.trig_vol=0
        self.trig_cur=0
        self.trig2_vol=0
        self.trig2_cur=0
        self.polarity=POL_POS
        
        self.zap_array=None
        self.cur_array=None
        self.vol_array=None
        self.leak_array=None
        
        self.point1_index=0
        self.point2_index=0
    
    def determin(self,sbdFile):
        #    step1:
        #        find the point 'point1' when TR1_MIN_RATIO<vol/zap<TR1_MAX_RATIO
        #    step2:
        #        set the leakage at 'point1' as reference leakage leak_ref
        #        divide leakage by leak_ref and get the result leak_ratio. Find the LEAK_TOLERth point 'point2' that LEAK_RATIO_MIN<leak_ratio<LEAK_RATIO_MAX
        #    step3:
        #        set point2 as 2nd trigger point
        #        look back. if there is a maxium value for diff(vol), use its value as 1st trigger point
        #        either use point 1 as 1st trigger point
        if sbdFile.data.zap[1]<0:
            self.polarity=POL_NEG
        else:
            self.polarity=POL_POS
            
        if self.polarity:
            self.zap_array=np.asarray(sbdFile.data.zap)
            self.cur_array=np.asarray(sbdFile.data.cur)
            self.vol_array=np.asarray(sbdFile.data.vol)
            self.leak_array=np.asarray(sbdFile.data.leak)
        else:
            self.zap_array=-np.asarray(sbdFile.data.zap)
            self.cur_array=-np.asarray(sbdFile.data.cur)
            self.vol_array=-np.asarray(sbdFile.data.vol)
            self.leak_array=np.abs(np.asarray(sbdFile.data.leak))
            
        self.step1()
        self.step2()
        self.step3()
        return True
        
    def step1(self):        #return the index of point 1
        vol_zap_ratio=self.vol_array/self.zap_array
        count=0
        index=0
        for i in vol_zap_ratio:
            
            if self.TR1_MIN_RATIO<i and i<self.TR1_MAX_RATIO:
                count=0
            else:
                count=count+1
                
            if count>=self.VZRAT_TOLER:
                self.point1_index=index+1-self.VZRAT_TOLER
                return True
            else:
                index=index+1
        return False
    
    def step2(self):
        leak_ref=self.leak_array[self.point1_index]
        leak_ratio=self.leak_array/leak_ref
        count=0
        index=0
        for i in leak_ratio:
            
            if self.LEAK_RATIO_MIN<i and i<self.LEAK_RATIO_MAX:
                count=0
            else:
                count=count+1
                
            if count>=self.LEAK_TOLER:
                self.point2_index=index+1-self.LEAK_TOLER
                return True
            else:
                index=index+1
        return False
    
    def step3(self):
        if self.point2_index==0:
            temp=self.vol_array
        else:
            self.trig2_cur=self.cur_array[self.point2_index]
            self.trig2_vol=self.vol_array[self.point2_index]
            temp=self.vol_array[0:self.point2_index]
            
        temp_dif=np.diff(temp,n=1)
        suspect_index=np.argmin(temp_dif)
        
        if temp_dif[suspect_index]<0 and self.vol_array[suspect_index+1]/self.vol_array[suspect_index]<self.SNAPBACK_RATIO :
            self.pattern=PAT_S
            self.trig_cur=self.cur_array[suspect_index]
            self.trig_vol=self.vol_array[suspect_index]
        else:
            self.pattern=PAT_D
            self.trig_cur=self.cur_array[self.point1_index]
            self.trig_vol=self.vol_array[self.point1_index]
            
        self.type=self.getType()
        return True
    
    def getType(self):
        if self.pattern is PAT_UKN:
            return('Unkown type')
        elif self.pattern is PAT_S:
            return('Snapback type')
        elif self.pattern is PAT_D:
            return('Diode type')
        elif self.pattern is PAT_R:
            return('Resistor type')
        else:
            return(False)