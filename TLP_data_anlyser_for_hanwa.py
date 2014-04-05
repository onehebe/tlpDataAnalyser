'''
Created on Apr 18, 2013

@author: root
'''
from Tkinter import *
from tkFileDialog import *
from matplotlib.backends.backend_tkagg import *
from matplotlib.backend_bases import *
from matplotlib.figure import *
from matplotlib.ticker import *
from tkFont import *
import classDef
import analyser

class TLP_GUI(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.formDef()
        self.varDef()
        self.createTopFramework()
        self.createMenu()
        self.createTLP()
        self.grid()
    #############################################################################
    #                format defination
    #############################################################################       
    def formDef(self):
        self.menu_font=Font(size=11)
        self.default_font=Font(size=11)
        self.box_font=Font(size=10,weight='normal')
        self.yminorLocator=MultipleLocator(2)
    
    #############################################################################
    #                variable defination
    #############################################################################       
    def varDef(self):     
        self.type=StringVar()
        self.fst_trig_cur=StringVar()
        self.fst_trig_vol=StringVar()
        self.sec_trig_cur=StringVar()
        self.sec_trig_vol=StringVar()    
        
        self.tlp_path=StringVar()
        self.save_path=StringVar()
        self.section_view_path=StringVar()
        self.line1=None
        self.line2=None
        self.sbd=classDef.sbdFile()
        self.analyser=analyser.analyser()
        
        self.figWid=8
        self.figHgt=5.5
    #############################################################################
    #                weidget construction
    #############################################################################
    def createTopFramework(self):
        self.topFrame=Frame(self,padx=10,pady=10)
        self.topFrame.grid(row=0,column=0)

    
    def createMenu(self):
        self.topFrame.menubar=Menu(self.winfo_toplevel())
        #self.topFrame.propagate(True)
        self.winfo_toplevel()['menu']=self.topFrame.menubar
    
        self.topFrame.menubar.file_menu=Menu(self.topFrame.menubar,tearoff=0)
        self.topFrame.menubar.file_menu.add_command(label="open file",command=self.default_com,font=self.default_font)
        self.topFrame.menubar.file_menu.add_command(label="open directory",command=self.default_com,font=self.default_font)
        self.topFrame.menubar.file_menu.add_command(label="save",command=self.default_com,font=self.default_font)
        self.topFrame.menubar.file_menu.add_separator()
        self.topFrame.menubar.file_menu.add_command(label="quit",command=self.quit,font=self.default_font)
        self.topFrame.menubar.add_cascade(label="File",menu=self.topFrame.menubar.file_menu,font=self.menu_font)
        
        self.topFrame.menubar.edit_menu=Menu(self.topFrame.menubar,tearoff=0)
        self.topFrame.menubar.edit_menu.add_command(label="edit",command=self.default_com,font=self.default_font)
        self.topFrame.menubar.add_cascade(label="Edit",menu=self.topFrame.menubar.edit_menu,font=self.menu_font)
        
        self.topFrame.menubar.view_menu=Menu(self.topFrame.menubar,tearoff=0)
        self.topFrame.menubar.view_menu.add_command(label="minimal",command=self.setMinimal,font=self.default_font)
        self.topFrame.menubar.view_menu.add_command(label="medium",command=self.setMiddium,font=self.default_font)
        self.topFrame.menubar.view_menu.add_command(label="max",command=self.setMax,font=self.default_font)
        self.topFrame.menubar.add_cascade(label="View",menu=self.topFrame.menubar.view_menu,font=self.menu_font)
        
        self.topFrame.menubar.help_menu=Menu(self.topFrame.menubar,tearoff=0)
        self.topFrame.menubar.help_menu.add_command(label="help",command=self.default_com,font=self.default_font)
        self.topFrame.menubar.help_menu.add_separator()
        self.topFrame.menubar.help_menu.add_command(label="about",command=self.default_com,font=self.default_font)
        self.topFrame.menubar.add_cascade(label="Help",menu=self.topFrame.menubar.help_menu,font=self.menu_font)      
    
    def createTLP(self):
        self.topFrame.tlpFrame=Frame(self.topFrame,padx=5,pady=5)
        self.topFrame.tlpFrame.grid(row=1,column=1)
        #self.topFrame.tlpFrame.propagate(True)
        self.createTLP_fbox()
        self.createTLP_infobox()
        self.createTLP_plot()
        self.topFrame.tlpFrame.columnconfigure(0,weight=1)
        self.topFrame.tlpFrame.columnconfigure(1,weight=2)
        self.topFrame.tlpFrame.rowconfigure(0,weight=1)
        self.topFrame.tlpFrame.rowconfigure(1,weight=3)
        self.topFrame.tlpFrame.rowconfigure(2,weight=1)
    
    def createTLP_fbox(self):
        self.topFrame.tlpFrame.fbox=Frame(self.topFrame.tlpFrame,padx=10,pady=5,borderwidth=1,relief=GROOVE)
        self.topFrame.tlpFrame.fbox.grid(row=0,column=0,padx=10,pady=5,sticky=NW)
        
        self.topFrame.tlpFrame.fbox.label=Label(self.topFrame.tlpFrame.fbox,text='select the data directory',anchor=W,font=self.default_font)
        self.topFrame.tlpFrame.fbox.label.grid(row=0,column=0,padx=10,pady=3,columnspan=4,sticky=W)
        
        self.topFrame.tlpFrame.fbox.entry=Entry(self.topFrame.tlpFrame.fbox,textvariable=self.tlp_path,width=30)
        self.topFrame.tlpFrame.fbox.entry.grid(row=1,column=0,padx=3,pady=3,columnspan=4)
        
        self.topFrame.tlpFrame.fbox.open_but=Button(self.topFrame.tlpFrame.fbox,text="Open",command=self.openFile,width=3,font=self.default_font)
        self.topFrame.tlpFrame.fbox.open_but.grid(row=3,column=1,padx=3,pady=3,sticky=E)
        
        self.topFrame.tlpFrame.fbox.clear_but=Button(self.topFrame.tlpFrame.fbox,text="Clear",command=self.clearPath,width=3,font=self.default_font)
        self.topFrame.tlpFrame.fbox.clear_but.grid(row=3,column=2,padx=3,pady=3,sticky=E)
        
        self.topFrame.tlpFrame.fbox.quit_but=Button(self.topFrame.tlpFrame.fbox,text="Plot",command=self.plotDirect,width=3,font=self.default_font)
        self.topFrame.tlpFrame.fbox.quit_but.grid(row=3,column=3,padx=3,pady=3,sticky=E)
        
        self.topFrame.tlpFrame.fbox.columnconfigure(0,weight=2)
        self.topFrame.tlpFrame.fbox.columnconfigure(1,weight=1)
        self.topFrame.tlpFrame.fbox.columnconfigure(2,weight=1)
        self.topFrame.tlpFrame.fbox.columnconfigure(3,weight=1)
    
    def createTLP_infobox(self):
        self.topFrame.tlpFrame.ifbox=Frame(self.topFrame.tlpFrame,padx=5,pady=5,borderwidth=1,relief=RIDGE)
        self.topFrame.tlpFrame.ifbox.grid(row=1,column=0,padx=5,pady=5,stick=NW)
        
        self.topFrame.tlpFrame.ifbox.type=Label(self.topFrame.tlpFrame.ifbox,text='Curve Type',anchor=W,font=self.default_font)
        self.topFrame.tlpFrame.ifbox.type.grid(row=0,column=0,padx=0,pady=0)
        self.topFrame.tlpFrame.ifbox.type_entry=Entry(self.topFrame.tlpFrame.ifbox,textvariable=self.type,width=15,font=self.box_font)
        self.topFrame.tlpFrame.ifbox.type_entry.grid(row=0,column=1,padx=0,pady=0,sticky=W)
        
        self.topFrame.tlpFrame.ifbox.ftv=Label(self.topFrame.tlpFrame.ifbox,text='1st Trigger Voltage',anchor=W,font=self.default_font)
        self.topFrame.tlpFrame.ifbox.ftv.grid(row=1,column=0,padx=0,pady=0)
        self.topFrame.tlpFrame.ifbox.ftv_entry=Entry(self.topFrame.tlpFrame.ifbox,textvariable=self.fst_trig_vol,width=15,font=self.box_font)
        self.topFrame.tlpFrame.ifbox.ftv_entry.grid(row=1,column=1,padx=0,pady=0,sticky=W)
        
        self.topFrame.tlpFrame.ifbox.ftc=Label(self.topFrame.tlpFrame.ifbox,text='1st Trigger Current',anchor=W,font=self.default_font)
        self.topFrame.tlpFrame.ifbox.ftc.grid(row=2,column=0,padx=0,pady=0)
        self.topFrame.tlpFrame.ifbox.ftc_entry=Entry(self.topFrame.tlpFrame.ifbox,textvariable=self.fst_trig_cur,width=15,font=self.box_font)
        self.topFrame.tlpFrame.ifbox.ftc_entry.grid(row=2,column=1,padx=0,pady=0,sticky=W)
        
        self.topFrame.tlpFrame.ifbox.stc=Label(self.topFrame.tlpFrame.ifbox,text='2nd Trigger Voltage',anchor=W,font=self.default_font)
        self.topFrame.tlpFrame.ifbox.stc.grid(row=3,column=0,padx=0,pady=0)
        self.topFrame.tlpFrame.ifbox.stc_entry=Entry(self.topFrame.tlpFrame.ifbox,textvariable=self.sec_trig_vol,width=15,font=self.box_font)
        self.topFrame.tlpFrame.ifbox.stc_entry.grid(row=3,column=1,padx=0,pady=0,sticky=W)
        
        self.topFrame.tlpFrame.ifbox.stc=Label(self.topFrame.tlpFrame.ifbox,text='2nd Trigger Current',anchor=W,font=self.default_font)
        self.topFrame.tlpFrame.ifbox.stc.grid(row=4,column=0,padx=0,pady=0)
        self.topFrame.tlpFrame.ifbox.stc_entry=Entry(self.topFrame.tlpFrame.ifbox,textvariable=self.sec_trig_cur,width=15,font=self.box_font)
        self.topFrame.tlpFrame.ifbox.stc_entry.grid(row=4,column=1,padx=0,pady=0,sticky=W)

    def createTLP_plot(self):
        self.topFrame.tlpFrame.plot=Frame(self.topFrame.tlpFrame,pady=5,borderwidth=1,relief=RIDGE)
        self.topFrame.tlpFrame.plot.grid(row=0,column=1,padx=5,pady=5,ipadx=5,ipady=5,rowspan=3)
        self.topFrame.tlpFrame.plot.propagate(True)
        
        self.topFrame.tlpFrame.plot.plotpars=SubplotParams(left=0.15,right=0.9,bottom=0.15,top=0.85)
        self.topFrame.tlpFrame.plot.figure = Figure(figsize=(self.figWid,self.figHgt),dpi=100,subplotpars=self.topFrame.tlpFrame.plot.plotpars)
        self.topFrame.tlpFrame.plot.figure.hold(False)
        
        self.ax= self.topFrame.tlpFrame.plot.figure.add_subplot(111)
        self.ax.set_xlabel('Voltage',size=15)
        self.ax.set_ylabel('Current',size=15)
        self.bx=self.ax.twiny()
        self.bx.set_xlabel('Leakage',size=15)
        self.ax.xaxis.set_minor_locator(self.yminorLocator)
        self.bx.xaxis.grid(True,which='major',color='b')
        self.bx.xaxis.grid(True,which='minor',color='g')
        self.ax.yaxis.grid(True,which='major',color='b')
        self.ax.yaxis.grid(True,which='minor',color='g')
        
        self.topFrame.tlpFrame.plot.canvas=FigureCanvasTkAgg(self.topFrame.tlpFrame.plot.figure,master= self.topFrame.tlpFrame.plot)
        self.topFrame.tlpFrame.plot.canvas.show()
        self.topFrame.tlpFrame.plot.canvas.get_tk_widget().grid(row=0,column=0)
        
        self.topFrame.tlpFrame.plot.toolbar=NavigationToolbar2TkAgg(self.topFrame.tlpFrame.plot.canvas,self.topFrame.tlpFrame.plot)
        self.topFrame.tlpFrame.plot.toolbar.update()
        self.topFrame.tlpFrame.plot.canvas._tkcanvas.pack()
        
    #############################################################################
    #                function
    ############################################################################# 
        
    def default_com(self):
        print('button')

    def openFile(self):
        feadback=askopenfilenames()
        if feadback is not () and feadback is not '':
            filename=feadback[0]
            self.tlp_path.set(filename)
        else:
            return False
        
        try:
            file_in=open(filename,'r')
        except:
            print('open file'+filename+' failed')
            return False
        
        self.sbd.reset()
        self.analyser.reset()
        self.sbd.load(file_in)
        self.analyser.determin(self.sbd)
        self.plotData()
        self.plotInfo()
    
    def plotDirect(self):
        self.plotData()

    
    def plotData(self):
        self.clearPath(False)
        self.line1=self.ax.plot(self.sbd.data.vol.tolist(),self.sbd.data.cur.tolist(),'r^-',linewidth=2)
        self.line2=self.bx.semilogx(self.sbd.data.leak.tolist(),self.sbd.data.cur.tolist(),'b1-',linewidth=1)
        
        self.topFrame.tlpFrame.plot.canvas.show()
    
    def plotInfo(self):
        self.type.set(self.analyser.type)
        if self.analyser.trig_vol is not 0:
            self.fst_trig_vol.set(self.analyser.trig_vol)
        else:
            self.fst_trig_vol.set("None")
            
        if self.analyser.trig_cur is not 0:
            self.fst_trig_cur.set(self.analyser.trig_cur)
        else:
            self.fst_trig_cur.set("None")  
            
        if self.analyser.trig2_vol is not 0:
            self.sec_trig_vol.set(self.analyser.trig2_vol)
        else:
            self.sec_trig_vol.set("None")  
            
        if self.analyser.trig2_cur is not 0:
            self.sec_trig_cur.set(self.analyser.trig2_cur)
        else:
            self.sec_trig_cur.set("None")     
    
    def clearPath(self,flag=True):
        self.ax.clear()
        self.bx.clear()
        self.ax.set_xlabel('Voltage',size=15)
        self.ax.set_ylabel('Current',size=15)
        self.bx=self.ax.twiny()
        self.bx.set_xlabel('Leakage',size=15)
        self.ax.xaxis.set_minor_locator(self.yminorLocator)
        self.bx.xaxis.grid(True,which='major',color='b')
        self.bx.xaxis.grid(True,which='minor',color='g')
        self.ax.yaxis.grid(True,which='major',color='b')
        self.ax.yaxis.grid(True,which='minor',color='g')
        if flag:
            self.topFrame.tlpFrame.plot.canvas.show()

    def setMinimal(self):
        self.figWid=4
        self.figHgt=3
        self.refreshAll()
    
    def setMiddium(self):
        self.figWid=8
        self.figHgt=5.5
        self.refreshAll()
        
    def setMax(self):
        self.figWid=10
        self.figHgt=8
        self.refreshAll()
    

    def refreshAll(self):
        self.topFrame.grid_remove()
        self.createTopFramework()
        self.createMenu()
        self.createTLP()
        self.plotData()

inst_GUI=TLP_GUI()
inst_GUI.master.title("TLP data anlyser for Hanwa")
inst_GUI.mainloop()
        
