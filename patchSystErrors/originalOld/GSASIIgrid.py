# -*- coding: utf-8 -*-
#GSASIIgrid - data display routines
########### SVN repository information ###################
# $Date: 2015-03-13 16:46:05 -0400 (Fri, 13 Mar 2015) $
# $Author: vondreele $
# $Revision: 1699 $
# $URL: https://subversion.xor.aps.anl.gov/pyGSAS/trunk/GSASIIgrid.py $
# $Id: GSASIIgrid.py 1699 2015-03-13 20:46:05Z vondreele $
########### SVN repository information ###################
'''
*GSASIIgrid: Basic GUI routines*
--------------------------------

Note that a number of routines here should be moved to GSASIIctrls eventually, such as
G2LoggedButton, EnumSelector, G2ChoiceButton, SingleFloatDialog, SingleStringDialog,
MultiStringDialog, G2MultiChoiceDialog, G2SingleChoiceDialog, G2ColumnIDDialog, ItemSelector, GridFractionEditor

Probably SGMessageBox, SymOpDialog, DisAglDialog, too. 
'''
import wx
import wx.grid as wg
import wx.wizard as wz
import wx.aui
import wx.lib.scrolledpanel as wxscroll
import time
import copy
import cPickle
import sys
import os
import numpy as np
import numpy.ma as ma
import scipy.optimize as so
import GSASIIpath
GSASIIpath.SetVersionNumber("$Revision: 1699 $")
import GSASIImath as G2mth
import GSASIIIO as G2IO
import GSASIIstrIO as G2stIO
import GSASIIlattice as G2lat
import GSASIIplot as G2plt
import GSASIIpwdGUI as G2pdG
import GSASIIimgGUI as G2imG
import GSASIIphsGUI as G2phG
import GSASIIspc as G2spc
import GSASIImapvars as G2mv
import GSASIIconstrGUI as G2cnstG
import GSASIIrestrGUI as G2restG
import GSASIIpy3 as G2py3
import GSASIIobj as G2obj
import GSASIIexprGUI as G2exG
import GSASIIlog as log
import GSASIIctrls as G2G

# trig functions in degrees
sind = lambda x: np.sin(x*np.pi/180.)
tand = lambda x: np.tan(x*np.pi/180.)
cosd = lambda x: np.cos(x*np.pi/180.)

# Define a short name for convenience
WACV = wx.ALIGN_CENTER_VERTICAL

[ wxID_FOURCALC, wxID_FOURSEARCH, wxID_FOURCLEAR, wxID_PEAKSMOVE, wxID_PEAKSCLEAR, 
    wxID_CHARGEFLIP, wxID_PEAKSUNIQUE, wxID_PEAKSDELETE, wxID_PEAKSDA,
    wxID_PEAKSDISTVP, wxID_PEAKSVIEWPT, wxID_FINDEQVPEAKS,wxID_SHOWBONDS,wxID_MULTIMCSA,
    wxID_SINGLEMCSA, wxID_4DMAPCOMPUTE,wxID_4DCHARGEFLIP,
] = [wx.NewId() for item in range(17)]

[ wxID_PWDRADD, wxID_HKLFADD, wxID_PWDANALYSIS, wxID_PWDCOPY, wxID_PLOTCTRLCOPY, 
    wxID_DATADELETE,
] = [wx.NewId() for item in range(6)]

[ wxID_ATOMSEDITADD, wxID_ATOMSEDITINSERT, wxID_ATOMSEDITDELETE, wxID_ATOMSREFINE, 
    wxID_ATOMSMODIFY, wxID_ATOMSTRANSFORM, wxID_ATOMSVIEWADD, wxID_ATOMVIEWINSERT,
    wxID_RELOADDRAWATOMS,wxID_ATOMSDISAGL,wxID_ATOMMOVE,wxID_MAKEMOLECULE,
    wxID_ASSIGNATMS2RB,wxID_ATOMSPDISAGL, wxID_ISODISP,
] = [wx.NewId() for item in range(15)]

[ wxID_DRAWATOMSTYLE, wxID_DRAWATOMLABEL, wxID_DRAWATOMCOLOR, wxID_DRAWATOMRESETCOLOR, 
    wxID_DRAWVIEWPOINT, wxID_DRAWTRANSFORM, wxID_DRAWDELETE, wxID_DRAWFILLCELL, 
    wxID_DRAWADDEQUIV, wxID_DRAWFILLCOORD, wxID_DRAWDISAGLTOR,  wxID_DRAWPLANE,
    wxID_DRAWDISTVP,
] = [wx.NewId() for item in range(13)]

[ wxID_DRAWRESTRBOND, wxID_DRAWRESTRANGLE, wxID_DRAWRESTRPLANE, wxID_DRAWRESTRCHIRAL,
] = [wx.NewId() for item in range(4)]

[ wxID_ADDMCSAATOM,wxID_ADDMCSARB,wxID_CLEARMCSARB,wxID_MOVEMCSA,wxID_MCSACLEARRESULTS,
] = [wx.NewId() for item in range(5)]

[ wxID_CLEARTEXTURE,wxID_REFINETEXTURE,
] = [wx.NewId() for item in range(2)]

[ wxID_PAWLEYLOAD, wxID_PAWLEYESTIMATE, wxID_PAWLEYUPDATE,
] = [wx.NewId() for item in range(3)]

[ wxID_IMCALIBRATE,wxID_IMRECALIBRATE,wxID_IMINTEGRATE, wxID_IMCLEARCALIB,  
    wxID_IMCOPYCONTROLS, wxID_INTEGRATEALL, wxID_IMSAVECONTROLS, wxID_IMLOADCONTROLS,
] = [wx.NewId() for item in range(8)]

[ wxID_MASKCOPY, wxID_MASKSAVE, wxID_MASKLOAD, wxID_NEWMASKSPOT,wxID_NEWMASKARC,wxID_NEWMASKRING,
    wxID_NEWMASKFRAME, wxID_NEWMASKPOLY,  wxID_MASKLOADNOT,
] = [wx.NewId() for item in range(9)]

[ wxID_STRSTACOPY, wxID_STRSTAFIT, wxID_STRSTASAVE, wxID_STRSTALOAD,wxID_STRSTSAMPLE,
    wxID_APPENDDZERO,wxID_STRSTAALLFIT,wxID_UPDATEDZERO,
] = [wx.NewId() for item in range(8)]

[ wxID_BACKCOPY,wxID_LIMITCOPY, wxID_SAMPLECOPY, wxID_SAMPLECOPYSOME, wxID_BACKFLAGCOPY, wxID_SAMPLEFLAGCOPY,
    wxID_SAMPLESAVE, wxID_SAMPLELOAD,wxID_ADDEXCLREGION,wxID_SETSCALE,wxID_SAMPLE1VAL,wxID_ALLSAMPLELOAD,
] = [wx.NewId() for item in range(12)]

[ wxID_INSTPRMRESET,wxID_CHANGEWAVETYPE,wxID_INSTCOPY, wxID_INSTFLAGCOPY, wxID_INSTLOAD,
    wxID_INSTSAVE, wxID_INST1VAL, wxID_INSTCALIB,
] = [wx.NewId() for item in range(8)]

[ wxID_UNDO,wxID_LSQPEAKFIT,wxID_LSQONECYCLE,wxID_RESETSIGGAM,wxID_CLEARPEAKS,wxID_AUTOSEARCH,
    wxID_PEAKSCOPY, wxID_SEQPEAKFIT,
] = [wx.NewId() for item in range(8)]

[  wxID_INDXRELOAD, wxID_INDEXPEAKS, wxID_REFINECELL, wxID_COPYCELL, wxID_MAKENEWPHASE,
] = [wx.NewId() for item in range(5)]

[ wxID_CONSTRAINTADD,wxID_EQUIVADD,wxID_HOLDADD,wxID_FUNCTADD,
  wxID_CONSPHASE, wxID_CONSHIST, wxID_CONSHAP, wxID_CONSGLOBAL,
] = [wx.NewId() for item in range(8)]

[ wxID_RESTRAINTADD, wxID_RESTSELPHASE,wxID_RESTDELETE, wxID_RESRCHANGEVAL, 
    wxID_RESTCHANGEESD,wxID_AARESTRAINTADD,wxID_AARESTRAINTPLOT,
] = [wx.NewId() for item in range(7)]

[ wxID_RIGIDBODYADD,wxID_DRAWDEFINERB,wxID_RIGIDBODYIMPORT,wxID_RESIDUETORSSEQ,
    wxID_AUTOFINDRESRB,wxID_GLOBALRESREFINE,wxID_RBREMOVEALL,wxID_COPYRBPARMS,
    wxID_GLOBALTHERM,wxID_VECTORBODYADD
] = [wx.NewId() for item in range(10)]

[ wxID_RENAMESEQSEL,wxID_SAVESEQSEL,wxID_SAVESEQSELCSV,wxID_SAVESEQCSV,wxID_PLOTSEQSEL,
  wxID_ORGSEQSEL,wxADDSEQVAR,wxDELSEQVAR,wxEDITSEQVAR,wxCOPYPARFIT,
  wxADDPARFIT,wxDELPARFIT,wxEDITPARFIT,wxDOPARFIT,
] = [wx.NewId() for item in range(14)]

[ wxID_MODELCOPY,wxID_MODELFIT,wxID_MODELADD,wxID_ELEMENTADD,wxID_ELEMENTDELETE,
    wxID_ADDSUBSTANCE,wxID_LOADSUBSTANCE,wxID_DELETESUBSTANCE,wxID_COPYSUBSTANCE,
    wxID_MODELUNDO,wxID_MODELFITALL,wxID_MODELCOPYFLAGS,
] = [wx.NewId() for item in range(12)]

[ wxID_SELECTPHASE,wxID_PWDHKLPLOT,wxID_PWD3DHKLPLOT,
] = [wx.NewId() for item in range(3)]

[ wxID_PDFCOPYCONTROLS, wxID_PDFSAVECONTROLS, wxID_PDFLOADCONTROLS, 
    wxID_PDFCOMPUTE, wxID_PDFCOMPUTEALL, wxID_PDFADDELEMENT, wxID_PDFDELELEMENT,
] = [wx.NewId() for item in range(7)]

[ wxID_MCRON,wxID_MCRLIST,wxID_MCRSAVE,wxID_MCRPLAY,
] = [wx.NewId() for item in range(4)]

VERY_LIGHT_GREY = wx.Colour(235,235,235)
################################################################################
#### GSAS-II class definitions
################################################################################

class SGMessageBox(wx.Dialog):
    ''' Special version of MessageBox that displays space group & super space group text
    in two blocks
    '''
    def __init__(self,parent,title,text,table,):
        wx.Dialog.__init__(self,parent,wx.ID_ANY,title,pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.text=text
        self.table = table
        self.panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add((0,10))
        for line in text:
            mainSizer.Add(wx.StaticText(self.panel,label='     %s     '%(line)),0,WACV)
        ncol = self.table[0].count(',')+1
        tableSizer = wx.FlexGridSizer(0,2*ncol+3,0,0)
        for j,item in enumerate(self.table):
            num,flds = item.split(')')
            tableSizer.Add(wx.StaticText(self.panel,label='     %s  '%(num+')')),0,WACV|wx.ALIGN_LEFT)            
            flds = flds.replace(' ','').split(',')
            for i,fld in enumerate(flds):
                if i < ncol-1:
                    tableSizer.Add(wx.StaticText(self.panel,label='%s, '%(fld)),0,WACV|wx.ALIGN_RIGHT)
                else:
                    tableSizer.Add(wx.StaticText(self.panel,label='%s'%(fld)),0,WACV|wx.ALIGN_RIGHT)
            if not j%2:
                tableSizer.Add((20,0))
        mainSizer.Add(tableSizer,0,wx.ALIGN_LEFT)
        btnsizer = wx.StdDialogButtonSizer()
        OKbtn = wx.Button(self.panel, wx.ID_OK)
        OKbtn.SetDefault()
        btnsizer.AddButton(OKbtn)
        btnsizer.Realize()
        mainSizer.Add((0,10))
        mainSizer.Add(btnsizer,0,wx.ALIGN_CENTER)
        self.panel.SetSizer(mainSizer)
        self.panel.Fit()
        self.Fit()
        size = self.GetSize()
        self.SetSize([size[0]+20,size[1]])

    def Show(self):
        '''Use this method after creating the dialog to post it
        '''
        self.ShowModal()
        return
        
        

class G2LoggedButton(wx.Button):
    '''A version of wx.Button that creates logging events. Bindings are saved
    in the object, and are looked up rather than directly set with a bind.
    An index to these buttons is saved as log.ButtonBindingLookup
    :param wx.Panel parent: parent widget
    :param int id: Id for button
    :param str label: label for button
    :param str locationcode: a label used internally to uniquely indentify the button
    :param function handler: a routine to call when the button is pressed
    '''
    def __init__(self,parent,id=wx.ID_ANY,label='',locationcode='',
                 handler=None,*args,**kwargs):
        super(self.__class__,self).__init__(parent,id,label,*args,**kwargs)
        self.label = label
        self.handler = handler
        self.locationcode = locationcode
        key = locationcode + '+' + label # hash code to find button
        self.Bind(wx.EVT_BUTTON,self.onPress)
        log.ButtonBindingLookup[key] = self
    def onPress(self,event):
        'create log event and call handler'
        log.MakeButtonLog(self.locationcode,self.label)
        self.handler(event)
        
################################################################################
################################################################################
class EnumSelector(wx.ComboBox):
    '''A customized :class:`wxpython.ComboBox` that selects items from a list
    of choices, but sets a dict (list) entry to the corresponding
    entry from the input list of values.

    :param wx.Panel parent: the parent to the :class:`~wxpython.ComboBox` (usually a
      frame or panel)
    :param dict dct: a dict (or list) to contain the value set
      for the :class:`~wxpython.ComboBox`.
    :param item: the dict key (or list index) where ``dct[item]`` will 
      be set to the value selected in the :class:`~wxpython.ComboBox`. Also, dct[item]
      contains the starting value shown in the widget. If the value
      does not match an entry in :data:`values`, the first value
      in :data:`choices` is used as the default, but ``dct[item]`` is
      not changed.    
    :param list choices: a list of choices to be displayed to the
      user such as
      ::
      
      ["default","option 1","option 2",]

      Note that these options will correspond to the entries in 
      :data:`values` (if specified) item by item. 
    :param list values: a list of values that correspond to
      the options in :data:`choices`, such as
      ::
      
      [0,1,2]
      
      The default for :data:`values` is to use the same list as
      specified for :data:`choices`.
    :param (other): additional keyword arguments accepted by
      :class:`~wxpython.ComboBox` can be specified.
    '''
    def __init__(self,parent,dct,item,choices,values=None,**kw):
        if values is None:
            values = choices
        if dct[item] in values:
            i = values.index(dct[item])
        else:
            i = 0
        startval = choices[i]
        wx.ComboBox.__init__(self,parent,wx.ID_ANY,startval,
                             choices = choices,
                             style=wx.CB_DROPDOWN|wx.CB_READONLY,
                             **kw)
        self.choices = choices
        self.values = values
        self.dct = dct
        self.item = item
        self.Bind(wx.EVT_COMBOBOX, self.onSelection)
    def onSelection(self,event):
        # respond to a selection by setting the enum value in the CIF dictionary
        if self.GetValue() in self.choices: # should always be true!
            self.dct[self.item] = self.values[self.choices.index(self.GetValue())]
        else:
            self.dct[self.item] = self.values[0] # unknown

################################################################################
################################################################################
class G2ChoiceButton(wx.Choice):
    '''A customized version of a wx.Choice that automatically initializes
    the control to match a supplied value and saves the choice directly
    into an array or list. Optionally a function can be called each time a
    choice is selected. The widget can be used with an array item that is set to 
    to the choice by number (``indLoc[indKey]``) or by string value
    (``strLoc[strKey]``) or both. The initial value is taken from ``indLoc[indKey]``
    if not None or ``strLoc[strKey]`` if not None. 

    :param wx.Panel parent: name of panel or frame that will be
      the parent to the widget. Can be None.
    :param list choiceList: a list or tuple of choices to offer the user.
    :param dict/list indLoc: a dict or list with the initial value to be
      placed in the Choice button. If this is None, this is ignored. 
    :param int/str indKey: the dict key or the list index for the value to be
      edited by the Choice button. If indLoc is not None then this
      must be specified and the ``indLoc[indKey]`` will be set. If the value
      for ``indLoc[indKey]`` is not None, it should be an integer in
      range(len(choiceList)). The Choice button will be initialized to the
      choice corresponding to the value in this element if not None.
    :param dict/list strLoc: a dict or list with the string value corresponding to
      indLoc/indKey. Default (None) means that this is not used. 
    :param int/str strKey: the dict key or the list index for the string value 
      The ``strLoc[strKey]`` element must exist or strLoc must be None (default).
    :param function onChoice: name of a function to call when the choice is made.
    '''
    def __init__(self,parent,choiceList,indLoc=None,indKey=None,strLoc=None,strKey=None,
                 onChoice=None,**kwargs):
        wx.Choice.__init__(self,parent,choices=choiceList,id=wx.ID_ANY,**kwargs)
        self.choiceList = choiceList
        self.indLoc = indLoc
        self.indKey = indKey
        self.strLoc = strLoc
        self.strKey = strKey
        self.onChoice = None
        self.SetSelection(wx.NOT_FOUND)
        if self.indLoc is not None and self.indLoc.get(self.indKey) is not None:
            self.SetSelection(self.indLoc[self.indKey])
            if self.strLoc is not None:
                self.strLoc[self.strKey] = self.GetStringSelection()
                log.LogVarChange(self.strLoc,self.strKey)
        elif self.strLoc is not None and self.strLoc.get(self.strKey) is not None:
            try:
                self.SetSelection(choiceList.index(self.strLoc[self.strKey]))
                if self.indLoc is not None:
                    self.indLoc[self.indKey] = self.GetSelection()
                    log.LogVarChange(self.indLoc,self.indKey)
            except ValueError:
                pass
        self.Bind(wx.EVT_CHOICE, self._OnChoice)
        #if self.strLoc is not None: # make sure strLoc gets initialized
        #    self._OnChoice(None) # note that onChoice will not be called
        self.onChoice = onChoice
    def _OnChoice(self,event):
        if self.indLoc is not None:
            self.indLoc[self.indKey] = self.GetSelection()
            log.LogVarChange(self.indLoc,self.indKey)
        if self.strLoc is not None:
            self.strLoc[self.strKey] = self.GetStringSelection()
            log.LogVarChange(self.strLoc,self.strKey)
        if self.onChoice:
            self.onChoice()

################################################################################
class SymOpDialog(wx.Dialog):
    '''Class to select a symmetry operator
    '''
    def __init__(self,parent,SGData,New=True,ForceUnit=False):
        wx.Dialog.__init__(self,parent,-1,'Select symmetry operator',
            pos=wx.DefaultPosition,style=wx.DEFAULT_DIALOG_STYLE)
        panel = wx.Panel(self)
        self.SGData = SGData
        self.New = New
        self.Force = ForceUnit
        self.OpSelected = [0,0,0,[0,0,0],False,False]
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        if ForceUnit:
            choice = ['No','Yes']
            self.force = wx.RadioBox(panel,-1,'Force to unit cell?',choices=choice)
            self.force.Bind(wx.EVT_RADIOBOX, self.OnOpSelect)
            mainSizer.Add(self.force,0,WACV)
        mainSizer.Add((5,5),0)
        if SGData['SGInv']:
            choice = ['No','Yes']
            self.inv = wx.RadioBox(panel,-1,'Choose inversion?',choices=choice)
            self.inv.Bind(wx.EVT_RADIOBOX, self.OnOpSelect)
            mainSizer.Add(self.inv,0,WACV)
        mainSizer.Add((5,5),0)
        if SGData['SGLatt'] != 'P':
            LattOp = G2spc.Latt2text(SGData['SGLatt']).split(';')
            self.latt = wx.RadioBox(panel,-1,'Choose cell centering?',choices=LattOp)
            self.latt.Bind(wx.EVT_RADIOBOX, self.OnOpSelect)
            mainSizer.Add(self.latt,0,WACV)
        mainSizer.Add((5,5),0)
        if SGData['SGLaue'] in ['-1','2/m','mmm','4/m','4/mmm']:
            Ncol = 2
        else:
            Ncol = 3
        OpList = []
        for Opr in SGData['SGOps']:
            OpList.append(G2spc.MT2text(Opr))
        self.oprs = wx.RadioBox(panel,-1,'Choose space group operator?',choices=OpList,
            majorDimension=Ncol)
        self.oprs.Bind(wx.EVT_RADIOBOX, self.OnOpSelect)
        mainSizer.Add(self.oprs,0,WACV)
        mainSizer.Add((5,5),0)
        mainSizer.Add(wx.StaticText(panel,-1,"   Choose unit cell?"),0,WACV)
        mainSizer.Add((5,5),0)
        cellSizer = wx.BoxSizer(wx.HORIZONTAL)
        cellSizer.Add((5,0),0)
        cellName = ['X','Y','Z']
        self.cell = []
        for i in range(3):
            self.cell.append(wx.SpinCtrl(panel,-1,cellName[i],size=wx.Size(50,20)))
            self.cell[-1].SetRange(-3,3)
            self.cell[-1].SetValue(0)
            self.cell[-1].Bind(wx.EVT_SPINCTRL, self.OnOpSelect)
            cellSizer.Add(self.cell[-1],0,WACV)
        mainSizer.Add(cellSizer,0,)
        if self.New:
            choice = ['No','Yes']
            self.new = wx.RadioBox(panel,-1,'Generate new positions?',choices=choice)
            self.new.Bind(wx.EVT_RADIOBOX, self.OnOpSelect)
            mainSizer.Add(self.new,0,WACV)
        mainSizer.Add((5,5),0)

        OkBtn = wx.Button(panel,-1,"Ok")
        OkBtn.Bind(wx.EVT_BUTTON, self.OnOk)
        cancelBtn = wx.Button(panel,-1,"Cancel")
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20),1)
        btnSizer.Add(OkBtn)
        btnSizer.Add((20,20),1)
        btnSizer.Add(cancelBtn)
        btnSizer.Add((20,20),1)

        mainSizer.Add(btnSizer,0,wx.EXPAND|wx.BOTTOM|wx.TOP, 10)
        panel.SetSizer(mainSizer)
        panel.Fit()
        self.Fit()

    def OnOpSelect(self,event):
        if self.SGData['SGInv']:
            self.OpSelected[0] = self.inv.GetSelection()
        if self.SGData['SGLatt'] != 'P':
            self.OpSelected[1] = self.latt.GetSelection()
        self.OpSelected[2] = self.oprs.GetSelection()
        for i in range(3):
            self.OpSelected[3][i] = float(self.cell[i].GetValue())
        if self.New:
            self.OpSelected[4] = self.new.GetSelection()
        if self.Force:
            self.OpSelected[5] = self.force.GetSelection()

    def GetSelection(self):
        return self.OpSelected

    def OnOk(self,event):
        parent = self.GetParent()
        parent.Raise()
        self.EndModal(wx.ID_OK)

    def OnCancel(self,event):
        parent = self.GetParent()
        parent.Raise()
        self.EndModal(wx.ID_CANCEL)

class DisAglDialog(wx.Dialog):
    '''Distance/Angle Controls input dialog. After
    :meth:`ShowModal` returns, the results are found in
    dict :attr:`self.data`, which is accessed using :meth:`GetData`.

    :param wx.Frame parent: reference to parent frame (or None)
    :param dict data: a dict containing the current
      search ranges or an empty dict, which causes default values
      to be used.
      Will be used to set element `DisAglCtls` in 
      :ref:`Phase Tree Item <Phase_table>`
    :param dict default:  A dict containing the default
      search ranges for each element.
    '''
    def __init__(self,parent,data,default):
        wx.Dialog.__init__(self,parent,wx.ID_ANY,
                           'Distance Angle Controls', 
            pos=wx.DefaultPosition,style=wx.DEFAULT_DIALOG_STYLE)
        self.default = default
        self.panel = wx.Panel(self)         #just a dummy - gets destroyed in Draw!
        self._default(data,self.default)
        self.Draw(self.data)
                
    def _default(self,data,default):
        '''Set starting values for the search values, either from
        the input array or from defaults, if input is null
        '''
        if data:
            self.data = copy.deepcopy(data) # don't mess with originals
        else:
            self.data = {}
            self.data['Name'] = default['Name']
            self.data['Factors'] = [0.85,0.85]
            self.data['AtomTypes'] = default['AtomTypes']
            self.data['BondRadii'] = default['BondRadii'][:]
            self.data['AngleRadii'] = default['AngleRadii'][:]

    def Draw(self,data):
        '''Creates the contents of the dialog. Normally called
        by :meth:`__init__`.
        '''
        self.panel.Destroy()
        self.panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(wx.StaticText(self.panel,-1,'Controls for phase '+data['Name']),
            0,WACV|wx.LEFT,10)
        mainSizer.Add((10,10),1)
        
        radiiSizer = wx.FlexGridSizer(0,3,5,5)
        radiiSizer.Add(wx.StaticText(self.panel,-1,' Type'),0,WACV)
        radiiSizer.Add(wx.StaticText(self.panel,-1,'Bond radii'),0,WACV)
        radiiSizer.Add(wx.StaticText(self.panel,-1,'Angle radii'),0,WACV)
        self.objList = {}
        for id,item in enumerate(self.data['AtomTypes']):
            radiiSizer.Add(wx.StaticText(self.panel,-1,' '+item),0,WACV)
            bRadii = wx.TextCtrl(self.panel,-1,value='%.3f'%(data['BondRadii'][id]),style=wx.TE_PROCESS_ENTER)
            self.objList[bRadii.GetId()] = ['BondRadii',id]
            bRadii.Bind(wx.EVT_TEXT_ENTER,self.OnRadiiVal)
            bRadii.Bind(wx.EVT_KILL_FOCUS,self.OnRadiiVal)
            radiiSizer.Add(bRadii,0,WACV)
            aRadii = wx.TextCtrl(self.panel,-1,value='%.3f'%(data['AngleRadii'][id]),style=wx.TE_PROCESS_ENTER)
            self.objList[aRadii.GetId()] = ['AngleRadii',id]
            aRadii.Bind(wx.EVT_TEXT_ENTER,self.OnRadiiVal)
            aRadii.Bind(wx.EVT_KILL_FOCUS,self.OnRadiiVal)
            radiiSizer.Add(aRadii,0,WACV)
        mainSizer.Add(radiiSizer,0,wx.EXPAND)
        factorSizer = wx.FlexGridSizer(0,2,5,5)
        Names = ['Bond','Angle']
        for i,name in enumerate(Names):
            factorSizer.Add(wx.StaticText(self.panel,-1,name+' search factor'),0,WACV)
            bondFact = wx.TextCtrl(self.panel,-1,value='%.3f'%(data['Factors'][i]),style=wx.TE_PROCESS_ENTER)
            self.objList[bondFact.GetId()] = ['Factors',i]
            bondFact.Bind(wx.EVT_TEXT_ENTER,self.OnRadiiVal)
            bondFact.Bind(wx.EVT_KILL_FOCUS,self.OnRadiiVal)
            factorSizer.Add(bondFact)
        mainSizer.Add(factorSizer,0,wx.EXPAND)
        
        OkBtn = wx.Button(self.panel,-1,"Ok")
        OkBtn.Bind(wx.EVT_BUTTON, self.OnOk)
        ResetBtn = wx.Button(self.panel,-1,'Reset')
        ResetBtn.Bind(wx.EVT_BUTTON, self.OnReset)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20),1)
        btnSizer.Add(OkBtn)
        btnSizer.Add(ResetBtn)
        btnSizer.Add((20,20),1)
        mainSizer.Add(btnSizer,0,wx.EXPAND|wx.BOTTOM|wx.TOP, 10)
        self.panel.SetSizer(mainSizer)
        self.panel.Fit()
        self.Fit()
    
    def OnRadiiVal(self,event):
        Obj = event.GetEventObject()
        item = self.objList[Obj.GetId()]
        try:
            self.data[item[0]][item[1]] = float(Obj.GetValue())
        except ValueError:
            pass
        Obj.SetValue("%.3f"%(self.data[item[0]][item[1]]))          #reset in case of error
        
    def GetData(self):
        'Returns the values from the dialog'
        return self.data
        
    def OnOk(self,event):
        'Called when the OK button is pressed'
        parent = self.GetParent()
        parent.Raise()
        self.EndModal(wx.ID_OK)              
        
    def OnReset(self,event):
        'Called when the Reset button is pressed'
        data = {}
        self._default(data,self.default)
        self.Draw(self.data)
                
class SingleFloatDialog(wx.Dialog):
    'Dialog to obtain a single float value from user'
    def __init__(self,parent,title,prompt,value,limits=[0.,1.],format='%.5g'):
        wx.Dialog.__init__(self,parent,-1,title, 
            pos=wx.DefaultPosition,style=wx.DEFAULT_DIALOG_STYLE)
        self.panel = wx.Panel(self)         #just a dummy - gets destroyed in Draw!
        self.limits = limits
        self.value = value
        self.prompt = prompt
        self.format = format
        self.Draw()
        
    def Draw(self):
        
        def OnValItem(event):
            try:
                val = float(valItem.GetValue())
                if val < self.limits[0] or val > self.limits[1]:
                    raise ValueError
            except ValueError:
                val = self.value
            self.value = val
            valItem.SetValue(self.format%(self.value))
            
        self.panel.Destroy()
        self.panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(wx.StaticText(self.panel,-1,self.prompt),0,wx.ALIGN_CENTER)
        valItem = wx.TextCtrl(self.panel,-1,value=self.format%(self.value),style=wx.TE_PROCESS_ENTER)
        mainSizer.Add(valItem,0,wx.ALIGN_CENTER)
        valItem.Bind(wx.EVT_TEXT_ENTER,OnValItem)
        valItem.Bind(wx.EVT_KILL_FOCUS,OnValItem)
        OkBtn = wx.Button(self.panel,-1,"Ok")
        OkBtn.Bind(wx.EVT_BUTTON, self.OnOk)
        CancelBtn = wx.Button(self.panel,-1,'Cancel')
        CancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20),1)
        btnSizer.Add(OkBtn)
        btnSizer.Add(CancelBtn)
        btnSizer.Add((20,20),1)
        mainSizer.Add(btnSizer,0,wx.EXPAND|wx.BOTTOM|wx.TOP, 10)
        self.panel.SetSizer(mainSizer)
        self.panel.Fit()
        self.Fit()

    def GetValue(self):
        return self.value
        
    def OnOk(self,event):
        parent = self.GetParent()
        parent.Raise()
        self.EndModal(wx.ID_OK)              
        
    def OnCancel(self,event):
        parent = self.GetParent()
        parent.Raise()
        self.EndModal(wx.ID_CANCEL)

################################################################################
class SingleStringDialog(wx.Dialog):
    '''Dialog to obtain a single string value from user
    
    :param wx.Frame parent: name of parent frame
    :param str title: title string for dialog
    :param str prompt: string to tell use what they are inputting
    :param str value: default input value, if any
    '''
    def __init__(self,parent,title,prompt,value='',size=(200,-1)):
        wx.Dialog.__init__(self,parent,wx.ID_ANY,title, 
                           pos=wx.DefaultPosition,
                           style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.value = value
        self.prompt = prompt
        self.CenterOnParent()
        self.panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(wx.StaticText(self.panel,-1,self.prompt),0,wx.ALIGN_CENTER)
        self.valItem = wx.TextCtrl(self.panel,-1,value=self.value,size=size)
        mainSizer.Add(self.valItem,0,wx.ALIGN_CENTER)
        btnsizer = wx.StdDialogButtonSizer()
        OKbtn = wx.Button(self.panel, wx.ID_OK)
        OKbtn.SetDefault()
        btnsizer.AddButton(OKbtn)
        btn = wx.Button(self.panel, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        mainSizer.Add(btnsizer,0,wx.ALIGN_CENTER)
        self.panel.SetSizer(mainSizer)
        self.panel.Fit()
        self.Fit()

    def Show(self):
        '''Use this method after creating the dialog to post it
        :returns: True if the user pressed OK; False if the User pressed Cancel
        '''
        if self.ShowModal() == wx.ID_OK:
            self.value = self.valItem.GetValue()
            return True
        else:
            return False

    def GetValue(self):
        '''Use this method to get the value entered by the user
        :returns: string entered by user
        '''
        return self.value

################################################################################
class MultiStringDialog(wx.Dialog):
    '''Dialog to obtain a multi string values from user
    
    :param wx.Frame parent: name of parent frame
    :param str title: title string for dialog
    :param str prompts: strings to tell use what they are inputting
    :param str values: default input values, if any
    '''
    def __init__(self,parent,title,prompts,values=[]):      #,size=(200,-1)?
        
        wx.Dialog.__init__(self,parent,wx.ID_ANY,title, 
                           pos=wx.DefaultPosition,
                           style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.values = values
        self.prompts = prompts
        self.CenterOnParent()
        self.panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        promptSizer = wx.FlexGridSizer(0,2,5,5)
        self.Indx = {}
        for prompt,value in zip(prompts,values):
            promptSizer.Add(wx.StaticText(self.panel,-1,prompt),0,WACV)
            valItem = wx.TextCtrl(self.panel,-1,value=value,style=wx.TE_PROCESS_ENTER)
            self.Indx[valItem.GetId()] = prompt
            valItem.Bind(wx.EVT_TEXT,self.newValue)
            promptSizer.Add(valItem,0,WACV)
        mainSizer.Add(promptSizer,0)
        btnsizer = wx.StdDialogButtonSizer()
        OKbtn = wx.Button(self.panel, wx.ID_OK)
        OKbtn.SetDefault()
        btnsizer.AddButton(OKbtn)
        btn = wx.Button(self.panel, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        mainSizer.Add(btnsizer,0,wx.ALIGN_CENTER)
        self.panel.SetSizer(mainSizer)
        self.panel.Fit()
        self.Fit()
        
    def newValue(self,event):
        Obj = event.GetEventObject()
        item = self.Indx[Obj.GetId()]
        id = self.prompts.index(item)
        self.values[id] = Obj.GetValue()

    def Show(self):
        '''Use this method after creating the dialog to post it
        :returns: True if the user pressed OK; False if the User pressed Cancel
        '''
        if self.ShowModal() == wx.ID_OK:
            return True
        else:
            return False

    def GetValues(self):
        '''Use this method to get the value entered by the user
        :returns: string entered by user
        '''
        return self.values

################################################################################

class G2MultiChoiceDialog(wx.Dialog):
    '''A dialog similar to MultiChoiceDialog except that buttons are
    added to set all choices and to toggle all choices.

    :param wx.Frame ParentFrame: reference to parent frame
    :param str title: heading above list of choices
    :param str header: Title to place on window frame 
    :param list ChoiceList: a list of choices where one will be selected
    :param bool toggle: If True (default) the toggle and select all buttons
      are displayed
    :param bool monoFont: If False (default), use a variable-spaced font;
      if True use a equally-spaced font.
    :param bool filterBox: If True (default) an input widget is placed on
      the window and only entries matching the entered text are shown.
    :param kw: optional keyword parameters for the wx.Dialog may
      be included such as size [which defaults to `(320,310)`] and
      style (which defaults to `wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.CENTRE| wx.OK | wx.CANCEL`);
      note that `wx.OK` and `wx.CANCEL` controls
      the presence of the eponymous buttons in the dialog.
    :returns: the name of the created dialog  
    '''
    def __init__(self,parent, title, header, ChoiceList, toggle=True,
                 monoFont=False, filterBox=True, **kw):
        # process keyword parameters, notably style
        options = {'size':(320,310), # default Frame keywords
                   'style':wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.CENTRE| wx.OK | wx.CANCEL,
                   }
        options.update(kw)
        self.ChoiceList = ChoiceList # list of choices (list of str values)
        self.Selections = len(self.ChoiceList) * [False,] # selection status for each choice (list of bools)
        self.filterlist = range(len(self.ChoiceList)) # list of the choice numbers that have been filtered (list of int indices)
        if options['style'] & wx.OK:
            useOK = True
            options['style'] ^= wx.OK
        else:
            useOK = False
        if options['style'] & wx.CANCEL:
            useCANCEL = True
            options['style'] ^= wx.CANCEL
        else:
            useCANCEL = False        
        # create the dialog frame
        wx.Dialog.__init__(self,parent,wx.ID_ANY,header,**options)
        # fill the dialog
        Sizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(
            wx.StaticText(self,wx.ID_ANY,title,size=(-1,35)),
            1,wx.ALL|wx.EXPAND|WACV,1)
        if filterBox:
            self.timer = wx.Timer()
            self.timer.Bind(wx.EVT_TIMER,self.Filter)
            topSizer.Add(wx.StaticText(self,wx.ID_ANY,'Name \nFilter: '),0,wx.ALL|WACV,1)
            self.filterBox = wx.TextCtrl(self, wx.ID_ANY, size=(80,-1),style=wx.TE_PROCESS_ENTER)
            self.filterBox.Bind(wx.EVT_CHAR,self.onChar)
            self.filterBox.Bind(wx.EVT_TEXT_ENTER,self.Filter)
            topSizer.Add(self.filterBox,0,wx.ALL|WACV,0)
        Sizer.Add(topSizer,0,wx.ALL|wx.EXPAND,8)
        self.trigger = False
        self.clb = wx.CheckListBox(self, wx.ID_ANY, (30,30), wx.DefaultSize, ChoiceList)
        self.clb.Bind(wx.EVT_CHECKLISTBOX,self.OnCheck)
        if monoFont:
            font1 = wx.Font(self.clb.GetFont().GetPointSize(),
                            wx.MODERN, wx.NORMAL, wx.NORMAL, False)
            self.clb.SetFont(font1)
        Sizer.Add(self.clb,1,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
        Sizer.Add((-1,10))
        # set/toggle buttons
        if toggle:
            bSizer = wx.BoxSizer(wx.VERTICAL)
            setBut = wx.Button(self,wx.ID_ANY,'Set All')
            setBut.Bind(wx.EVT_BUTTON,self._SetAll)
            bSizer.Add(setBut,0,wx.ALIGN_CENTER)
            bSizer.Add((-1,5))
            togBut = wx.Button(self,wx.ID_ANY,'Toggle All')
            togBut.Bind(wx.EVT_BUTTON,self._ToggleAll)
            bSizer.Add(togBut,0,wx.ALIGN_CENTER)
            Sizer.Add(bSizer,0,wx.LEFT,12)
        # OK/Cancel buttons
        btnsizer = wx.StdDialogButtonSizer()
        if useOK:
            self.OKbtn = wx.Button(self, wx.ID_OK)
            self.OKbtn.SetDefault()
            btnsizer.AddButton(self.OKbtn)
        if useCANCEL:
            btn = wx.Button(self, wx.ID_CANCEL)
            btnsizer.AddButton(btn)
        btnsizer.Realize()
        Sizer.Add((-1,5))
        Sizer.Add(btnsizer,0,wx.ALIGN_RIGHT,50)
        Sizer.Add((-1,20))
        # OK done, let's get outa here
        self.SetSizer(Sizer)
        self.CenterOnParent()
        
    def GetSelections(self):
        'Returns a list of the indices for the selected choices'
        # update self.Selections with settings for displayed items
        for i in range(len(self.filterlist)):
            self.Selections[self.filterlist[i]] = self.clb.IsChecked(i)
        # return all selections, shown or hidden
        return [i for i in range(len(self.Selections)) if self.Selections[i]]
        
    def SetSelections(self,selList):
        '''Sets the selection indices in selList as selected. Resets any previous
        selections for compatibility with wx.MultiChoiceDialog. Note that
        the state for only the filtered items is shown.

        :param list selList: indices of items to be selected. These indices
          are referenced to the order in self.ChoiceList
        '''
        self.Selections = len(self.ChoiceList) * [False,] # reset selections
        for sel in selList:
            self.Selections[sel] = True
        self._ShowSelections()

    def _ShowSelections(self):
        'Show the selection state for displayed items'
        self.clb.SetChecked(
            [i for i in range(len(self.filterlist)) if self.Selections[self.filterlist[i]]]
            ) # Note anything previously checked will be cleared.
            
    def _SetAll(self,event):
        'Set all viewed choices on'
        self.clb.SetChecked(range(len(self.filterlist)))
        
    def _ToggleAll(self,event):
        'flip the state of all viewed choices'
        for i in range(len(self.filterlist)):
            self.clb.Check(i,not self.clb.IsChecked(i))
            
    def onChar(self,event):
        'for keyboard events. self.trigger is used in self.OnCheck below'
        self.OKbtn.Enable(False)
        if event.GetKeyCode() == wx.WXK_SHIFT:
            self.trigger = True
        if self.timer.IsRunning():
            self.timer.Stop()
        self.timer.Start(1000,oneShot=True)
        event.Skip()
        
    def OnCheck(self,event):
        '''for CheckListBox events; if Shift key down this sets all unset 
            entries below the selected one'''
        if self.trigger:
            id = event.GetSelection()
            name = self.clb.GetString(id)            
            iB = id-1
            if iB < 0:
                return
            while not self.clb.IsChecked(iB):
                self.clb.Check(iB)
                iB -= 1
                if iB < 0:
                    break
        self.trigger = not self.trigger
        
    def Filter(self,event):
        if self.timer.IsRunning():
            self.timer.Stop()
        self.GetSelections() # record current selections
        txt = self.filterBox.GetValue()
        self.clb.Clear()
        
        self.Update()
        self.filterlist = []
        if txt:
            txt = txt.lower()
            ChoiceList = []
            for i,item in enumerate(self.ChoiceList):
                if item.lower().find(txt) != -1:
                    ChoiceList.append(item)
                    self.filterlist.append(i)
        else:
            self.filterlist = range(len(self.ChoiceList))
            ChoiceList = self.ChoiceList
        self.clb.AppendItems(ChoiceList)
        self._ShowSelections()
        self.OKbtn.Enable(True)

################################################################################

class G2SingleChoiceDialog(wx.Dialog):
    '''A dialog similar to wx.SingleChoiceDialog except that a filter can be
    added.

    :param wx.Frame ParentFrame: reference to parent frame
    :param str title: heading above list of choices
    :param str header: Title to place on window frame 
    :param list ChoiceList: a list of choices where one will be selected
    :param bool monoFont: If False (default), use a variable-spaced font;
      if True use a equally-spaced font.
    :param bool filterBox: If True (default) an input widget is placed on
      the window and only entries matching the entered text are shown.
    :param kw: optional keyword parameters for the wx.Dialog may
      be included such as size [which defaults to `(320,310)`] and
      style (which defaults to ``wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.CENTRE | wx.OK | wx.CANCEL``);
      note that ``wx.OK`` and ``wx.CANCEL`` controls
      the presence of the eponymous buttons in the dialog.
    :returns: the name of the created dialog
    '''
    def __init__(self,parent, title, header, ChoiceList, 
                 monoFont=False, filterBox=True, **kw):
        # process keyword parameters, notably style
        options = {'size':(320,310), # default Frame keywords
                   'style':wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.CENTRE| wx.OK | wx.CANCEL,
                   }
        options.update(kw)
        self.ChoiceList = ChoiceList
        self.filterlist = range(len(self.ChoiceList))
        if options['style'] & wx.OK:
            useOK = True
            options['style'] ^= wx.OK
        else:
            useOK = False
        if options['style'] & wx.CANCEL:
            useCANCEL = True
            options['style'] ^= wx.CANCEL
        else:
            useCANCEL = False        
        # create the dialog frame
        wx.Dialog.__init__(self,parent,wx.ID_ANY,header,**options)
        # fill the dialog
        Sizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(
            wx.StaticText(self,wx.ID_ANY,title,size=(-1,35)),
            1,wx.ALL|wx.EXPAND|WACV,1)
        if filterBox:
            self.timer = wx.Timer()
            self.timer.Bind(wx.EVT_TIMER,self.Filter)
            topSizer.Add(wx.StaticText(self,wx.ID_ANY,'Filter: '),0,wx.ALL,1)
            self.filterBox = wx.TextCtrl(self, wx.ID_ANY, size=(80,-1),
                                         style=wx.TE_PROCESS_ENTER)
            self.filterBox.Bind(wx.EVT_CHAR,self.onChar)
            self.filterBox.Bind(wx.EVT_TEXT_ENTER,self.Filter)
        topSizer.Add(self.filterBox,0,wx.ALL,0)
        Sizer.Add(topSizer,0,wx.ALL|wx.EXPAND,8)
        self.clb = wx.ListBox(self, wx.ID_ANY, (30,30), wx.DefaultSize, ChoiceList)
        self.clb.Bind(wx.EVT_LEFT_DCLICK,self.onDoubleClick)
        if monoFont:
            font1 = wx.Font(self.clb.GetFont().GetPointSize(),
                            wx.MODERN, wx.NORMAL, wx.NORMAL, False)
            self.clb.SetFont(font1)
        Sizer.Add(self.clb,1,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
        Sizer.Add((-1,10))
        # OK/Cancel buttons
        btnsizer = wx.StdDialogButtonSizer()
        if useOK:
            self.OKbtn = wx.Button(self, wx.ID_OK)
            self.OKbtn.SetDefault()
            btnsizer.AddButton(self.OKbtn)
        if useCANCEL:
            btn = wx.Button(self, wx.ID_CANCEL)
            btnsizer.AddButton(btn)
        btnsizer.Realize()
        Sizer.Add((-1,5))
        Sizer.Add(btnsizer,0,wx.ALIGN_RIGHT,50)
        Sizer.Add((-1,20))
        # OK done, let's get outa here
        self.SetSizer(Sizer)
    def GetSelection(self):
        'Returns the index of the selected choice'
        i = self.clb.GetSelection()
        if i < 0 or i >= len(self.filterlist):
            return wx.NOT_FOUND
        return self.filterlist[i]
    def onChar(self,event):
        self.OKbtn.Enable(False)
        if self.timer.IsRunning():
            self.timer.Stop()
        self.timer.Start(1000,oneShot=True)
        event.Skip()
    def Filter(self,event):
        if self.timer.IsRunning():
            self.timer.Stop()
        txt = self.filterBox.GetValue()
        self.clb.Clear()
        self.Update()
        self.filterlist = []
        if txt:
            txt = txt.lower()
            ChoiceList = []
            for i,item in enumerate(self.ChoiceList):
                if item.lower().find(txt) != -1:
                    ChoiceList.append(item)
                    self.filterlist.append(i)
        else:
            self.filterlist = range(len(self.ChoiceList))
            ChoiceList = self.ChoiceList
        self.clb.AppendItems(ChoiceList)
        self.OKbtn.Enable(True)
    def onDoubleClick(self,event):
        self.EndModal(wx.ID_OK)

################################################################################
class G2ColumnIDDialog(wx.Dialog):
    '''A dialog for matching column data to desired items; some columns may be ignored.
    
    :param wx.Frame ParentFrame: reference to parent frame
    :param str title: heading above list of choices
    :param str header: Title to place on window frame 
    :param list ChoiceList: a list of possible choices for the columns
    :param list ColumnData: lists of column data to be matched with ChoiceList
    :param bool monoFont: If False (default), use a variable-spaced font;
      if True use a equally-spaced font.
    :param kw: optional keyword parameters for the wx.Dialog may
      be included such as size [which defaults to `(320,310)`] and
      style (which defaults to ``wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.CENTRE | wx.OK | wx.CANCEL``);
      note that ``wx.OK`` and ``wx.CANCEL`` controls
      the presence of the eponymous buttons in the dialog.
    :returns: the name of the created dialog
    
    '''

    def __init__(self,parent, title, header,Comments,ChoiceList, ColumnData,
                 monoFont=False, **kw):

        def OnOk(sevent):
            OK = True
            selCols = []
            for col in self.sel:
                item = col.GetValue()
                if item != ' ' and item in selCols:
                    OK = False
                    break
                else:
                    selCols.append(item)
            parent = self.GetParent()
            if not OK:
                parent.ErrorDialog('Duplicate',item+' selected more than once')
                return
            parent.Raise()
            self.EndModal(wx.ID_OK)
            
        def OnModify(event):
            Obj = event.GetEventObject()
            icol,colData = Indx[Obj.GetId()]
            modify = Obj.GetValue()
            if not modify:
                return
            print 'Modify column',icol,' by', modify
            for i,item in enumerate(self.ColumnData[icol]):
                self.ColumnData[icol][i] = str(eval(item+modify))
            colData.SetValue('\n'.join(self.ColumnData[icol]))
            Obj.SetValue('')
            
        # process keyword parameters, notably style
        options = {'size':(600,310), # default Frame keywords
                   'style':wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.CENTRE| wx.OK | wx.CANCEL,
                   }
        options.update(kw)
        self.Comments = ''.join(Comments)
        self.ChoiceList = ChoiceList
        self.ColumnData = ColumnData
        nCol = len(ColumnData)
        if options['style'] & wx.OK:
            useOK = True
            options['style'] ^= wx.OK
        else:
            useOK = False
        if options['style'] & wx.CANCEL:
            useCANCEL = True
            options['style'] ^= wx.CANCEL
        else:
            useCANCEL = False        
        # create the dialog frame
        wx.Dialog.__init__(self,parent,wx.ID_ANY,header,**options)
        panel = wxscroll.ScrolledPanel(self)
        # fill the dialog
        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add((-1,5))
        Sizer.Add(wx.StaticText(panel,label=title),0,WACV)
        if self.Comments:
            Sizer.Add(wx.StaticText(panel,label=' Header lines:'),0,WACV)
            Sizer.Add(wx.TextCtrl(panel,value=self.Comments,size=(200,-1),
                style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP),0,wx.ALL|wx.EXPAND|WACV,8)
        columnsSizer = wx.FlexGridSizer(0,nCol,5,10)
        self.sel = []
        self.mod = []
        Indx = {}
        for icol,col in enumerate(self.ColumnData):
            colSizer = wx.BoxSizer(wx.VERTICAL)
            colSizer.Add(wx.StaticText(panel,label=' Column #%d Select:'%(icol)),0,WACV)
            self.sel.append(wx.ComboBox(panel,value=' ',choices=self.ChoiceList,style=wx.CB_READONLY|wx.CB_DROPDOWN))
            colSizer.Add(self.sel[-1])
            colData = wx.TextCtrl(panel,value='\n'.join(self.ColumnData[icol]),size=(120,-1),
                style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP)
            colSizer.Add(colData,0,WACV)
            colSizer.Add(wx.StaticText(panel,label=' Modify by:'),0,WACV)
            mod = wx.TextCtrl(panel,size=(120,-1),value='',style=wx.TE_PROCESS_ENTER)
            mod.Bind(wx.EVT_TEXT_ENTER,OnModify)
            mod.Bind(wx.EVT_KILL_FOCUS,OnModify)
            Indx[mod.GetId()] = [icol,colData]
            colSizer.Add(mod,0,WACV)
            columnsSizer.Add(colSizer)
        Sizer.Add(columnsSizer)
        Sizer.Add(wx.StaticText(panel,label=' For modify by, enter arithmetic string eg. "-12345.67". "+","-","*","/","**" all allowed'),0,WACV) 
        Sizer.Add((-1,10))
        # OK/Cancel buttons
        btnsizer = wx.StdDialogButtonSizer()
        if useOK:
            self.OKbtn = wx.Button(panel, wx.ID_OK)
            self.OKbtn.SetDefault()
            btnsizer.AddButton(self.OKbtn)
            self.OKbtn.Bind(wx.EVT_BUTTON, OnOk)
        if useCANCEL:
            btn = wx.Button(panel, wx.ID_CANCEL)
            btnsizer.AddButton(btn)
        btnsizer.Realize()
        Sizer.Add((-1,5))
        Sizer.Add(btnsizer,0,wx.ALIGN_LEFT,20)
        Sizer.Add((-1,5))
        # OK done, let's get outa here
        panel.SetSizer(Sizer)
        panel.SetAutoLayout(1)
        panel.SetupScrolling()
        Size = [450,375]
        panel.SetSize(Size)
        Size[0] += 25; Size[1]+= 25
        self.SetSize(Size)
        
    def GetSelection(self):
        'Returns the selected sample parm for each column'
        selCols = []
        for item in self.sel:
            selCols.append(item.GetValue())
        return selCols,self.ColumnData

################################################################################

def ItemSelector(ChoiceList, ParentFrame=None,
                 title='Select an item',
                 size=None, header='Item Selector',
                 useCancel=True,multiple=False):
    ''' Provide a wx dialog to select a single item or multiple items from list of choices

    :param list ChoiceList: a list of choices where one will be selected
    :param wx.Frame ParentFrame: Name of parent frame (default None)
    :param str title: heading above list of choices (default 'Select an item')
    :param wx.Size size: Size for dialog to be created (default None -- size as needed)
    :param str header: Title to place on window frame (default 'Item Selector')
    :param bool useCancel: If True (default) both the OK and Cancel buttons are offered
    :param bool multiple: If True then multiple items can be selected (default False)
    
    :returns: the selection index or None or a selection list if multiple is true
    '''
    if multiple:
        if useCancel:
            dlg = G2MultiChoiceDialog(
                ParentFrame,title, header, ChoiceList)
        else:
            dlg = G2MultiChoiceDialog(
                ParentFrame,title, header, ChoiceList,
                style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.OK|wx.CENTRE)
    else:
        if useCancel:
            dlg = wx.SingleChoiceDialog(
                ParentFrame,title, header, ChoiceList)
        else:
            dlg = wx.SingleChoiceDialog(
                ParentFrame,title, header,ChoiceList,
                style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.OK|wx.CENTRE)
    if size: dlg.SetSize(size)
    if dlg.ShowModal() == wx.ID_OK:
        if multiple:
            dlg.Destroy()
            return dlg.GetSelections()
        else:
            dlg.Destroy()
            return dlg.GetSelection()
    else:
        dlg.Destroy()
        return None
    dlg.Destroy()

################################################################################
class GridFractionEditor(wg.PyGridCellEditor):
    '''A grid cell editor class that allows entry of values as fractions as well
    as sine and cosine values [as s() and c()]
    '''
    def __init__(self,grid):
        wg.PyGridCellEditor.__init__(self)

    def Create(self, parent, id, evtHandler):
        self._tc = wx.TextCtrl(parent, id, "")
        self._tc.SetInsertionPoint(0)
        self.SetControl(self._tc)

        if evtHandler:
            self._tc.PushEventHandler(evtHandler)

        self._tc.Bind(wx.EVT_CHAR, self.OnChar)

    def SetSize(self, rect):
        self._tc.SetDimensions(rect.x, rect.y, rect.width+2, rect.height+2,
                               wx.SIZE_ALLOW_MINUS_ONE)

    def BeginEdit(self, row, col, grid):
        self.startValue = grid.GetTable().GetValue(row, col)
        self._tc.SetValue(str(self.startValue))
        self._tc.SetInsertionPointEnd()
        self._tc.SetFocus()
        self._tc.SetSelection(0, self._tc.GetLastPosition())

    def EndEdit(self, row, col, grid, oldVal=None):
        changed = False

        self.nextval = self.startValue
        val = self._tc.GetValue().lower()
        if val != self.startValue:
            changed = True
            neg = False
            if '-' in val:
                neg = True
            if '/' in val and '.' not in val:
                val += '.'
            elif 's' in val and not 'sind(' in val:
                if neg:
                    val = '-sind('+val.strip('-s')+')'
                else:
                    val = 'sind('+val.strip('s')+')'
            elif 'c' in val and not 'cosd(' in val:
                if neg:
                    val = '-cosd('+val.strip('-c')+')'
                else:
                    val = 'cosd('+val.strip('c')+')'
            try:
                self.nextval = val = float(eval(val))
            except (SyntaxError,NameError,ZeroDivisionError):
                val = self.startValue
                return None
            
            if oldVal is None: # this arg appears in 2.9+; before, we should go ahead & change the table
                grid.GetTable().SetValue(row, col, val) # update the table
            # otherwise self.ApplyEdit gets called

        self.startValue = ''
        self._tc.SetValue('')
        return changed
    
    def ApplyEdit(self, row, col, grid):
        """ Called only in wx >= 2.9
        Save the value of the control into the grid if EndEdit() returns as True
        """
        grid.GetTable().SetValue(row, col, self.nextval) # update the table

    def Reset(self):
        self._tc.SetValue(self.startValue)
        self._tc.SetInsertionPointEnd()

    def Clone(self):
        return GridFractionEditor(grid)

    def StartingKey(self, evt):
        self.OnChar(evt)
        if evt.GetSkipped():
            self._tc.EmulateKeyPress(evt)

    def OnChar(self, evt):
        key = evt.GetKeyCode()
        if key == 15:
            return
        if key > 255:
            evt.Skip()
            return
        char = chr(key)
        if char in '.+-/0123456789cosind()':
            self._tc.WriteText(char)
        else:
            evt.Skip()

################################################################################
class ShowLSParms(wx.Dialog):
    '''Create frame to show least-squares parameters
    '''
    def __init__(self,parent,title,parmDict,varyList,fullVaryList,
                 size=(300,430)):
        wx.Dialog.__init__(self,parent,wx.ID_ANY,title,size=size,
                           style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        panel = wxscroll.ScrolledPanel(
            self, wx.ID_ANY,
            #size=size,
            style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        num = len(varyList)
        mainSizer.Add(wx.StaticText(self,wx.ID_ANY,'Number of refined variables: '+str(num)))
        if len(varyList) != len(fullVaryList):
            num = len(fullVaryList) - len(varyList)
            mainSizer.Add(wx.StaticText(self,wx.ID_ANY,' + '+str(num)+' parameters are varied via constraints'))
        subSizer = wx.FlexGridSizer(cols=4,hgap=2,vgap=2)
        parmNames = parmDict.keys()
        parmNames.sort()
        subSizer.Add((-1,-1))
        subSizer.Add(wx.StaticText(panel,wx.ID_ANY,'Parameter name  '))
        subSizer.Add(wx.StaticText(panel,wx.ID_ANY,'refine?'))
        subSizer.Add(wx.StaticText(panel,wx.ID_ANY,'value'),0,wx.ALIGN_RIGHT)
        explainRefine = False
        for name in parmNames:
            # skip entries without numerical values
            if isinstance(parmDict[name],basestring): continue
            try:
                value = G2py3.FormatSigFigs(parmDict[name])
            except TypeError:
                value = str(parmDict[name])+' -?' # unexpected
                #continue
            v = G2obj.getVarDescr(name)
            if v is None or v[-1] is None:
                subSizer.Add((-1,-1))
            else:                
                ch = G2G.HelpButton(panel,G2obj.fmtVarDescr(name))
                subSizer.Add(ch,0,wx.LEFT|wx.RIGHT|WACV|wx.ALIGN_CENTER,1)
            subSizer.Add(wx.StaticText(panel,wx.ID_ANY,str(name)))
            if name in varyList:
                subSizer.Add(wx.StaticText(panel,wx.ID_ANY,'R'))
            elif name in fullVaryList:
                subSizer.Add(wx.StaticText(panel,wx.ID_ANY,'C'))
                explainRefine = True
            else:
                subSizer.Add((-1,-1))
            subSizer.Add(wx.StaticText(panel,wx.ID_ANY,value),0,wx.ALIGN_RIGHT)

        # finish up ScrolledPanel
        panel.SetSizer(subSizer)
        panel.SetAutoLayout(1)
        panel.SetupScrolling()
        mainSizer.Add(panel,1, wx.ALL|wx.EXPAND,1)

        if explainRefine:
            mainSizer.Add(
                wx.StaticText(self,wx.ID_ANY,
                          '"R" indicates a refined variable\n'+
                          '"C" indicates generated from a constraint'
                          ),
                0, wx.ALL,0)
        # make OK button 
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, wx.ID_CLOSE,"Close") 
        btn.Bind(wx.EVT_BUTTON,self._onClose)
        btnsizer.Add(btn)
        mainSizer.Add(btnsizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        # Allow window to be enlarged but not made smaller
        self.SetSizer(mainSizer)
        self.SetMinSize(self.GetSize())

    def _onClose(self,event):
        self.EndModal(wx.ID_CANCEL)
 
################################################################################
class DataFrame(wx.Frame):
    '''Create the data item window and all the entries in menus used in
    that window. For Linux and windows, the menu entries are created for the
    current data item window, but in the Mac the menu is accessed from all
    windows. This means that a different menu is posted depending on which
    data item is posted. On the Mac, all the menus contain the data tree menu
    items, but additional menus are added specific to the data item. 

    Note that while the menus are created here, 
    the binding for the menus is done later in various GSASII*GUI modules,
    where the functions to be called are defined.
    '''
    def Bind(self,eventtype,handler,*args,**kwargs):
        '''Override the Bind() function: on the Mac the binding is to
        the main window, so that menus operate with any window on top.
        For other platforms, either wrap calls that will be logged
        or call the default wx.Frame Bind() to bind to the menu item directly.

        Note that bindings can be made to objects by Id or by direct reference to the
        object. As a convention, when bindings are to objects, they are not logged
        but when bindings are by Id, they are logged.
        '''
        if sys.platform == "darwin": # mac
            self.G2frame.Bind(eventtype,handler,*args,**kwargs)
            return
        if eventtype == wx.EVT_MENU and 'id' in kwargs:
            menulabels = log.SaveMenuCommand(kwargs['id'],self.G2frame,handler)
            if menulabels:
                #print 'intercepting bind for',handler,menulabels,kwargs['id']
                wx.Frame.Bind(self,eventtype,self.G2frame.MenuBinding,*args,**kwargs)
                return
            wx.Frame.Bind(self,eventtype,handler,*args,**kwargs)      
        
    def PrefillDataMenu(self,menu,helpType,helpLbl=None,empty=False):
        '''Create the "standard" part of data frame menus. Note that on Linux and
        Windows nothing happens here. On Mac, this menu duplicates the
        tree menu, but adds an extra help command for the data item and a separator. 
        '''
        self.datamenu = menu
        self.G2frame.dataMenuBars.append(menu)
        self.helpType = helpType
        self.helpLbl = helpLbl
        if sys.platform == "darwin": # mac                         
            self.G2frame.FillMainMenu(menu) # add the data tree menu items
            if not empty:
                menu.Append(wx.Menu(title=''),title='|') # add a separator
        
    def PostfillDataMenu(self,empty=False):
        '''Create the "standard" part of data frame menus. Note that on Linux and
        Windows, this is the standard help Menu. On Mac, this menu duplicates the
        tree menu, but adds an extra help command for the data item and a separator. 
        '''
        menu = self.datamenu
        helpType = self.helpType
        helpLbl = self.helpLbl
        if sys.platform == "darwin": # mac
            if not empty:
                menu.Append(wx.Menu(title=''),title='|') # add another separator
            menu.Append(G2G.AddHelp(self.G2frame,helpType=helpType, helpLbl=helpLbl),
                        title='&Help')
        else: # other
            menu.Append(menu=G2G.MyHelp(self,helpType=helpType, helpLbl=helpLbl),
                        title='&Help')

    def _init_menus(self):
        'define all GSAS-II data frame menus'

        # for use where no menu or data frame help is provided
        self.BlankMenu = wx.MenuBar()
        
        # Controls
        self.ControlsMenu = wx.MenuBar()
        self.PrefillDataMenu(self.ControlsMenu,helpType='Controls',empty=True)
        self.PostfillDataMenu(empty=True)
        
        # Notebook
        self.DataNotebookMenu = wx.MenuBar() 
        self.PrefillDataMenu(self.DataNotebookMenu,helpType='Notebook',empty=True)
        self.PostfillDataMenu(empty=True)
        
        # Comments
        self.DataCommentsMenu = wx.MenuBar()
        self.PrefillDataMenu(self.DataCommentsMenu,helpType='Comments',empty=True)
        self.PostfillDataMenu(empty=True)
        
        # Constraints - something amiss here - get weird wx C++ error after refine!
        self.ConstraintMenu = wx.MenuBar()
        self.PrefillDataMenu(self.ConstraintMenu,helpType='Constraints')
        self.ConstraintTab = wx.Menu(title='')
        self.ConstraintMenu.Append(menu=self.ConstraintTab, title='Select tab')
        for id,txt in (
            (wxID_CONSPHASE,'Phase'),
            (wxID_CONSHAP,'Histogram/Phase'),
            (wxID_CONSHIST,'Histogram'),
            (wxID_CONSGLOBAL,'Global')):
            self.ConstraintTab.Append(
                id=id, kind=wx.ITEM_NORMAL,text=txt,
                help='Select '+txt+' constraint editing tab')
        self.ConstraintEdit = wx.Menu(title='')
        self.ConstraintMenu.Append(menu=self.ConstraintEdit, title='Edit')
        self.ConstraintEdit.Append(id=wxID_HOLDADD, kind=wx.ITEM_NORMAL,text='Add hold',
            help='Add hold on a parameter value')
        self.ConstraintEdit.Append(id=wxID_EQUIVADD, kind=wx.ITEM_NORMAL,text='Add equivalence',
            help='Add equivalence between parameter values')
        self.ConstraintEdit.Append(id=wxID_CONSTRAINTADD, kind=wx.ITEM_NORMAL,text='Add constraint',
            help='Add constraint on parameter values')
        self.ConstraintEdit.Append(id=wxID_FUNCTADD, kind=wx.ITEM_NORMAL,text='Add New Var',
            help='Add variable composed of existing parameter')
        self.PostfillDataMenu()

        # item = self.ConstraintEdit.Append(id=wx.ID_ANY,kind=wx.ITEM_NORMAL,text='Update GUI')
        # def UpdateGSASIIconstrGUI(event):
        #     import GSASIIconstrGUI
        #     reload(GSASIIconstrGUI)
        #     import GSASIIobj
        #     reload(GSASIIobj)
        # self.Bind(wx.EVT_MENU,UpdateGSASIIconstrGUI,id=item.GetId())

        # Rigid bodies
        self.RigidBodyMenu = wx.MenuBar()
        self.PrefillDataMenu(self.RigidBodyMenu,helpType='Rigid bodies')
        self.ResidueRBMenu = wx.Menu(title='')
        self.ResidueRBMenu.Append(id=wxID_RIGIDBODYIMPORT, kind=wx.ITEM_NORMAL,text='Import XYZ',
            help='Import rigid body XYZ from file')
        self.ResidueRBMenu.Append(id=wxID_RESIDUETORSSEQ, kind=wx.ITEM_NORMAL,text='Define sequence',
            help='Define torsion sequence')
        self.ResidueRBMenu.Append(id=wxID_RIGIDBODYADD, kind=wx.ITEM_NORMAL,text='Import residues',
            help='Import residue rigid bodies from macro file')
        self.RigidBodyMenu.Append(menu=self.ResidueRBMenu, title='Edit Body')
        self.PostfillDataMenu()

        self.VectorBodyMenu = wx.MenuBar()
        self.PrefillDataMenu(self.VectorBodyMenu,helpType='Vector rigid bodies')
        self.VectorRBEdit = wx.Menu(title='')
        self.VectorRBEdit.Append(id=wxID_VECTORBODYADD, kind=wx.ITEM_NORMAL,text='Add rigid body',
            help='Add vector rigid body')
        self.VectorBodyMenu.Append(menu=self.VectorRBEdit, title='Edit Vector Body')
        self.PostfillDataMenu()

                    
        # Restraints
        self.RestraintTab = wx.Menu(title='')
        self.RestraintEdit = wx.Menu(title='')
        self.RestraintEdit.Append(id=wxID_RESTSELPHASE, kind=wx.ITEM_NORMAL,text='Select phase',
            help='Select phase')
        self.RestraintEdit.Append(id=wxID_RESTRAINTADD, kind=wx.ITEM_NORMAL,text='Add restraints',
            help='Add restraints')
        self.RestraintEdit.Enable(wxID_RESTRAINTADD,True)    #gets disabled if macromolecule phase
        self.RestraintEdit.Append(id=wxID_AARESTRAINTADD, kind=wx.ITEM_NORMAL,text='Add residue restraints',
            help='Add residue based restraints for macromolecules from macro file')
        self.RestraintEdit.Enable(wxID_AARESTRAINTADD,False)    #gets enabled if macromolecule phase
        self.RestraintEdit.Append(id=wxID_AARESTRAINTPLOT, kind=wx.ITEM_NORMAL,text='Plot residue restraints',
            help='Plot selected residue based restraints for macromolecules from macro file')
        self.RestraintEdit.Enable(wxID_AARESTRAINTPLOT,False)    #gets enabled if macromolecule phase
        self.RestraintEdit.Append(id=wxID_RESRCHANGEVAL, kind=wx.ITEM_NORMAL,text='Change value',
            help='Change observed value')
        self.RestraintEdit.Append(id=wxID_RESTCHANGEESD, kind=wx.ITEM_NORMAL,text='Change esd',
            help='Change esd in observed value')
        self.RestraintEdit.Append(id=wxID_RESTDELETE, kind=wx.ITEM_NORMAL,text='Delete restraints',
            help='Delete selected restraints')

        self.RestraintMenu = wx.MenuBar()
        self.PrefillDataMenu(self.RestraintMenu,helpType='Restraints')
        self.RestraintMenu.Append(menu=self.RestraintTab, title='Select tab')
        self.RestraintMenu.Append(menu=self.RestraintEdit, title='Edit')
        self.PostfillDataMenu()
            
        # Sequential results
        self.SequentialMenu = wx.MenuBar()
        self.PrefillDataMenu(self.SequentialMenu,helpType='Sequential',helpLbl='Sequential Refinement')
        self.SequentialFile = wx.Menu(title='')
        self.SequentialMenu.Append(menu=self.SequentialFile, title='Columns')
        self.SequentialFile.Append(id=wxID_RENAMESEQSEL, kind=wx.ITEM_NORMAL,text='Rename selected',
            help='Rename selected sequential refinement columns')
        self.SequentialFile.Append(id=wxID_SAVESEQSEL, kind=wx.ITEM_NORMAL,text='Save selected as text',
            help='Save selected sequential refinement results as a text file')
        self.SequentialFile.Append(id=wxID_SAVESEQCSV, kind=wx.ITEM_NORMAL,text='Save all as CSV',
            help='Save all sequential refinement results as a CSV spreadsheet file')
        self.SequentialFile.Append(id=wxID_SAVESEQSELCSV, kind=wx.ITEM_NORMAL,text='Save selected as CSV',
            help='Save selected sequential refinement results as a CSV spreadsheet file')
        self.SequentialFile.Append(id=wxID_PLOTSEQSEL, kind=wx.ITEM_NORMAL,text='Plot selected',
            help='Plot selected sequential refinement results')
        self.SequentialFile.Append(id=wxID_ORGSEQSEL, kind=wx.ITEM_NORMAL,text='Reorganize',
            help='Reorganize variables where variables change')
        self.SequentialPvars = wx.Menu(title='')
        self.SequentialMenu.Append(menu=self.SequentialPvars, title='Pseudo Vars')
        self.SequentialPvars.Append(
            id=wxADDSEQVAR, kind=wx.ITEM_NORMAL,text='Add',
            help='Add a new pseudo-variable')
        self.SequentialPvars.Append(
            id=wxDELSEQVAR, kind=wx.ITEM_NORMAL,text='Delete',
            help='Delete an existing pseudo-variable')
        self.SequentialPvars.Append(
            id=wxEDITSEQVAR, kind=wx.ITEM_NORMAL,text='Edit',
            help='Edit an existing pseudo-variable')

        self.SequentialPfit = wx.Menu(title='')
        self.SequentialMenu.Append(menu=self.SequentialPfit, title='Parametric Fit')
        self.SequentialPfit.Append(
            id=wxADDPARFIT, kind=wx.ITEM_NORMAL,text='Add equation',
            help='Add a new equation to minimize')
        self.SequentialPfit.Append(
            id=wxCOPYPARFIT, kind=wx.ITEM_NORMAL,text='Copy equation',
            help='Copy an equation to minimize - edit it next')
        self.SequentialPfit.Append(
            id=wxDELPARFIT, kind=wx.ITEM_NORMAL,text='Delete equation',
            help='Delete an equation for parametric minimization')
        self.SequentialPfit.Append(
            id=wxEDITPARFIT, kind=wx.ITEM_NORMAL,text='Edit equation',
            help='Edit an existing parametric minimization equation')
        self.SequentialPfit.Append(
            id=wxDOPARFIT, kind=wx.ITEM_NORMAL,text='Fit to equation(s)',
            help='Perform a parametric minimization')
        self.PostfillDataMenu()
            
        # PWDR & SASD
        self.PWDRMenu = wx.MenuBar()
        self.PrefillDataMenu(self.PWDRMenu,helpType='PWDR Analysis',helpLbl='Powder Fit Error Analysis')
        self.ErrorAnal = wx.Menu(title='')
        self.PWDRMenu.Append(menu=self.ErrorAnal,title='Commands')
        self.ErrorAnal.Append(id=wxID_PWDANALYSIS,kind=wx.ITEM_NORMAL,text='Error Analysis',
            help='Error analysis on powder pattern')
        self.ErrorAnal.Append(id=wxID_PWDCOPY,kind=wx.ITEM_NORMAL,text='Copy params',
            help='Copy of PWDR parameters')
        self.ErrorAnal.Append(id=wxID_PLOTCTRLCOPY,kind=wx.ITEM_NORMAL,text='Copy plot controls',
            help='Copy of PWDR plot controls')
            
        self.PostfillDataMenu()
            
        # HKLF 
        self.HKLFMenu = wx.MenuBar()
        self.PrefillDataMenu(self.HKLFMenu,helpType='HKLF Analysis',helpLbl='HKLF Fit Error Analysis')
        self.ErrorAnal = wx.Menu(title='')
        self.HKLFMenu.Append(menu=self.ErrorAnal,title='Commands')
        self.ErrorAnal.Append(id=wxID_PWDANALYSIS,kind=wx.ITEM_NORMAL,text='Error Analysis',
            help='Error analysis on single crystal data')
        self.ErrorAnal.Append(id=wxID_PWD3DHKLPLOT,kind=wx.ITEM_NORMAL,text='Plot 3D HKLs',
            help='Plot HKLs from single crystal data in 3D')
        self.ErrorAnal.Append(id=wxID_PWDCOPY,kind=wx.ITEM_NORMAL,text='Copy params',
            help='Copy of HKLF parameters')
        self.PostfillDataMenu()
            
        # PDR / Limits
        self.LimitMenu = wx.MenuBar()
        self.PrefillDataMenu(self.LimitMenu,helpType='Limits')
        self.LimitEdit = wx.Menu(title='')
        self.LimitMenu.Append(menu=self.LimitEdit, title='Edit')
        self.LimitEdit.Append(id=wxID_LIMITCOPY, kind=wx.ITEM_NORMAL,text='Copy',
            help='Copy limits to other histograms')
        self.LimitEdit.Append(id=wxID_ADDEXCLREGION, kind=wx.ITEM_NORMAL,text='Add exclude',
            help='Add excluded region - select a point on plot; drag to adjust')            
        self.PostfillDataMenu()
            
        # PDR / Background
        self.BackMenu = wx.MenuBar()
        self.PrefillDataMenu(self.BackMenu,helpType='Background')
        self.BackEdit = wx.Menu(title='')
        self.BackMenu.Append(menu=self.BackEdit, title='File')
        self.BackEdit.Append(id=wxID_BACKCOPY, kind=wx.ITEM_NORMAL,text='Copy',
            help='Copy background parameters to other histograms')
        self.BackEdit.Append(id=wxID_BACKFLAGCOPY, kind=wx.ITEM_NORMAL,text='Copy flags',
            help='Copy background refinement flags to other histograms')
        self.PostfillDataMenu()
            
        # PDR / Instrument Parameters
        self.InstMenu = wx.MenuBar()
        self.PrefillDataMenu(self.InstMenu,helpType='Instrument Parameters')
        self.InstEdit = wx.Menu(title='')
        self.InstMenu.Append(menu=self.InstEdit, title='Operations')
        self.InstEdit.Append(help='Calibrate from indexed peaks', 
            id=wxID_INSTCALIB, kind=wx.ITEM_NORMAL,text='Calibrate')            
        self.InstEdit.Append(help='Reset instrument profile parameters to default', 
            id=wxID_INSTPRMRESET, kind=wx.ITEM_NORMAL,text='Reset profile')            
        self.InstEdit.Append(help='Load instrument profile parameters from file', 
            id=wxID_INSTLOAD, kind=wx.ITEM_NORMAL,text='Load profile...')            
        self.InstEdit.Append(help='Save instrument profile parameters to file', 
            id=wxID_INSTSAVE, kind=wx.ITEM_NORMAL,text='Save profile...')            
        self.InstEdit.Append(help='Copy instrument profile parameters to other histograms', 
            id=wxID_INSTCOPY, kind=wx.ITEM_NORMAL,text='Copy')
        self.InstEdit.Append(id=wxID_INSTFLAGCOPY, kind=wx.ITEM_NORMAL,text='Copy flags',
            help='Copy instrument parameter refinement flags to other histograms')
#        self.InstEdit.Append(help='Change radiation type (Ka12 - synch)', 
#            id=wxID_CHANGEWAVETYPE, kind=wx.ITEM_NORMAL,text='Change radiation')
        self.InstEdit.Append(id=wxID_INST1VAL, kind=wx.ITEM_NORMAL,text='Set one value',
            help='Set one instrument parameter value across multiple histograms')

        self.PostfillDataMenu()
        
        # PDR / Sample Parameters
        self.SampleMenu = wx.MenuBar()
        self.PrefillDataMenu(self.SampleMenu,helpType='Sample Parameters')
        self.SampleEdit = wx.Menu(title='')
        self.SampleMenu.Append(menu=self.SampleEdit, title='Command')
        self.SetScale = self.SampleEdit.Append(id=wxID_SETSCALE, kind=wx.ITEM_NORMAL,text='Set scale',
            help='Set scale by matching to another histogram')
        self.SampleEdit.Append(id=wxID_SAMPLELOAD, kind=wx.ITEM_NORMAL,text='Load',
            help='Load sample parameters from file')
        self.SampleEdit.Append(id=wxID_SAMPLESAVE, kind=wx.ITEM_NORMAL,text='Save',
            help='Save sample parameters to file')
        self.SampleEdit.Append(id=wxID_SAMPLECOPY, kind=wx.ITEM_NORMAL,text='Copy',
            help='Copy refinable and most other sample parameters to other histograms')
        self.SampleEdit.Append(id=wxID_SAMPLECOPYSOME, kind=wx.ITEM_NORMAL,text='Copy selected...',
            help='Copy selected sample parameters to other histograms')
        self.SampleEdit.Append(id=wxID_SAMPLEFLAGCOPY, kind=wx.ITEM_NORMAL,text='Copy flags',
            help='Copy sample parameter refinement flags to other histograms')
        self.SampleEdit.Append(id=wxID_SAMPLE1VAL, kind=wx.ITEM_NORMAL,text='Set one value',
            help='Set one sample parameter value across multiple histograms')
        self.SampleEdit.Append(id=wxID_ALLSAMPLELOAD, kind=wx.ITEM_NORMAL,text='Load all',
            help='Load sample parmameters over multiple histograms')

        self.PostfillDataMenu()
        self.SetScale.Enable(False)

        # PDR / Peak List
        self.PeakMenu = wx.MenuBar()
        self.PrefillDataMenu(self.PeakMenu,helpType='Peak List')
        self.PeakEdit = wx.Menu(title='')
        self.PeakMenu.Append(menu=self.PeakEdit, title='Peak Fitting')
        self.AutoSearch = self.PeakEdit.Append(help='Automatic peak search', 
            id=wxID_AUTOSEARCH, kind=wx.ITEM_NORMAL,text='Auto search')
        self.UnDo = self.PeakEdit.Append(help='Undo last least squares refinement', 
            id=wxID_UNDO, kind=wx.ITEM_NORMAL,text='UnDo')
        self.PeakFit = self.PeakEdit.Append(id=wxID_LSQPEAKFIT, kind=wx.ITEM_NORMAL,text='Peakfit', 
            help='Peak fitting' )
        self.PFOneCycle = self.PeakEdit.Append(id=wxID_LSQONECYCLE, kind=wx.ITEM_NORMAL,text='Peakfit one cycle', 
            help='One cycle of Peak fitting' )
        self.PeakEdit.Append(id=wxID_RESETSIGGAM, kind=wx.ITEM_NORMAL, 
            text='Reset sig and gam',help='Reset sigma and gamma to global fit' )
        self.PeakCopy = self.PeakEdit.Append(help='Copy peaks to other histograms', 
            id=wxID_PEAKSCOPY, kind=wx.ITEM_NORMAL,text='Peak copy')
        self.SeqPeakFit = self.PeakEdit.Append(id=wxID_SEQPEAKFIT, kind=wx.ITEM_NORMAL,text='Seq PeakFit', 
            help='Sequential Peak fitting for all histograms' )
        self.PeakEdit.Append(id=wxID_CLEARPEAKS, kind=wx.ITEM_NORMAL,text='Clear peaks', 
            help='Clear the peak list' )
        self.PostfillDataMenu()
        self.UnDo.Enable(False)
        self.PeakFit.Enable(False)
        self.PFOneCycle.Enable(False)
        self.AutoSearch.Enable(True)
        
        # PDR / Index Peak List
        self.IndPeaksMenu = wx.MenuBar()
        self.PrefillDataMenu(self.IndPeaksMenu,helpType='Index Peak List')
        self.IndPeaksEdit = wx.Menu(title='')
        self.IndPeaksMenu.Append(menu=self.IndPeaksEdit,title='Operations')
        self.IndPeaksEdit.Append(help='Load/Reload index peaks from peak list',id=wxID_INDXRELOAD, 
            kind=wx.ITEM_NORMAL,text='Load/Reload')
        self.PostfillDataMenu()
        
        # PDR / Unit Cells List
        self.IndexMenu = wx.MenuBar()
        self.PrefillDataMenu(self.IndexMenu,helpType='Unit Cells List')
        self.IndexEdit = wx.Menu(title='')
        self.IndexMenu.Append(menu=self.IndexEdit, title='Cell Index/Refine')
        self.IndexPeaks = self.IndexEdit.Append(help='', id=wxID_INDEXPEAKS, kind=wx.ITEM_NORMAL,
            text='Index Cell')
        self.CopyCell = self.IndexEdit.Append( id=wxID_COPYCELL, kind=wx.ITEM_NORMAL,text='Copy Cell', 
            help='Copy selected unit cell from indexing to cell refinement fields')
        self.RefineCell = self.IndexEdit.Append( id=wxID_REFINECELL, kind=wx.ITEM_NORMAL, 
            text='Refine Cell',help='Refine unit cell parameters from indexed peaks')
        self.MakeNewPhase = self.IndexEdit.Append( id=wxID_MAKENEWPHASE, kind=wx.ITEM_NORMAL,
            text='Make new phase',help='Make new phase from selected unit cell')
        self.PostfillDataMenu()
        self.IndexPeaks.Enable(False)
        self.CopyCell.Enable(False)
        self.RefineCell.Enable(False)
        self.MakeNewPhase.Enable(False)
        
        # PDR / Reflection Lists
        self.ReflMenu = wx.MenuBar()
        self.PrefillDataMenu(self.ReflMenu,helpType='Reflection List')
        self.ReflEdit = wx.Menu(title='')
        self.ReflMenu.Append(menu=self.ReflEdit, title='Reflection List')
        self.SelectPhase = self.ReflEdit.Append(help='Select phase for reflection list',id=wxID_SELECTPHASE, 
            kind=wx.ITEM_NORMAL,text='Select phase')
        self.ReflEdit.Append(id=wxID_PWDHKLPLOT,kind=wx.ITEM_NORMAL,text='Plot HKLs',
            help='Plot HKLs from powder pattern')
        self.ReflEdit.Append(id=wxID_PWD3DHKLPLOT,kind=wx.ITEM_NORMAL,text='Plot 3D HKLs',
            help='Plot HKLs from powder pattern in 3D')
        self.PostfillDataMenu()
        
        # SASD / Instrument Parameters
        self.SASDInstMenu = wx.MenuBar()
        self.PrefillDataMenu(self.SASDInstMenu,helpType='Instrument Parameters')
        self.SASDInstEdit = wx.Menu(title='')
        self.SASDInstMenu.Append(menu=self.SASDInstEdit, title='Operations')
        self.InstEdit.Append(help='Reset instrument profile parameters to default', 
            id=wxID_INSTPRMRESET, kind=wx.ITEM_NORMAL,text='Reset profile')
        self.SASDInstEdit.Append(help='Copy instrument profile parameters to other histograms', 
            id=wxID_INSTCOPY, kind=wx.ITEM_NORMAL,text='Copy')
        self.PostfillDataMenu()
        
        #SASD & REFL/ Substance editor
        self.SubstanceMenu = wx.MenuBar()
        self.PrefillDataMenu(self.SubstanceMenu,helpType='Substances')
        self.SubstanceEdit = wx.Menu(title='')
        self.SubstanceMenu.Append(menu=self.SubstanceEdit, title='Edit')
        self.SubstanceEdit.Append(id=wxID_LOADSUBSTANCE, kind=wx.ITEM_NORMAL,text='Load substance',
            help='Load substance from file')
        self.SubstanceEdit.Append(id=wxID_ADDSUBSTANCE, kind=wx.ITEM_NORMAL,text='Add substance',
            help='Add new substance to list')
        self.SubstanceEdit.Append(id=wxID_COPYSUBSTANCE, kind=wx.ITEM_NORMAL,text='Copy substances',
            help='Copy substances')
        self.SubstanceEdit.Append(id=wxID_DELETESUBSTANCE, kind=wx.ITEM_NORMAL,text='Delete substance',
            help='Delete substance from list')            
        self.SubstanceEdit.Append(id=wxID_ELEMENTADD, kind=wx.ITEM_NORMAL,text='Add elements',
            help='Add elements to substance')
        self.SubstanceEdit.Append(id=wxID_ELEMENTDELETE, kind=wx.ITEM_NORMAL,text='Delete elements',
            help='Delete elements from substance')
        self.PostfillDataMenu()
        
        # SASD/ Models
        self.ModelMenu = wx.MenuBar()
        self.PrefillDataMenu(self.ModelMenu,helpType='Models')
        self.ModelEdit = wx.Menu(title='')
        self.ModelMenu.Append(menu=self.ModelEdit, title='Models')
        self.ModelEdit.Append(id=wxID_MODELADD,kind=wx.ITEM_NORMAL,text='Add',
            help='Add new term to model')
        self.ModelEdit.Append(id=wxID_MODELFIT, kind=wx.ITEM_NORMAL,text='Fit',
            help='Fit model parameters to data')
        self.SasdUndo = self.ModelEdit.Append(id=wxID_MODELUNDO, kind=wx.ITEM_NORMAL,text='Undo',
            help='Undo model fit')
        self.SasdUndo.Enable(False)            
        self.ModelEdit.Append(id=wxID_MODELFITALL, kind=wx.ITEM_NORMAL,text='Sequential fit',
            help='Sequential fit of model parameters to all SASD data')
        self.ModelEdit.Append(id=wxID_MODELCOPY, kind=wx.ITEM_NORMAL,text='Copy',
            help='Copy model parameters to other histograms')
        self.ModelEdit.Append(id=wxID_MODELCOPYFLAGS, kind=wx.ITEM_NORMAL,text='Copy flags',
            help='Copy model refinement flags to other histograms')
        self.PostfillDataMenu()
        
        # IMG / Image Controls
        self.ImageMenu = wx.MenuBar()
        self.PrefillDataMenu(self.ImageMenu,helpType='Image Controls')
        self.ImageEdit = wx.Menu(title='')
        self.ImageMenu.Append(menu=self.ImageEdit, title='Operations')
        self.ImageEdit.Append(help='Calibrate detector by fitting to calibrant lines', 
            id=wxID_IMCALIBRATE, kind=wx.ITEM_NORMAL,text='Calibrate')
        self.ImageEdit.Append(help='Recalibrate detector by fitting to calibrant lines', 
            id=wxID_IMRECALIBRATE, kind=wx.ITEM_NORMAL,text='Recalibrate')
        self.ImageEdit.Append(help='Clear calibration data points and rings',id=wxID_IMCLEARCALIB, 
            kind=wx.ITEM_NORMAL,text='Clear calibration')
        self.ImageEdit.Append(help='Integrate selected image',id=wxID_IMINTEGRATE, 
            kind=wx.ITEM_NORMAL,text='Integrate')
        self.ImageEdit.Append(help='Integrate all images selected from list',id=wxID_INTEGRATEALL,
            kind=wx.ITEM_NORMAL,text='Integrate all')
        self.ImageEdit.Append(help='Copy image controls to other images', 
            id=wxID_IMCOPYCONTROLS, kind=wx.ITEM_NORMAL,text='Copy Controls')
        self.ImageEdit.Append(help='Save image controls to file', 
            id=wxID_IMSAVECONTROLS, kind=wx.ITEM_NORMAL,text='Save Controls')
        self.ImageEdit.Append(help='Load image controls from file', 
            id=wxID_IMLOADCONTROLS, kind=wx.ITEM_NORMAL,text='Load Controls')
        self.PostfillDataMenu()
            
        # IMG / Masks
        self.MaskMenu = wx.MenuBar()
        self.PrefillDataMenu(self.MaskMenu,helpType='Image Masks')
        self.MaskEdit = wx.Menu(title='')
        self.MaskMenu.Append(menu=self.MaskEdit, title='Operations')
        submenu = wx.Menu()
        self.MaskEdit.AppendMenu(
            wx.ID_ANY,'Create new', submenu,
            help=''
            )
        self.MaskEdit.Append(help='Copy mask to other images', 
            id=wxID_MASKCOPY, kind=wx.ITEM_NORMAL,text='Copy mask')
        self.MaskEdit.Append(help='Save mask to file', 
            id=wxID_MASKSAVE, kind=wx.ITEM_NORMAL,text='Save mask')
        self.MaskEdit.Append(help='Load mask from file', 
            id=wxID_MASKLOAD, kind=wx.ITEM_NORMAL,text='Load mask')
        self.MaskEdit.Append(help='Load mask from file; ignore threshold', 
            id=wxID_MASKLOADNOT, kind=wx.ITEM_NORMAL,text='Load mask w/o threshold')
        submenu.Append(help='Create an arc mask with mouse input', 
            id=wxID_NEWMASKARC, kind=wx.ITEM_NORMAL,text='Arc mask')
        submenu.Append(help='Create a frame mask with mouse input', 
            id=wxID_NEWMASKFRAME, kind=wx.ITEM_NORMAL,text='Frame mask')
        submenu.Append(help='Create a polygon mask with mouse input', 
            id=wxID_NEWMASKPOLY, kind=wx.ITEM_NORMAL,text='Polygon mask')
        submenu.Append(help='Create a ring mask with mouse input', 
            id=wxID_NEWMASKRING, kind=wx.ITEM_NORMAL,text='Ring mask')
        submenu.Append(help='Create a spot mask with mouse input', 
            id=wxID_NEWMASKSPOT, kind=wx.ITEM_NORMAL,text='Spot mask')
        self.PostfillDataMenu()
            
        # IMG / Stress/Strain
        self.StrStaMenu = wx.MenuBar()
        self.PrefillDataMenu(self.StrStaMenu,helpType='Stress/Strain')
        self.StrStaEdit = wx.Menu(title='')
        self.StrStaMenu.Append(menu=self.StrStaEdit, title='Operations')
        self.StrStaEdit.Append(help='Append d-zero for one ring', 
            id=wxID_APPENDDZERO, kind=wx.ITEM_NORMAL,text='Append d-zero')
        self.StrStaEdit.Append(help='Fit stress/strain data', 
            id=wxID_STRSTAFIT, kind=wx.ITEM_NORMAL,text='Fit stress/strain')
        self.StrStaEdit.Append(help='Update d-zero from ave d-zero',
            id=wxID_UPDATEDZERO, kind=wx.ITEM_NORMAL,text='Update d-zero')        
        self.StrStaEdit.Append(help='Fit stress/strain data for all images', 
            id=wxID_STRSTAALLFIT, kind=wx.ITEM_NORMAL,text='All image fit')
        self.StrStaEdit.Append(help='Copy stress/strain data to other images', 
            id=wxID_STRSTACOPY, kind=wx.ITEM_NORMAL,text='Copy stress/strain')
        self.StrStaEdit.Append(help='Save stress/strain data to file', 
            id=wxID_STRSTASAVE, kind=wx.ITEM_NORMAL,text='Save stress/strain')
        self.StrStaEdit.Append(help='Load stress/strain data from file', 
            id=wxID_STRSTALOAD, kind=wx.ITEM_NORMAL,text='Load stress/strain')
        self.StrStaEdit.Append(help='Load sample data from file', 
            id=wxID_STRSTSAMPLE, kind=wx.ITEM_NORMAL,text='Load sample data')
        self.PostfillDataMenu()
            
        # PDF / PDF Controls
        self.PDFMenu = wx.MenuBar()
        self.PrefillDataMenu(self.PDFMenu,helpType='PDF Controls')
        self.PDFEdit = wx.Menu(title='')
        self.PDFMenu.Append(menu=self.PDFEdit, title='PDF Controls')
        self.PDFEdit.Append(help='Add element to sample composition',id=wxID_PDFADDELEMENT, kind=wx.ITEM_NORMAL,
            text='Add element')
        self.PDFEdit.Append(help='Delete element from sample composition',id=wxID_PDFDELELEMENT, kind=wx.ITEM_NORMAL,
            text='Delete element')
        self.PDFEdit.Append(help='Copy PDF controls', id=wxID_PDFCOPYCONTROLS, kind=wx.ITEM_NORMAL,
            text='Copy controls')
        self.PDFEdit.Append(help='Load PDF controls from file',id=wxID_PDFLOADCONTROLS, kind=wx.ITEM_NORMAL,
            text='Load Controls')
        self.PDFEdit.Append(help='Save PDF controls to file', id=wxID_PDFSAVECONTROLS, kind=wx.ITEM_NORMAL,
            text='Save controls')
        self.PDFEdit.Append(help='Compute PDF', id=wxID_PDFCOMPUTE, kind=wx.ITEM_NORMAL,
            text='Compute PDF')
        self.PDFEdit.Append(help='Compute all PDFs', id=wxID_PDFCOMPUTEALL, kind=wx.ITEM_NORMAL,
            text='Compute all PDFs')
        self.PostfillDataMenu()
        
        # Phase / General tab
        self.DataGeneral = wx.MenuBar()
        self.PrefillDataMenu(self.DataGeneral,helpType='General', helpLbl='Phase/General')
        self.DataGeneral.Append(menu=wx.Menu(title=''),title='Select tab')
        self.GeneralCalc = wx.Menu(title='')
        self.DataGeneral.Append(menu=self.GeneralCalc,title='Compute')
        self.GeneralCalc.Append(help='Compute Fourier map',id=wxID_FOURCALC, kind=wx.ITEM_NORMAL,
            text='Fourier map')
        self.GeneralCalc.Append(help='Search Fourier map',id=wxID_FOURSEARCH, kind=wx.ITEM_NORMAL,
            text='Search map')
        self.GeneralCalc.Append(help='Run charge flipping',id=wxID_CHARGEFLIP, kind=wx.ITEM_NORMAL,
            text='Charge flipping')
        self.GeneralCalc.Append(help='Run 4D charge flipping',id=wxID_4DCHARGEFLIP, kind=wx.ITEM_NORMAL,
            text='4D Charge flipping')
        self.GeneralCalc.Enable(wxID_4DCHARGEFLIP,False)   
        self.GeneralCalc.Append(help='Clear map',id=wxID_FOURCLEAR, kind=wx.ITEM_NORMAL,
            text='Clear map')
        self.GeneralCalc.Append(help='Run Monte Carlo - Simulated Annealing',id=wxID_SINGLEMCSA, kind=wx.ITEM_NORMAL,
            text='MC/SA')
        self.GeneralCalc.Append(help='Run Monte Carlo - Simulated Annealing on multiprocessors',id=wxID_MULTIMCSA, kind=wx.ITEM_NORMAL,
            text='Multi MC/SA')            #currently not useful
        self.PostfillDataMenu()
        
        # Phase / Data tab
        self.DataMenu = wx.MenuBar()
        self.PrefillDataMenu(self.DataMenu,helpType='Data', helpLbl='Phase/Data')
        self.DataMenu.Append(menu=wx.Menu(title=''),title='Select tab')
        self.DataEdit = wx.Menu(title='')
        self.DataMenu.Append(menu=self.DataEdit, title='Edit')
        self.DataEdit.Append(id=wxID_PWDRADD, kind=wx.ITEM_NORMAL,text='Add powder histograms',
            help='Select new powder histograms to be used for this phase')
        self.DataEdit.Append(id=wxID_HKLFADD, kind=wx.ITEM_NORMAL,text='Add single crystal histograms',
            help='Select new single crystal histograms to be used for this phase')
        self.DataEdit.Append(id=wxID_DATADELETE, kind=wx.ITEM_NORMAL,text='Remove histograms',
            help='Remove histograms from use for this phase')
        self.PostfillDataMenu()
            
        # Phase / Atoms tab
        self.AtomsMenu = wx.MenuBar()
        self.PrefillDataMenu(self.AtomsMenu,helpType='Atoms')
        self.AtomsMenu.Append(menu=wx.Menu(title=''),title='Select tab')
        self.AtomEdit = wx.Menu(title='')
        self.AtomCompute = wx.Menu(title='')
        self.AtomsMenu.Append(menu=self.AtomEdit, title='Edit')
        self.AtomsMenu.Append(menu=self.AtomCompute, title='Compute')
        self.AtomEdit.Append(id=wxID_ATOMSEDITADD, kind=wx.ITEM_NORMAL,text='Append atom',
            help='Appended as an H atom')
        self.AtomEdit.Append(id=wxID_ATOMSVIEWADD, kind=wx.ITEM_NORMAL,text='Append view point',
            help='Appended as an H atom')
        self.AtomEdit.Append(id=wxID_ATOMSEDITINSERT, kind=wx.ITEM_NORMAL,text='Insert atom',
            help='Select atom row to insert before; inserted as an H atom')
        self.AtomEdit.Append(id=wxID_ATOMVIEWINSERT, kind=wx.ITEM_NORMAL,text='Insert view point',
            help='Select atom row to insert before; inserted as an H atom')
        self.AtomEdit.Append(id=wxID_ATOMMOVE, kind=wx.ITEM_NORMAL,text='Move atom to view point',
            help='Select single atom to move')
        self.AtomEdit.Append(id=wxID_ATOMSEDITDELETE, kind=wx.ITEM_NORMAL,text='Delete atom',
            help='Select atoms to delete first')
        self.AtomEdit.Append(id=wxID_ATOMSREFINE, kind=wx.ITEM_NORMAL,text='Set atom refinement flags',
            help='Select atoms to refine first')
        self.AtomEdit.Append(id=wxID_ATOMSMODIFY, kind=wx.ITEM_NORMAL,text='Modify atom parameters',
            help='Select atoms to modify first')
        self.AtomEdit.Append(id=wxID_ATOMSTRANSFORM, kind=wx.ITEM_NORMAL,text='Transform atoms',
            help='Select atoms to transform first')
        self.AtomEdit.Append(id=wxID_MAKEMOLECULE, kind=wx.ITEM_NORMAL,text='Assemble molecule',
            help='Assemble molecule from scatterd atom positions')
        self.AtomEdit.Append(id=wxID_RELOADDRAWATOMS, kind=wx.ITEM_NORMAL,text='Reload draw atoms',
            help='Reload atom drawing list')
        submenu = wx.Menu()
        self.AtomEdit.AppendMenu(wx.ID_ANY, 'Reimport atoms', submenu, 
            help='Reimport atoms from file; sequence must match')
        # setup a cascade menu for the formats that have been defined
        self.ReImportMenuId = {}  # points to readers for each menu entry
        for reader in self.G2frame.ImportPhaseReaderlist:
            item = submenu.Append(
                wx.ID_ANY,help=reader.longFormatName,
                kind=wx.ITEM_NORMAL,text='reimport coordinates from '+reader.formatName+' file')
            self.ReImportMenuId[item.GetId()] = reader
        item = submenu.Append(
            wx.ID_ANY,
            help='Reimport coordinates, try to determine format from file',
            kind=wx.ITEM_NORMAL,
            text='guess format from file')
        self.ReImportMenuId[item.GetId()] = None # try all readers

        self.AtomCompute.Append(id=wxID_ATOMSDISAGL, kind=wx.ITEM_NORMAL,text='Show Distances && Angles',
            help='Compute distances & angles for selected atoms')
        self.AtomCompute.Append(id=wxID_ATOMSPDISAGL, kind=wx.ITEM_NORMAL,text='Save Distances && Angles',
            help='Compute distances & angles for selected atoms')
        self.AtomCompute.ISOcalc = self.AtomCompute.Append(
            id=wxID_ISODISP, kind=wx.ITEM_NORMAL,
            text='Compute ISODISTORT mode values',
            help='Compute values of ISODISTORT modes from atom parameters')
        self.PostfillDataMenu()
        
        # Phase / Imcommensurate "waves" tab
        self.WavesData = wx.MenuBar()
        self.PrefillDataMenu(self.WavesData,helpType='Wave Data', helpLbl='Imcommensurate wave data')
        self.WavesData.Append(menu=wx.Menu(title=''),title='Select tab')
        self.WavesDataCompute = wx.Menu(title='')
        self.WavesData.Append(menu=self.WavesDataCompute,title='Compute')
        self.WavesDataCompute.Append(id=wxID_4DMAPCOMPUTE, kind=wx.ITEM_NORMAL,text='Compute 4D map',
            help='Compute 4-dimensional map')
        self.PostfillDataMenu()
                 
        # Phase / Draw Options tab
        self.DataDrawOptions = wx.MenuBar()
        self.PrefillDataMenu(self.DataDrawOptions,helpType='Draw Options', helpLbl='Phase/Draw Options')
        self.DataDrawOptions.Append(menu=wx.Menu(title=''),title='Select tab')
        self.PostfillDataMenu()
        
        # Phase / Draw Atoms tab 
        self.DrawAtomsMenu = wx.MenuBar()
        self.PrefillDataMenu(self.DrawAtomsMenu,helpType='Draw Atoms')
        self.DrawAtomsMenu.Append(menu=wx.Menu(title=''),title='Select tab')
        self.DrawAtomEdit = wx.Menu(title='')
        self.DrawAtomCompute = wx.Menu(title='')
        self.DrawAtomRestraint = wx.Menu(title='')
        self.DrawAtomRigidBody = wx.Menu(title='')
        self.DrawAtomsMenu.Append(menu=self.DrawAtomEdit, title='Edit')
        self.DrawAtomsMenu.Append(menu=self.DrawAtomCompute,title='Compute')
        self.DrawAtomsMenu.Append(menu=self.DrawAtomRestraint, title='Restraints')
        self.DrawAtomsMenu.Append(menu=self.DrawAtomRigidBody, title='Rigid body')
        self.DrawAtomEdit.Append(id=wxID_DRAWATOMSTYLE, kind=wx.ITEM_NORMAL,text='Atom style',
            help='Select atoms first')
        self.DrawAtomEdit.Append(id=wxID_DRAWATOMLABEL, kind=wx.ITEM_NORMAL,text='Atom label',
            help='Select atoms first')
        self.DrawAtomEdit.Append(id=wxID_DRAWATOMCOLOR, kind=wx.ITEM_NORMAL,text='Atom color',
            help='Select atoms first')
        self.DrawAtomEdit.Append(id=wxID_DRAWATOMRESETCOLOR, kind=wx.ITEM_NORMAL,text='Reset atom colors',
            help='Resets all atom colors to defaults')
        self.DrawAtomEdit.Append(id=wxID_DRAWVIEWPOINT, kind=wx.ITEM_NORMAL,text='View point',
            help='View point is 1st atom selected')
        self.DrawAtomEdit.Append(id=wxID_DRAWADDEQUIV, kind=wx.ITEM_NORMAL,text='Add atoms',
            help='Add symmetry & cell equivalents to drawing set from selected atoms')
        self.DrawAtomEdit.Append(id=wxID_DRAWTRANSFORM, kind=wx.ITEM_NORMAL,text='Transform draw atoms',
            help='Transform selected atoms by symmetry & cell translations')
        self.DrawAtomEdit.Append(id=wxID_DRAWFILLCOORD, kind=wx.ITEM_NORMAL,text='Fill CN-sphere',
            help='Fill coordination sphere for selected atoms')            
        self.DrawAtomEdit.Append(id=wxID_DRAWFILLCELL, kind=wx.ITEM_NORMAL,text='Fill unit cell',
            help='Fill unit cell with selected atoms')
        self.DrawAtomEdit.Append(id=wxID_DRAWDELETE, kind=wx.ITEM_NORMAL,text='Delete atoms',
            help='Delete atoms from drawing set')
        self.DrawAtomCompute.Append(id=wxID_DRAWDISTVP, kind=wx.ITEM_NORMAL,text='View pt. dist.',
            help='Compute distance of selected atoms from view point')   
        self.DrawAtomCompute.Append(id=wxID_DRAWDISAGLTOR, kind=wx.ITEM_NORMAL,text='Dist. Ang. Tors.',
            help='Compute distance, angle or torsion for 2-4 selected atoms')   
        self.DrawAtomCompute.Append(id=wxID_DRAWPLANE, kind=wx.ITEM_NORMAL,text='Best plane',
            help='Compute best plane for 4+ selected atoms')   
        self.DrawAtomRestraint.Append(id=wxID_DRAWRESTRBOND, kind=wx.ITEM_NORMAL,text='Add bond restraint',
            help='Add bond restraint for selected atoms (2)')
        self.DrawAtomRestraint.Append(id=wxID_DRAWRESTRANGLE, kind=wx.ITEM_NORMAL,text='Add angle restraint',
            help='Add angle restraint for selected atoms (3: one end 1st)')
        self.DrawAtomRestraint.Append(id=wxID_DRAWRESTRPLANE, kind=wx.ITEM_NORMAL,text='Add plane restraint',
            help='Add plane restraint for selected atoms (4+)')
        self.DrawAtomRestraint.Append(id=wxID_DRAWRESTRCHIRAL, kind=wx.ITEM_NORMAL,text='Add chiral restraint',
            help='Add chiral restraint for selected atoms (4: center atom 1st)')
        self.DrawAtomRigidBody.Append(id=wxID_DRAWDEFINERB, kind=wx.ITEM_NORMAL,text='Define rigid body',
            help='Define rigid body with selected atoms')
        self.PostfillDataMenu()

        # Phase / MCSA tab
        self.MCSAMenu = wx.MenuBar()
        self.PrefillDataMenu(self.MCSAMenu,helpType='MC/SA')
        self.MCSAMenu.Append(menu=wx.Menu(title=''),title='Select tab')
        self.MCSAEdit = wx.Menu(title='')
        self.MCSAMenu.Append(menu=self.MCSAEdit, title='MC/SA')
        self.MCSAEdit.Append(id=wxID_ADDMCSAATOM, kind=wx.ITEM_NORMAL,text='Add atom', 
            help='Add single atom to MC/SA model')
        self.MCSAEdit.Append(id=wxID_ADDMCSARB, kind=wx.ITEM_NORMAL,text='Add rigid body', 
            help='Add rigid body to MC/SA model' )
        self.MCSAEdit.Append(id=wxID_CLEARMCSARB, kind=wx.ITEM_NORMAL,text='Clear rigid bodies', 
            help='Clear all atoms & rigid bodies from MC/SA model' )
        self.MCSAEdit.Append(id=wxID_MOVEMCSA, kind=wx.ITEM_NORMAL,text='Move MC/SA solution', 
            help='Move MC/SA solution to atom list' )
        self.MCSAEdit.Append(id=wxID_MCSACLEARRESULTS, kind=wx.ITEM_NORMAL,text='Clear results', 
            help='Clear table of MC/SA results' )
        self.PostfillDataMenu()
            
        # Phase / Texture tab
        self.TextureMenu = wx.MenuBar()
        self.PrefillDataMenu(self.TextureMenu,helpType='Texture')
        self.TextureMenu.Append(menu=wx.Menu(title=''),title='Select tab')
        self.TextureEdit = wx.Menu(title='')
        self.TextureMenu.Append(menu=self.TextureEdit, title='Texture')
#        self.TextureEdit.Append(id=wxID_REFINETEXTURE, kind=wx.ITEM_NORMAL,text='Refine texture', 
#            help='Refine the texture coefficients from sequential Pawley results')
# N.B. Binding is now commented out
        self.TextureEdit.Append(id=wxID_CLEARTEXTURE, kind=wx.ITEM_NORMAL,text='Clear texture', 
            help='Clear the texture coefficients' )
        self.PostfillDataMenu()
            
        # Phase / Pawley tab
        self.PawleyMenu = wx.MenuBar()
        self.PrefillDataMenu(self.PawleyMenu,helpType='Pawley')
        self.PawleyMenu.Append(menu=wx.Menu(title=''),title='Select tab')
        self.PawleyEdit = wx.Menu(title='')
        self.PawleyMenu.Append(menu=self.PawleyEdit,title='Operations')
        self.PawleyEdit.Append(id=wxID_PAWLEYLOAD, kind=wx.ITEM_NORMAL,text='Pawley create',
            help='Initialize Pawley reflection list')
        self.PawleyEdit.Append(id=wxID_PAWLEYESTIMATE, kind=wx.ITEM_NORMAL,text='Pawley estimate',
            help='Estimate initial Pawley intensities')
        self.PawleyEdit.Append(id=wxID_PAWLEYUPDATE, kind=wx.ITEM_NORMAL,text='Pawley update',
            help='Update negative Pawley intensities with -0.5*Fobs and turn off refinemnt')
        self.PostfillDataMenu()
            
        # Phase / Map peaks tab
        self.MapPeaksMenu = wx.MenuBar()
        self.PrefillDataMenu(self.MapPeaksMenu,helpType='Map peaks')
        self.MapPeaksMenu.Append(menu=wx.Menu(title=''),title='Select tab')
        self.MapPeaksEdit = wx.Menu(title='')
        self.MapPeaksMenu.Append(menu=self.MapPeaksEdit, title='Map peaks')
        self.MapPeaksEdit.Append(id=wxID_PEAKSMOVE, kind=wx.ITEM_NORMAL,text='Move peaks', 
            help='Move selected peaks to atom list')
        self.MapPeaksEdit.Append(id=wxID_PEAKSVIEWPT, kind=wx.ITEM_NORMAL,text='View point',
            help='View point is 1st peak selected')
        self.MapPeaksEdit.Append(id=wxID_PEAKSDISTVP, kind=wx.ITEM_NORMAL,text='View pt. dist.',
            help='Compute distance of selected peaks from view point')   
        self.MapPeaksEdit.Append(id=wxID_SHOWBONDS, kind=wx.ITEM_NORMAL,text='Hide bonds',
            help='Hide or show bonds between peak positions')   
        self.MapPeaksEdit.Append(id=wxID_PEAKSDA, kind=wx.ITEM_NORMAL,text='Calc dist/ang', 
            help='Calculate distance or angle for selection')
        self.MapPeaksEdit.Append(id=wxID_FINDEQVPEAKS, kind=wx.ITEM_NORMAL,text='Equivalent peaks', 
            help='Find equivalent peaks')
        self.MapPeaksEdit.Append(id=wxID_PEAKSUNIQUE, kind=wx.ITEM_NORMAL,text='Unique peaks', 
            help='Select unique set')
        self.MapPeaksEdit.Append(id=wxID_PEAKSDELETE, kind=wx.ITEM_NORMAL,text='Delete peaks', 
            help='Delete selected peaks')
        self.MapPeaksEdit.Append(id=wxID_PEAKSCLEAR, kind=wx.ITEM_NORMAL,text='Clear peaks', 
            help='Clear the map peak list')
        self.PostfillDataMenu()

        # Phase / Rigid bodies tab
        self.RigidBodiesMenu = wx.MenuBar()
        self.PrefillDataMenu(self.RigidBodiesMenu,helpType='Rigid bodies')
        self.RigidBodiesMenu.Append(menu=wx.Menu(title=''),title='Select tab')
        self.RigidBodiesEdit = wx.Menu(title='')
        self.RigidBodiesMenu.Append(menu=self.RigidBodiesEdit, title='Edit')
        self.RigidBodiesEdit.Append(id=wxID_ASSIGNATMS2RB, kind=wx.ITEM_NORMAL,text='Assign atoms to rigid body',
            help='Select & position rigid body in structure of existing atoms')
        self.RigidBodiesEdit.Append(id=wxID_AUTOFINDRESRB, kind=wx.ITEM_NORMAL,text='Auto find residues',
            help='Auto find of residue RBs in macromolecule')
        self.RigidBodiesEdit.Append(id=wxID_COPYRBPARMS, kind=wx.ITEM_NORMAL,text='Copy rigid body parms',
            help='Copy rigid body location & TLS parameters')
        self.RigidBodiesEdit.Append(id=wxID_GLOBALTHERM, kind=wx.ITEM_NORMAL,text='Global thermal motion',
            help='Global setting of residue thermal motion models')
        self.RigidBodiesEdit.Append(id=wxID_GLOBALRESREFINE, kind=wx.ITEM_NORMAL,text='Global residue refine',
            help='Global setting of residue RB refinement flags')
        self.RigidBodiesEdit.Append(id=wxID_RBREMOVEALL, kind=wx.ITEM_NORMAL,text='Remove all rigid bodies',
            help='Remove all rigid body assignment for atoms')
        self.PostfillDataMenu()
    # end of GSAS-II menu definitions
        
    def _init_ctrls(self, parent,name=None,size=None,pos=None):
        wx.Frame.__init__(
            self,parent=parent,
            #style=wx.DEFAULT_FRAME_STYLE ^ wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT ,
            style=wx.DEFAULT_FRAME_STYLE ^ wx.CLOSE_BOX,
            size=size,pos=pos,title='GSAS-II data display')
        self._init_menus()
        if name:
            self.SetLabel(name)
        self.Show()
        
    def __init__(self,parent,frame,data=None,name=None, size=None,pos=None):
        self.G2frame = frame
        self._init_ctrls(parent,name,size,pos)
        self.data = data
        clientSize = wx.ClientDisplayRect()
        Size = self.GetSize()
        xPos = clientSize[2]-Size[0]
        self.SetPosition(wx.Point(xPos,clientSize[1]+250))
        self.AtomGrid = []
        self.selectedRow = 0
        
    def setSizePosLeft(self,Width):
        clientSize = wx.ClientDisplayRect()
        Width[1] = min(Width[1],clientSize[2]-300)
        Width[0] = max(Width[0],300)
        self.SetSize(Width)
#        self.SetPosition(wx.Point(clientSize[2]-Width[0],clientSize[1]+250))
        
    def Clear(self):
        self.ClearBackground()
        self.DestroyChildren()
                   
################################################################################
#####  GSNotebook
################################################################################           
       
class GSNoteBook(wx.aui.AuiNotebook):
    '''Notebook used in various locations; implemented with wx.aui extension
    '''
    def __init__(self, parent, name='',size = None):
        wx.aui.AuiNotebook.__init__(self, parent, -1,
                                    style=wx.aui.AUI_NB_TOP |
                                    wx.aui.AUI_NB_SCROLL_BUTTONS)
        if size: self.SetSize(size)
        self.parent = parent
        self.PageChangeHandler = None
        
    def PageChangeEvent(self,event):
        G2frame = self.parent.G2frame
        page = event.GetSelection()
        if self.PageChangeHandler:
            if log.LogInfo['Logging']:
                log.MakeTabLog(
                    G2frame.dataFrame.GetTitle(),
                    G2frame.dataDisplay.GetPageText(page)
                    )
            self.PageChangeHandler(event)
            
    def Bind(self,eventtype,handler,*args,**kwargs):
        '''Override the Bind() function so that page change events can be trapped
        '''
        if eventtype == wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED:
            self.PageChangeHandler = handler
            wx.aui.AuiNotebook.Bind(self,eventtype,self.PageChangeEvent)
            return
        wx.aui.AuiNotebook.Bind(self,eventtype,handler,*args,**kwargs)
                                                      
    def Clear(self):        
        GSNoteBook.DeleteAllPages(self)
        
    def FindPage(self,name):
        numPage = self.GetPageCount()
        for page in range(numPage):
            if self.GetPageText(page) == name:
                return page

    def ChangeSelection(self,page):
        # in wx.Notebook ChangeSelection is like SetSelection, but it
        # does not invoke the event related to pressing the tab button
        # I don't see a way to do that in aui.
        oldPage = self.GetSelection()
        self.SetSelection(page)
        return oldPage

    # def __getattribute__(self,name):
    #     '''This method provides a way to print out a message every time
    #     that a method in a class is called -- to see what all the calls
    #     might be, or where they might be coming from.
    #     Cute trick for debugging!
    #     '''
    #     attr = object.__getattribute__(self, name)
    #     if hasattr(attr, '__call__'):
    #         def newfunc(*args, **kwargs):
    #             print('GSauiNoteBook calling %s' %attr.__name__)
    #             result = attr(*args, **kwargs)
    #             return result
    #         return newfunc
    #     else:
    #         return attr
            
################################################################################
#####  GSGrid
################################################################################           
       
class GSGrid(wg.Grid):
    '''Basic wx.Grid implementation
    '''
    def __init__(self, parent, name=''):
        wg.Grid.__init__(self,parent,-1,name=name)                    
        #self.SetSize(parent.GetClientSize())
        # above removed to speed drawing of initial grid
        # does not appear to be needed
            
    def Clear(self):
        wg.Grid.ClearGrid(self)
        
    def SetCellReadOnly(self,r,c,readonly=True):
        self.SetReadOnly(r,c,isReadOnly=readonly)
        
    def SetCellStyle(self,r,c,color="white",readonly=True):
        self.SetCellBackgroundColour(r,c,color)
        self.SetReadOnly(r,c,isReadOnly=readonly)
        
    def GetSelection(self):
        #this is to satisfy structure drawing stuff in G2plt when focus changes
        return None

    def InstallGridToolTip(self, rowcolhintcallback,
                           colLblCallback=None,rowLblCallback=None):
        '''code to display a tooltip for each item on a grid
        from http://wiki.wxpython.org/wxGrid%20ToolTips (buggy!), expanded to
        column and row labels using hints from
        https://groups.google.com/forum/#!topic/wxPython-users/bm8OARRVDCs

        :param function rowcolhintcallback: a routine that returns a text
          string depending on the selected row and column, to be used in
          explaining grid entries.
        :param function colLblCallback: a routine that returns a text
          string depending on the selected column, to be used in
          explaining grid columns (if None, the default), column labels
          do not get a tooltip.
        :param function rowLblCallback: a routine that returns a text
          string depending on the selected row, to be used in
          explaining grid rows (if None, the default), row labels
          do not get a tooltip.
        '''
        prev_rowcol = [None,None,None]
        def OnMouseMotion(event):
            # event.GetRow() and event.GetCol() would be nice to have here,
            # but as this is a mouse event, not a grid event, they are not
            # available and we need to compute them by hand.
            x, y = self.CalcUnscrolledPosition(event.GetPosition())
            row = self.YToRow(y)
            col = self.XToCol(x)
            hinttext = ''
            win = event.GetEventObject()
            if [row,col,win] == prev_rowcol: # no change from last position
                event.Skip()
                return
            if win == self.GetGridWindow() and row >= 0 and col >= 0:
                hinttext = rowcolhintcallback(row, col)
            elif win == self.GetGridColLabelWindow() and col >= 0:
                if colLblCallback: hinttext = colLblCallback(col)
            elif win == self.GetGridRowLabelWindow() and row >= 0:
                if rowLblCallback: hinttext = rowLblCallback(row)
            else: # this should be the upper left corner, which is empty
                event.Skip()
                return
            if hinttext is None: hinttext = ''
            win.SetToolTipString(hinttext)
            prev_rowcol[:] = [row,col,win]
            event.Skip()

        wx.EVT_MOTION(self.GetGridWindow(), OnMouseMotion)
        if colLblCallback: wx.EVT_MOTION(self.GetGridColLabelWindow(), OnMouseMotion)
        if rowLblCallback: wx.EVT_MOTION(self.GetGridRowLabelWindow(), OnMouseMotion)
                                                    
################################################################################
#####  Table
################################################################################           
       
class Table(wg.PyGridTableBase):
    '''Basic data table for use with GSgrid
    '''
    def __init__(self, data=[], rowLabels=None, colLabels=None, types = None):
        wg.PyGridTableBase.__init__(self)
        self.colLabels = colLabels
        self.rowLabels = rowLabels
        self.dataTypes = types
        self.data = data
        
    def AppendRows(self, numRows=1):
        self.data.append([])
        return True
        
    def CanGetValueAs(self, row, col, typeName):
        if self.dataTypes:
            colType = self.dataTypes[col].split(':')[0]
            if typeName == colType:
                return True
            else:
                return False
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)

    def DeleteRow(self,pos):
        data = self.GetData()
        self.SetData([])
        new = []
        for irow,row in enumerate(data):
            if irow <> pos:
                new.append(row)
        self.SetData(new)
        
    def GetColLabelValue(self, col):
        if self.colLabels:
            return self.colLabels[col]
            
    def GetData(self):
        data = []
        for row in range(self.GetNumberRows()):
            data.append(self.GetRowValues(row))
        return data
        
    def GetNumberCols(self):
        try:
            return len(self.colLabels)
        except TypeError:
            return None
        
    def GetNumberRows(self):
        return len(self.data)
        
    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]
        
    def GetColValues(self, col):
        data = []
        for row in range(self.GetNumberRows()):
            data.append(self.GetValue(row, col))
        return data
        
    def GetRowValues(self, row):
        data = []
        for col in range(self.GetNumberCols()):
            data.append(self.GetValue(row, col))
        return data
        
    def GetTypeName(self, row, col):
        try:
            if self.data[row][col] is None: return None
            return self.dataTypes[col]
        except (TypeError,IndexError):
            return None

    def GetValue(self, row, col):
        try:
            if self.data[row][col] is None: return ""
            return self.data[row][col]
        except IndexError:
            return None
            
    def InsertRows(self, pos, rows):
        for row in range(rows):
            self.data.insert(pos,[])
            pos += 1
        
    def IsEmptyCell(self,row,col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True
        
    def OnKeyPress(self, event):
        dellist = self.GetSelectedRows()
        if event.GetKeyCode() == wx.WXK_DELETE and dellist:
            grid = self.GetView()
            for i in dellist: grid.DeleteRow(i)
                
    def SetColLabelValue(self, col, label):
        numcols = self.GetNumberCols()
        if col > numcols-1:
            self.colLabels.append(label)
        else:
            self.colLabels[col]=label
        
    def SetData(self,data):
        for row in range(len(data)):
            self.SetRowValues(row,data[row])
                
    def SetRowLabelValue(self, row, label):
        self.rowLabels[row]=label
            
    def SetRowValues(self,row,data):
        self.data[row] = data
            
    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except TypeError:
                return
            except IndexError:
                print row,col,value
                # add a new row
                if row > self.GetNumberRows():
                    self.data.append([''] * self.GetNumberCols())
                elif col > self.GetNumberCols():
                    for row in range(self.GetNumberRows):
                        self.data[row].append('')
                print self.data
                self.data[row][col] = value
        innerSetValue(row, col, value)

################################################################################
#####  Notebook
################################################################################           
       
def UpdateNotebook(G2frame,data):
    '''Called when the data tree notebook entry is selected. Allows for
    editing of the text in that tree entry
    '''
    def OnNoteBook(event):
        data = G2frame.dataDisplay.GetValue().split('\n')
        G2frame.PatternTree.SetItemPyData(GetPatternTreeItemId(G2frame,G2frame.root,'Notebook'),data)
        if 'nt' not in os.name:
            G2frame.dataDisplay.AppendText('\n')
                    
    if G2frame.dataDisplay:
        G2frame.dataDisplay.Destroy()
    G2frame.dataFrame.SetLabel('Notebook')
    G2frame.dataDisplay = wx.TextCtrl(parent=G2frame.dataFrame,size=G2frame.dataFrame.GetClientSize(),
        style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER | wx.TE_DONTWRAP)
    G2frame.dataDisplay.Bind(wx.EVT_TEXT_ENTER,OnNoteBook)
    G2frame.dataDisplay.Bind(wx.EVT_KILL_FOCUS,OnNoteBook)
    for line in data:
        G2frame.dataDisplay.AppendText(line+"\n")
    G2frame.dataDisplay.AppendText('Notebook entry @ '+time.ctime()+"\n")
    G2frame.dataFrame.setSizePosLeft([400,250])
            
################################################################################
#####  Controls
################################################################################           
       
def UpdateControls(G2frame,data):
    '''Edit overall GSAS-II controls in main Controls data tree entry
    '''
    #patch
    if 'deriv type' not in data:
        data = {}
        data['deriv type'] = 'analytic Hessian'
        data['min dM/M'] = 0.0001
        data['shift factor'] = 1.
        data['max cyc'] = 3        
        data['F**2'] = True
        data['minF/sig'] = 0
    if 'shift factor' not in data:
        data['shift factor'] = 1.
    if 'max cyc' not in data:
        data['max cyc'] = 3
    if 'F**2' not in data:
        data['F**2'] = True
        data['minF/sig'] = 0
    if 'Author' not in data:
        data['Author'] = 'no name'
    if 'FreePrm1' not in data:
        data['FreePrm1'] = 'Sample humidity (%)'
    if 'FreePrm2' not in data:
        data['FreePrm2'] = 'Sample voltage (V)'
    if 'FreePrm3' not in data:
        data['FreePrm3'] = 'Applied load (MN)'
    if 'Copy2Next' not in data:
        data['Copy2Next'] = False
    if 'Reverse Seq' not in data:
        data['Reverse Seq'] = False   
     
    
    #end patch

    def SeqSizer():
        
        def OnSelectData(event):
            choices = GetPatternTreeDataNames(G2frame,['PWDR',])
            sel = []
            if 'Seq Data' in data:
                for item in data['Seq Data']:
                    sel.append(choices.index(item))
                sel = [choices.index(item) for item in data['Seq Data']]
            dlg = G2MultiChoiceDialog(G2frame.dataFrame, 'Sequential refinement',
                                      'Select dataset to include',
                                      choices)
            dlg.SetSelections(sel)
            names = []
            if dlg.ShowModal() == wx.ID_OK:
                for sel in dlg.GetSelections():
                    names.append(choices[sel])
                data['Seq Data'] = names                
                G2frame.EnableSeqRefineMenu()
            dlg.Destroy()
            wx.CallAfter(UpdateControls,G2frame,data)
            
        def OnReverse(event):
            data['Reverse Seq'] = reverseSel.GetValue()
            
        def OnCopySel(event):
            data['Copy2Next'] = copySel.GetValue() 
                    
        seqSizer = wx.BoxSizer(wx.VERTICAL)
        dataSizer = wx.BoxSizer(wx.HORIZONTAL)
        dataSizer.Add(wx.StaticText(G2frame.dataDisplay,label=' Sequential Refinement: '),0,WACV)
        selSeqData = wx.Button(G2frame.dataDisplay,-1,label=' Select data')
        selSeqData.Bind(wx.EVT_BUTTON,OnSelectData)
        dataSizer.Add(selSeqData,0,WACV)
        SeqData = data.get('Seq Data',[])
        if not SeqData:
            lbl = ' (no powder data selected)'
        else:
            lbl = ' ('+str(len(SeqData))+' dataset(s) selected)'

        dataSizer.Add(wx.StaticText(G2frame.dataDisplay,label=lbl),0,WACV)
        seqSizer.Add(dataSizer,0)
        if SeqData:
            selSizer = wx.BoxSizer(wx.HORIZONTAL)
            reverseSel = wx.CheckBox(G2frame.dataDisplay,-1,label=' Reverse order?')
            reverseSel.Bind(wx.EVT_CHECKBOX,OnReverse)
            reverseSel.SetValue(data['Reverse Seq'])
            selSizer.Add(reverseSel,0,WACV)
            copySel =  wx.CheckBox(G2frame.dataDisplay,-1,label=' Copy results to next histogram?')
            copySel.Bind(wx.EVT_CHECKBOX,OnCopySel)
            copySel.SetValue(data['Copy2Next'])
            selSizer.Add(copySel,0,WACV)
            seqSizer.Add(selSizer,0)
        return seqSizer
        
    def LSSizer():        
        
        def OnDerivType(event):
            data['deriv type'] = derivSel.GetValue()
            derivSel.SetValue(data['deriv type'])
            wx.CallAfter(UpdateControls,G2frame,data)
            
        def OnConvergence(event):
            try:
                value = max(1.e-9,min(1.0,float(Cnvrg.GetValue())))
            except ValueError:
                value = 0.0001
            data['min dM/M'] = value
            Cnvrg.SetValue('%.2g'%(value))
            
        def OnMaxCycles(event):
            data['max cyc'] = int(maxCyc.GetValue())
            maxCyc.SetValue(str(data['max cyc']))
                        
        def OnFactor(event):
            try:
                value = min(max(float(Factr.GetValue()),0.00001),100.)
            except ValueError:
                value = 1.0
            data['shift factor'] = value
            Factr.SetValue('%.5f'%(value))
            
        def OnFsqRef(event):
            data['F**2'] = fsqRef.GetValue()
        
        def OnMinSig(event):
            try:
                value = min(max(float(minSig.GetValue()),0.),5.)
            except ValueError:
                value = 1.0
            data['minF/sig'] = value
            minSig.SetValue('%.2f'%(value))

        LSSizer = wx.FlexGridSizer(cols=4,vgap=5,hgap=5)
        LSSizer.Add(wx.StaticText(G2frame.dataDisplay,label=' Refinement derivatives: '),0,WACV)
        Choice=['analytic Jacobian','numeric','analytic Hessian']
        derivSel = wx.ComboBox(parent=G2frame.dataDisplay,value=data['deriv type'],choices=Choice,
            style=wx.CB_READONLY|wx.CB_DROPDOWN)
        derivSel.SetValue(data['deriv type'])
        derivSel.Bind(wx.EVT_COMBOBOX, OnDerivType)
            
        LSSizer.Add(derivSel,0,WACV)
        LSSizer.Add(wx.StaticText(G2frame.dataDisplay,label=' Min delta-M/M: '),0,WACV)
        Cnvrg = wx.TextCtrl(G2frame.dataDisplay,-1,value='%.2g'%(data['min dM/M']),style=wx.TE_PROCESS_ENTER)
        Cnvrg.Bind(wx.EVT_TEXT_ENTER,OnConvergence)
        Cnvrg.Bind(wx.EVT_KILL_FOCUS,OnConvergence)
        LSSizer.Add(Cnvrg,0,WACV)
        if 'Hessian' in data['deriv type']:
            LSSizer.Add(wx.StaticText(G2frame.dataDisplay,label=' Max cycles: '),0,WACV)
            Choice = ['0','1','2','3','5','10','15','20']
            maxCyc = wx.ComboBox(parent=G2frame.dataDisplay,value=str(data['max cyc']),choices=Choice,
                style=wx.CB_READONLY|wx.CB_DROPDOWN)
            maxCyc.SetValue(str(data['max cyc']))
            maxCyc.Bind(wx.EVT_COMBOBOX, OnMaxCycles)
            LSSizer.Add(maxCyc,0,WACV)
        else:
            LSSizer.Add(wx.StaticText(G2frame.dataDisplay,label=' Initial shift factor: '),0,WACV)
            Factr = wx.TextCtrl(G2frame.dataDisplay,-1,value='%.5f'%(data['shift factor']),style=wx.TE_PROCESS_ENTER)
            Factr.Bind(wx.EVT_TEXT_ENTER,OnFactor)
            Factr.Bind(wx.EVT_KILL_FOCUS,OnFactor)
            LSSizer.Add(Factr,0,WACV)
        if G2frame.Sngl:
            LSSizer.Add((1,0),)
            LSSizer.Add((1,0),)
            fsqRef = wx.CheckBox(G2frame.dataDisplay,-1,label='Refine HKLF as F^2? ')
            fsqRef.SetValue(data['F**2'])
            fsqRef.Bind(wx.EVT_CHECKBOX,OnFsqRef)
            LSSizer.Add(fsqRef,0,WACV)
            LSSizer.Add(wx.StaticText(G2frame.dataDisplay,-1,label='Min obs/sig (0-5): '),0,WACV)
            minSig = wx.TextCtrl(G2frame.dataDisplay,-1,value='%.2f'%(data['minF/sig']),style=wx.TE_PROCESS_ENTER)
            minSig.Bind(wx.EVT_TEXT_ENTER,OnMinSig)
            minSig.Bind(wx.EVT_KILL_FOCUS,OnMinSig)
            LSSizer.Add(minSig,0,WACV)
        return LSSizer
        
    def AuthSizer():

        def OnAuthor(event):
            data['Author'] = auth.GetValue()

        Author = data['Author']
        authSizer = wx.BoxSizer(wx.HORIZONTAL)
        authSizer.Add(wx.StaticText(G2frame.dataDisplay,label=' CIF Author (last, first):'),0,WACV)
        auth = wx.TextCtrl(G2frame.dataDisplay,-1,value=Author,style=wx.TE_PROCESS_ENTER)
        auth.Bind(wx.EVT_TEXT_ENTER,OnAuthor)
        auth.Bind(wx.EVT_KILL_FOCUS,OnAuthor)
        authSizer.Add(auth,0,WACV)
        return authSizer
        
        
    if G2frame.dataDisplay:
        G2frame.dataDisplay.Destroy()
    if not G2frame.dataFrame.GetStatusBar():
        Status = G2frame.dataFrame.CreateStatusBar()
        Status.SetStatusText('')
    G2frame.dataFrame.SetLabel('Controls')
    G2frame.dataDisplay = wx.Panel(G2frame.dataFrame)
    SetDataMenuBar(G2frame,G2frame.dataFrame.ControlsMenu)
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add((5,5),0)
    mainSizer.Add(wx.StaticText(G2frame.dataDisplay,label=' Refinement Controls:'),0,WACV)    
    mainSizer.Add(LSSizer())
    mainSizer.Add((5,5),0)
    mainSizer.Add(SeqSizer())
    mainSizer.Add((5,5),0)
    mainSizer.Add(AuthSizer())
    mainSizer.Add((5,5),0)
        
    mainSizer.Layout()    
    G2frame.dataDisplay.SetSizer(mainSizer)
    G2frame.dataDisplay.SetSize(mainSizer.Fit(G2frame.dataFrame))
    G2frame.dataFrame.setSizePosLeft(mainSizer.Fit(G2frame.dataFrame))
     
################################################################################
#####  Comments
################################################################################           
       
def UpdateComments(G2frame,data):                   

    if G2frame.dataDisplay:
        G2frame.dataDisplay.Destroy()
    G2frame.dataFrame.SetLabel('Comments')
    G2frame.dataDisplay = wx.TextCtrl(parent=G2frame.dataFrame,size=G2frame.dataFrame.GetClientSize(),
        style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP)
    for line in data:
        G2frame.dataDisplay.AppendText(line+'\n')
    G2frame.dataFrame.setSizePosLeft([400,250])
            
################################################################################
#####  Display of Sequential Results
################################################################################           
       
def UpdateSeqResults(G2frame,data,prevSize=None):
    """
    Called when the Sequential Results data tree entry is selected
    to show results from a sequential refinement.
    
    :param wx.Frame G2frame: main GSAS-II data tree windows

    :param dict data: a dictionary containing the following items:  

            * 'histNames' - list of histogram names in order as processed by Sequential Refinement
            * 'varyList' - list of variables - identical over all refinements in sequence
              note that this is the original list of variables, prior to processing
              constraints.
            * 'variableLabels' -- a dict of labels to be applied to each parameter
              (this is created as an empty dict if not present in data).
            * keyed by histName - dictionaries for all data sets processed, which contains:

              * 'variables'- result[0] from leastsq call
              * 'varyList' - list of variables passed to leastsq call (not same as above)
              * 'sig' - esds for variables
              * 'covMatrix' - covariance matrix from individual refinement
              * 'title' - histogram name; same as dict item name
              * 'newAtomDict' - new atom parameters after shifts applied
              * 'newCellDict' - refined cell parameters after shifts to A0-A5 from Dij terms applied'
    """

    def GetSampleParms():
        '''Make a dictionary of the sample parameters are not the same over the
        refinement series.
        '''
        if 'IMG' in histNames[0]:
            sampleParmDict = {'Sample load':[],}
        else:
            sampleParmDict = {'Temperature':[],'Pressure':[],'Time':[],
                              'FreePrm1':[],'FreePrm2':[],'FreePrm3':[],}
        Controls = G2frame.PatternTree.GetItemPyData(
            GetPatternTreeItemId(G2frame,G2frame.root, 'Controls'))
        sampleParm = {}
        for name in histNames:
            if 'IMG' in name:
                for item in sampleParmDict:
                    sampleParmDict[item].append(data[name]['parmDict'].get(item,0))
            else:
                Id = GetPatternTreeItemId(G2frame,G2frame.root,name)
                sampleData = G2frame.PatternTree.GetItemPyData(GetPatternTreeItemId(G2frame,Id,'Sample Parameters'))
                for item in sampleParmDict:
                    sampleParmDict[item].append(sampleData.get(item,0))
        for item in sampleParmDict:
            frstValue = sampleParmDict[item][0]
            if np.any(np.array(sampleParmDict[item])-frstValue):
                if item.startswith('FreePrm'):
                    sampleParm[Controls[item]] = sampleParmDict[item]
                else:
                    sampleParm[item] = sampleParmDict[item]
        return sampleParm

    def GetColumnInfo(col):
        '''returns column label, lists of values and errors (or None) for each column in the table
        for plotting. The column label is reformatted from Unicode to MatPlotLib encoding
        '''
        colName = G2frame.SeqTable.GetColLabelValue(col)
        plotName = variableLabels.get(colName,colName)
        plotName = plotSpCharFix(plotName)
        return plotName,colList[col],colSigs[col]
            
    def PlotSelect(event):
        'Plots a row (covariance) or column on double-click'
        cols = G2frame.dataDisplay.GetSelectedCols()
        rows = G2frame.dataDisplay.GetSelectedRows()
        if cols:
            G2plt.PlotSelectedSequence(G2frame,cols,GetColumnInfo,SelectXaxis)
        elif rows:
            name = histNames[rows[0]]       #only does 1st one selected
            G2plt.PlotCovariance(G2frame,data[name])
        else:
            G2frame.ErrorDialog(
                'Select row or columns',
                'Nothing selected in table. Click on column or row label(s) to plot. N.B. Grid selection can be a bit funky.'
                )
            
    def OnPlotSelSeq(event):
        'plot the selected columns or row from menu command'
        cols = sorted(G2frame.dataDisplay.GetSelectedCols()) # ignore selection order
        rows = G2frame.dataDisplay.GetSelectedRows()
        if cols:
            G2plt.PlotSelectedSequence(G2frame,cols,GetColumnInfo,SelectXaxis)
        elif rows:
            name = histNames[rows[0]]       #only does 1st one selected
            G2plt.PlotCovariance(G2frame,data[name])
        else:
            G2frame.ErrorDialog(
                'Select columns',
                'No columns or rows selected in table. Click on row or column labels to select fields for plotting.'
                )                
    def OnRenameSelSeq(event):
        cols = sorted(G2frame.dataDisplay.GetSelectedCols()) # ignore selection order
        colNames = [G2frame.SeqTable.GetColLabelValue(c) for c in cols]
        newNames = colNames[:]
        for i,name in enumerate(colNames):
            if name in variableLabels:
                newNames[i] = variableLabels[name]
        if not cols:
            G2frame.ErrorDialog('Select columns',
                'No columns selected in table. Click on column labels to select fields for rename.')
            return
        dlg = MultiStringDialog(G2frame.dataDisplay,'Set column names',colNames,newNames)
        if dlg.Show():
            newNames = dlg.GetValues()            
            variableLabels.update(dict(zip(colNames,newNames)))
        data['variableLabels'] = variableLabels 
        dlg.Destroy()
        UpdateSeqResults(G2frame,data,G2frame.dataDisplay.GetSize()) # redisplay variables
        G2plt.PlotSelectedSequence(G2frame,cols,GetColumnInfo,SelectXaxis)
            
    def OnReOrgSelSeq(event):
        'Reorder the columns'
        G2G.GetItemOrder(G2frame,VaryListChanges,vallookup,posdict)    
        UpdateSeqResults(G2frame,data,G2frame.dataDisplay.GetSize()) # redisplay variables

    def OnSaveSelSeqCSV(event):
        'export the selected columns to a .csv file from menu command'
        OnSaveSelSeq(event,csv=True)
        
    def OnSaveSeqCSV(event):
        'export all columns to a .csv file from menu command'
        OnSaveSelSeq(event,csv=True,allcols=True)
        
    def OnSaveSelSeq(event,csv=False,allcols=False):
        'export the selected columns to a .txt or .csv file from menu command'
        def WriteCSV():
            def WriteList(headerItems):
                line = ''
                for lbl in headerItems:
                    if line: line += ','
                    line += '"'+lbl+'"'
                return line
            head = ['name']
            for col in cols:
                item = G2frame.SeqTable.GetColLabelValue(col)
                # get rid of labels that have Unicode characters
                if not all([ord(c) < 128 and ord(c) != 0 for c in item]): item = '?'
                if col in havesig:
                    head += [item,'esd-'+item]
                else:
                    head += [item]
            SeqFile.write(WriteList(head)+'\n')
            for row,name in enumerate(saveNames):
                line = '"'+saveNames[row]+'"'
                for col in cols:
                    if col in havesig:
                        line += ','+str(saveData[col][row])+','+str(saveSigs[col][row])
                    else:
                        line += ','+str(saveData[col][row])
                SeqFile.write(line+'\n')
        def WriteSeq():
            lenName = len(saveNames[0])
            line = '  %s  '%('name'.center(lenName))
            for col in cols:
                item = G2frame.SeqTable.GetColLabelValue(col)
                if col in havesig:
                    line += ' %12s %12s '%(item.center(12),'esd'.center(12))
                else:
                    line += ' %12s '%(item.center(12))
            SeqFile.write(line+'\n')
            for row,name in enumerate(saveNames):
                line = " '%s' "%(saveNames[row])
                for col in cols:
                    if col in havesig:
                        line += ' %12.6f %12.6f '%(saveData[col][row],saveSigs[col][row])
                    else:
                        line += ' %12.6f '%saveData[col][row]
                SeqFile.write(line+'\n')

        # start of OnSaveSelSeq code
        if allcols:
            cols = range(G2frame.SeqTable.GetNumberCols())
        else:
            cols = sorted(G2frame.dataDisplay.GetSelectedCols()) # ignore selection order
        nrows = G2frame.SeqTable.GetNumberRows()
        if not cols:
            G2frame.ErrorDialog('Select columns',
                             'No columns selected in table. Click on column labels to select fields for output.')
            return
        saveNames = [G2frame.SeqTable.GetRowLabelValue(r) for r in range(nrows)]
        saveData = {}
        saveSigs = {}
        havesig = []
        for col in cols:
            name,vals,sigs = GetColumnInfo(col)
            saveData[col] = vals
            if sigs:
                havesig.append(col)
                saveSigs[col] = sigs
        if csv:
            wild = 'CSV output file (*.csv)|*.csv'
        else:
            wild = 'Text output file (*.txt)|*.txt'
        dlg = wx.FileDialog(
            G2frame,
            'Choose text output file for your selection', '.', '', 
            wild,wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.CHANGE_DIR)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                SeqTextFile = dlg.GetPath()
                SeqTextFile = G2IO.FileDlgFixExt(dlg,SeqTextFile) 
                SeqFile = open(SeqTextFile,'w')
                if csv:
                    WriteCSV()
                else:
                    WriteSeq()
                SeqFile.close()
        finally:
            dlg.Destroy()
                
    def striphist(var,insChar=''):
        'strip a histogram number from a var name'
        sv = var.split(':')
        if len(sv) <= 1: return var
        if sv[1]:
            sv[1] = insChar
        return ':'.join(sv)
        
    def plotSpCharFix(lbl):
        'Change selected unicode characters to their matplotlib equivalent'
        for u,p in [
            (u'\u03B1',r'$\alpha$'),
            (u'\u03B2',r'$\beta$'),
            (u'\u03B3',r'$\gamma$'),
            (u'\u0394\u03C7',r'$\Delta\chi$'),
            ]:
            lbl = lbl.replace(u,p)
        return lbl
    
    def SelectXaxis():
        'returns a selected column number (or None) as the X-axis selection'
        ncols = G2frame.SeqTable.GetNumberCols()
        colNames = [G2frame.SeqTable.GetColLabelValue(r) for r in range(ncols)]
        dlg = G2SingleChoiceDialog(
            G2frame.dataDisplay,
            'Select x-axis parameter for plot or Cancel for sequence number',
            'Select X-axis',
            colNames)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                col = dlg.GetSelection()
            else:
                col = None
        finally:
            dlg.Destroy()
        return col
    
    def EnablePseudoVarMenus():
        'Enables or disables the PseudoVar menu items that require existing defs'
        if Controls['SeqPseudoVars']:
            val = True
        else:
            val = False
        G2frame.dataFrame.SequentialPvars.Enable(wxDELSEQVAR,val)
        G2frame.dataFrame.SequentialPvars.Enable(wxEDITSEQVAR,val)

    def DelPseudoVar(event):
        'Ask the user to select a pseudo var expression to delete'
        choices = Controls['SeqPseudoVars'].keys()
        selected = ItemSelector(
            choices,G2frame.dataFrame,
            multiple=True,
            title='Select expressions to remove',
            header='Delete expression')
        if selected is None: return
        for item in selected:
            del Controls['SeqPseudoVars'][choices[item]]
        if selected:
            UpdateSeqResults(G2frame,data,G2frame.dataDisplay.GetSize()) # redisplay variables

    def EditPseudoVar(event):
        'Edit an existing pseudo var expression'
        choices = Controls['SeqPseudoVars'].keys()
        if len(choices) == 1:
            selected = 0
        else:
            selected = ItemSelector(
                choices,G2frame.dataFrame,
                multiple=False,
                title='Select an expression to edit',
                header='Edit expression')
        if selected is not None:
            dlg = G2exG.ExpressionDialog(
                G2frame.dataDisplay,PSvarDict,
                Controls['SeqPseudoVars'][choices[selected]],
                header="Edit the PseudoVar expression",
                VarLabel="PseudoVar #"+str(selected+1),
                fit=False)
            newobj = dlg.Show(True)
            if newobj:
                calcobj = G2obj.ExpressionCalcObj(newobj)
                del Controls['SeqPseudoVars'][choices[selected]]
                Controls['SeqPseudoVars'][calcobj.eObj.expression] = newobj
                UpdateSeqResults(G2frame,data,G2frame.dataDisplay.GetSize()) # redisplay variables
        
    def AddNewPseudoVar(event):
        'Create a new pseudo var expression'
        dlg = G2exG.ExpressionDialog(
            G2frame.dataDisplay,PSvarDict,
            header='Enter an expression for a PseudoVar here',
            VarLabel = "New PseudoVar",
            fit=False)
        obj = dlg.Show(True)
        dlg.Destroy()
        if obj:
            calcobj = G2obj.ExpressionCalcObj(obj)
            Controls['SeqPseudoVars'][calcobj.eObj.expression] = obj
            UpdateSeqResults(G2frame,data,G2frame.dataDisplay.GetSize()) # redisplay variables

    def UpdateParmDict(parmDict):
        '''generate the atom positions and the direct & reciprocal cell values,
        because they might be needed to evaluate the pseudovar
        '''
        Ddict = dict(zip(['D11','D22','D33','D12','D13','D23'],
                         ['A'+str(i) for i in range(6)])
                     )
        delList = []
        phaselist = []
        for item in parmDict: 
            if ':' not in item: continue
            key = item.split(':')
            if len(key) < 3: continue
            # remove the dA[xyz] terms, they would only bring confusion
            if key[2].startswith('dA'):
                delList.append(item)
            # compute and update the corrected reciprocal cell terms using the Dij values
            elif key[2] in Ddict:
                if key[0] not in phaselist: phaselist.append(key[0])
                akey = key[0]+'::'+Ddict[key[2]]
                parmDict[akey] -= parmDict[item]
                delList.append(item)
        for item in delList:
            del parmDict[item]                
        for i in phaselist:
            pId = int(i)
            # apply cell symmetry
            A,zeros = G2stIO.cellFill(str(pId)+'::',SGdata[pId],parmDict,zeroDict[pId])
            # convert to direct cell & add the unique terms to the dictionary
            for i,val in enumerate(G2lat.A2cell(A)):
                if i in uniqCellIndx[pId]:
                    lbl = str(pId)+'::'+cellUlbl[i]
                    parmDict[lbl] = val
            lbl = str(pId)+'::'+'vol'
            parmDict[lbl] = G2lat.calc_V(A)
        return parmDict

    def EvalPSvarDeriv(calcobj,parmDict,sampleDict,var,ESD):
        '''Evaluate an expression derivative with respect to a
        GSAS-II variable name.

        Note this likely could be faster if the loop over calcobjs were done
        inside after the Dict was created. 
        '''
        step = ESD/10
        Ddict = dict(zip(['D11','D22','D33','D12','D13','D23'],
                         ['A'+str(i) for i in range(6)])
                     )
        results = []
        phaselist = []
        VparmDict = sampleDict.copy()
        for incr in step,-step:
            VparmDict.update(parmDict.copy())           
            # as saved, the parmDict has updated 'A[xyz]' values, but 'dA[xyz]'
            # values are not zeroed: fix that!
            VparmDict.update({item:0.0 for item in parmDict if 'dA' in item})
            VparmDict[var] += incr
            G2mv.Dict2Map(VparmDict,[]) # apply constraints
            # generate the atom positions and the direct & reciprocal cell values now, because they might
            # needed to evaluate the pseudovar
            for item in VparmDict:
                if item in sampleDict:
                    continue 
                if ':' not in item: continue
                key = item.split(':')
                if len(key) < 3: continue
                # apply any new shifts to atom positions
                if key[2].startswith('dA'):
                    VparmDict[''.join(item.split('d'))] += VparmDict[item]
                    VparmDict[item] = 0.0
                # compute and update the corrected reciprocal cell terms using the Dij values
                if key[2] in Ddict:
                    if key[0] not in phaselist: phaselist.append(key[0])
                    akey = key[0]+'::'+Ddict[key[2]]
                    VparmDict[akey] -= VparmDict[item]
            for i in phaselist:
                pId = int(i)
                # apply cell symmetry
                A,zeros = G2stIO.cellFill(str(pId)+'::',SGdata[pId],VparmDict,zeroDict[pId])
                # convert to direct cell & add the unique terms to the dictionary
                for i,val in enumerate(G2lat.A2cell(A)):
                    if i in uniqCellIndx[pId]:
                        lbl = str(pId)+'::'+cellUlbl[i]
                        VparmDict[lbl] = val
                lbl = str(pId)+'::'+'vol'
                VparmDict[lbl] = G2lat.calc_V(A)
            # dict should be fully updated, use it & calculate
            calcobj.SetupCalc(VparmDict)
            results.append(calcobj.EvalExpression())
        return (results[0] - results[1]) / (2.*step)
        
    def EnableParFitEqMenus():
        'Enables or disables the Parametric Fit menu items that require existing defs'
        if Controls['SeqParFitEqList']:
            val = True
        else:
            val = False
        G2frame.dataFrame.SequentialPfit.Enable(wxDELPARFIT,val)
        G2frame.dataFrame.SequentialPfit.Enable(wxEDITPARFIT,val)
        G2frame.dataFrame.SequentialPfit.Enable(wxDOPARFIT,val)

    def ParEqEval(Values,calcObjList,varyList):
        '''Evaluate the parametric expression(s)
        :param list Values: a list of values for each variable parameter
        :param list calcObjList: a list of :class:`GSASIIobj.ExpressionCalcObj`
          expression objects to evaluate
        :param list varyList: a list of variable names for each value in Values
        '''
        result = []
        for calcobj in calcObjList:
            calcobj.UpdateVars(varyList,Values)
            result.append((calcobj.depVal-calcobj.EvalExpression())/calcobj.depSig)
        return result

    def DoParEqFit(event,eqObj=None):
        'Parametric fit minimizer'
        varyValueDict = {} # dict of variables and their initial values
        calcObjList = [] # expression objects, ready to go for each data point
        if eqObj is not None:
            eqObjList = [eqObj,]
        else:
            eqObjList = Controls['SeqParFitEqList']
        UseFlags = G2frame.SeqTable.GetColValues(0)         
        for obj in eqObjList:
            expr = obj.expression
            # assemble refined vars for this equation
            varyValueDict.update({var:val for var,val in obj.GetVariedVarVal()})
            # lookup dependent var position
            depVar = obj.GetDepVar()
            if depVar in colLabels:
                indx = colLabels.index(depVar)
            else:
                raise Exception('Dependent variable '+depVar+' not found')
            # assemble a list of the independent variables
            indepVars = obj.GetIndependentVars()
            # loop over each datapoint
            for j,row in enumerate(zip(*colList)):
                if not UseFlags[j]: continue
                # assemble equations to fit
                calcobj = G2obj.ExpressionCalcObj(obj)
                # prepare a dict of needed independent vars for this expression
                indepVarDict = {var:row[i] for i,var in enumerate(colLabels) if var in indepVars}
                calcobj.SetupCalc(indepVarDict)                
                # values and sigs for current value of dependent var
                calcobj.depVal = row[indx]
                calcobj.depSig = colSigs[indx][j]
                calcObjList.append(calcobj)
        # varied parameters
        varyList = varyValueDict.keys()
        values = varyValues = [varyValueDict[key] for key in varyList]
        if not varyList:
            print 'no variables to refine!'
            return
        try:
            result = so.leastsq(ParEqEval,varyValues,full_output=True,   #ftol=Ftol,
                                args=(calcObjList,varyList)
                                )
            values = result[0]
            covar = result[1]
            if covar is None:
                raise Exception
            esdDict = {}
            for i,avar in enumerate(varyList):
                esdDict[avar] = np.sqrt(covar[i,i])
        except:
            print('====> Fit failed')
            return
        print('==== Fit Results ====')
        for obj in eqObjList:
            obj.UpdateVariedVars(varyList,values)
            ind = '      '
            print('  '+obj.GetDepVar()+' = '+obj.expression)
            for var in obj.assgnVars:
                print(ind+var+' = '+obj.assgnVars[var])
            for var in obj.freeVars:
                avar = "::"+obj.freeVars[var][0]
                val = obj.freeVars[var][1]
                if obj.freeVars[var][2]:
                    print(ind+var+' = '+avar + " = " + G2mth.ValEsd(val,esdDict[avar]))
                else:
                    print(ind+var+' = '+avar + " =" + G2mth.ValEsd(val,0))
        # create a plot for each parametric variable
        for fitnum,obj in enumerate(eqObjList):
            calcobj = G2obj.ExpressionCalcObj(obj)
            # lookup dependent var position
            indx = colLabels.index(obj.GetDepVar())
            # assemble a list of the independent variables
            indepVars = obj.GetIndependentVars()            
            # loop over each datapoint
            fitvals = []
            for j,row in enumerate(zip(*colList)):
                calcobj.SetupCalc(
                    {var:row[i] for i,var in enumerate(colLabels) if var in indepVars}
                    )
                fitvals.append(calcobj.EvalExpression())
            G2plt.PlotSelectedSequence(
                G2frame,[indx],GetColumnInfo,SelectXaxis,
                fitnum,fitvals)

    def SingleParEqFit(eqObj):
        DoParEqFit(None,eqObj)

    def DelParFitEq(event):
        'Ask the user to select function to delete'
        txtlst = [obj.GetDepVar()+' = '+obj.expression for obj in Controls['SeqParFitEqList']]
        selected = ItemSelector(
            txtlst,G2frame.dataFrame,
            multiple=True,
            title='Select a parametric equation(s) to remove',
            header='Delete equation')
        if selected is None: return
        Controls['SeqParFitEqList'] = [obj for i,obj in enumerate(Controls['SeqParFitEqList']) if i not in selected]
        EnableParFitEqMenus()
        if Controls['SeqParFitEqList']: DoParEqFit(event)
        
    def EditParFitEq(event):
        'Edit an existing parametric equation'
        txtlst = [obj.GetDepVar()+' = '+obj.expression for obj in Controls['SeqParFitEqList']]
        if len(txtlst) == 1:
            selected = 0
        else:
            selected = ItemSelector(
                txtlst,G2frame.dataFrame,
                multiple=False,
                title='Select a parametric equation to edit',
                header='Edit equation')
        if selected is not None:
            dlg = G2exG.ExpressionDialog(
                G2frame.dataDisplay,indepVarDict,
                Controls['SeqParFitEqList'][selected],
                depVarDict=depVarDict,
                header="Edit the formula for this minimization function",
                ExtraButton=['Fit',SingleParEqFit])
            newobj = dlg.Show(True)
            if newobj:
                calcobj = G2obj.ExpressionCalcObj(newobj)
                Controls['SeqParFitEqList'][selected] = newobj
                EnableParFitEqMenus()
            if Controls['SeqParFitEqList']: DoParEqFit(event)

    def AddNewParFitEq(event):
        'Create a new parametric equation to be fit to sequential results'

        # compile the variable names used in previous freevars to avoid accidental name collisions
        usedvarlist = []
        for obj in Controls['SeqParFitEqList']:
            for var in obj.freeVars:
                if obj.freeVars[var][0] not in usedvarlist: usedvarlist.append(obj.freeVars[var][0])

        dlg = G2exG.ExpressionDialog(
            G2frame.dataDisplay,indepVarDict,
            depVarDict=depVarDict,
            header='Define an equation to minimize in the parametric fit',
            ExtraButton=['Fit',SingleParEqFit],
            usedVars=usedvarlist)
        obj = dlg.Show(True)
        dlg.Destroy()
        if obj:
            Controls['SeqParFitEqList'].append(obj)
            EnableParFitEqMenus()
            if Controls['SeqParFitEqList']: DoParEqFit(event)
                
    def CopyParFitEq(event):
        'Copy an existing parametric equation to be fit to sequential results'
        # compile the variable names used in previous freevars to avoid accidental name collisions
        usedvarlist = []
        for obj in Controls['SeqParFitEqList']:
            for var in obj.freeVars:
                if obj.freeVars[var][0] not in usedvarlist: usedvarlist.append(obj.freeVars[var][0])
        txtlst = [obj.GetDepVar()+' = '+obj.expression for obj in Controls['SeqParFitEqList']]
        if len(txtlst) == 1:
            selected = 0
        else:
            selected = ItemSelector(
                txtlst,G2frame.dataFrame,
                multiple=False,
                title='Select a parametric equation to copy',
                header='Copy equation')
        if selected is not None:
            newEqn = copy.deepcopy(Controls['SeqParFitEqList'][selected])
            for var in newEqn.freeVars:
                newEqn.freeVars[var][0] = G2obj.MakeUniqueLabel(newEqn.freeVars[var][0],usedvarlist)
            dlg = G2exG.ExpressionDialog(
                G2frame.dataDisplay,indepVarDict,
                newEqn,
                depVarDict=depVarDict,
                header="Edit the formula for this minimization function",
                ExtraButton=['Fit',SingleParEqFit])
            newobj = dlg.Show(True)
            if newobj:
                calcobj = G2obj.ExpressionCalcObj(newobj)
                Controls['SeqParFitEqList'].append(newobj)
                EnableParFitEqMenus()
            if Controls['SeqParFitEqList']: DoParEqFit(event)
                                            
    def GridSetToolTip(row,col):
        '''Routine to show standard uncertainties for each element in table
        as a tooltip
        '''
        if colSigs[col]:
            return u'\u03c3 = '+str(colSigs[col][row])
        return ''
        
    def GridColLblToolTip(col):
        '''Define a tooltip for a column. This will be the user-entered value
        (from data['variableLabels']) or the default name
        '''
        if col < 0 or col > len(colLabels):
            print 'Illegal column #',col
            return
        var = colLabels[col]
        return variableLabels.get(var,G2obj.fmtVarDescr(var))
        
    def SetLabelString(event):
        '''Define or edit the label for a column in the table, to be used
        as a tooltip and for plotting
        '''
        col = event.GetCol()
        if col < 0 or col > len(colLabels):
            return
        var = colLabels[col]
        lbl = variableLabels.get(var,G2obj.fmtVarDescr(var))
        dlg = SingleStringDialog(G2frame.dataFrame,'Set variable label',
                                 'Set a new name for variable '+var,lbl,size=(400,-1))
        if dlg.Show():
            variableLabels[var] = dlg.GetValue()
        dlg.Destroy()
        
    #def GridRowLblToolTip(row): return 'Row ='+str(row)
    
    # lookup table for unique cell parameters by symmetry
    cellGUIlist = [
        [['m3','m3m'],(0,)],
        [['3R','3mR'],(0,3)],
        [['3','3m1','31m','6/m','6/mmm','4/m','4/mmm'],(0,2)],
        [['mmm'],(0,1,2)],
        [['2/m'+'a'],(0,1,2,3)],
        [['2/m'+'b'],(0,1,2,4)],
        [['2/m'+'c'],(0,1,2,5)],
        [['-1'],(0,1,2,3,4,5)],
        ]
    # cell labels
    cellUlbl = ('a','b','c',u'\u03B1',u'\u03B2',u'\u03B3') # unicode a,b,c,alpha,beta,gamma

    #======================================================================
    # start processing sequential results here (UpdateSeqResults)
    #======================================================================
    if not data:
        print 'No sequential refinement results'
        return
    variableLabels = data.get('variableLabels',{})
    data['variableLabels'] = variableLabels
    Histograms,Phases = G2frame.GetUsedHistogramsAndPhasesfromTree()
    Controls = G2frame.PatternTree.GetItemPyData(GetPatternTreeItemId(G2frame,G2frame.root,'Controls'))
    # create a place to store Pseudo Vars & Parametric Fit functions, if not present
    if 'SeqPseudoVars' not in Controls: Controls['SeqPseudoVars'] = {}
    if 'SeqParFitEqList' not in Controls: Controls['SeqParFitEqList'] = []
    histNames = data['histNames']
    if G2frame.dataDisplay:
        G2frame.dataDisplay.Destroy()
    if not G2frame.dataFrame.GetStatusBar():
        Status = G2frame.dataFrame.CreateStatusBar()
        Status.SetStatusText("Select column to export; Double click on column to plot data; on row for Covariance")
    sampleParms = GetSampleParms()

    # make dict of varied atom coords keyed by absolute position
    newAtomDict = data[histNames[0]].get('newAtomDict',{}) # dict with atom positions; relative & absolute
    # Possible error: the next might need to be data[histNames[0]]['varyList']
    # error will arise if there constraints on coordinates?
    atomLookup = {newAtomDict[item][0]:item for item in newAtomDict if item in data['varyList']}
    
    # make dict of varied cell parameters equivalents
    ESDlookup = {} # provides the Dij term for each Ak term (where terms are refined)
    Dlookup = {} # provides the Ak term for each Dij term (where terms are refined)
    # N.B. These Dij vars are missing a histogram #
    newCellDict = data[histNames[0]].get('newCellDict',{})
    for item in newCellDict:
        if item in data['varyList']:
            ESDlookup[newCellDict[item][0]] = item
            Dlookup[item] = newCellDict[item][0]
    # add coordinate equivalents to lookup table
    for parm in atomLookup:
        Dlookup[atomLookup[parm]] = parm
        ESDlookup[parm] = atomLookup[parm]

    # get unit cell & symmetry for all phases & initial stuff for later use
    RecpCellTerms = {}
    SGdata = {}
    uniqCellIndx = {}
    initialCell = {}
    RcellLbls = {}
    zeroDict = {}
    Rcelldict = {}
    for phase in Phases:
        phasedict = Phases[phase]
        pId = phasedict['pId']
        pfx = str(pId)+'::' # prefix for A values from phase
        RcellLbls[pId] = [pfx+'A'+str(i) for i in range(6)]
        RecpCellTerms[pId] = G2lat.cell2A(phasedict['General']['Cell'][1:7])
        zeroDict[pId] = dict(zip(RcellLbls[pId],6*[0.,]))
        SGdata[pId] = phasedict['General']['SGData']
        Rcelldict.update({lbl:val for lbl,val in zip(RcellLbls[pId],RecpCellTerms[pId])})
        laue = SGdata[pId]['SGLaue']
        if laue == '2/m':
            laue += SGdata[pId]['SGUniq']
        for symlist,celllist in cellGUIlist:
            if laue in symlist:
                uniqCellIndx[pId] = celllist
                break
        else: # should not happen
            uniqCellIndx[pId] = range(6)
        for i in uniqCellIndx[pId]:
            initialCell[str(pId)+'::A'+str(i)] =  RecpCellTerms[pId][i]

    SetDataMenuBar(G2frame,G2frame.dataFrame.SequentialMenu)
    G2frame.dataFrame.SetLabel('Sequential refinement results')
    if not G2frame.dataFrame.GetStatusBar():
        Status = G2frame.dataFrame.CreateStatusBar()
        Status.SetStatusText('')
    G2frame.dataFrame.Bind(wx.EVT_MENU, OnRenameSelSeq, id=wxID_RENAMESEQSEL)
    G2frame.dataFrame.Bind(wx.EVT_MENU, OnSaveSelSeq, id=wxID_SAVESEQSEL)
    G2frame.dataFrame.Bind(wx.EVT_MENU, OnSaveSelSeqCSV, id=wxID_SAVESEQSELCSV)
    G2frame.dataFrame.Bind(wx.EVT_MENU, OnSaveSeqCSV, id=wxID_SAVESEQCSV)
    G2frame.dataFrame.Bind(wx.EVT_MENU, OnPlotSelSeq, id=wxID_PLOTSEQSEL)
    G2frame.dataFrame.Bind(wx.EVT_MENU, OnReOrgSelSeq, id=wxID_ORGSEQSEL)
    G2frame.dataFrame.Bind(wx.EVT_MENU, AddNewPseudoVar, id=wxADDSEQVAR)
    G2frame.dataFrame.Bind(wx.EVT_MENU, DelPseudoVar, id=wxDELSEQVAR)
    G2frame.dataFrame.Bind(wx.EVT_MENU, EditPseudoVar, id=wxEDITSEQVAR)
    G2frame.dataFrame.Bind(wx.EVT_MENU, AddNewParFitEq, id=wxADDPARFIT)
    G2frame.dataFrame.Bind(wx.EVT_MENU, CopyParFitEq, id=wxCOPYPARFIT)
    G2frame.dataFrame.Bind(wx.EVT_MENU, DelParFitEq, id=wxDELPARFIT)
    G2frame.dataFrame.Bind(wx.EVT_MENU, EditParFitEq, id=wxEDITPARFIT)
    G2frame.dataFrame.Bind(wx.EVT_MENU, DoParEqFit, id=wxDOPARFIT)
    EnablePseudoVarMenus()
    EnableParFitEqMenus()

    # scan for locations where the variables change
    VaryListChanges = [] # histograms where there is a change
    combinedVaryList = []
    firstValueDict = {}
    vallookup = {}
    posdict = {}
    prevVaryList = []
    for i,name in enumerate(histNames):
        for var,val,sig in zip(data[name]['varyList'],data[name]['variables'],data[name]['sig']):
            svar = striphist(var,'*') # wild-carded
            if svar not in combinedVaryList:
                # add variables to list as they appear
                combinedVaryList.append(svar)
                firstValueDict[svar] = (val,sig)
        if prevVaryList != data[name]['varyList']: # this refinement has a different refinement list from previous
            prevVaryList = data[name]['varyList']
            vallookup[name] = dict(zip(data[name]['varyList'],data[name]['variables']))
            posdict[name] = {}
            for var in data[name]['varyList']:
                svar = striphist(var,'*')
                posdict[name][combinedVaryList.index(svar)] = svar
            VaryListChanges.append(name)
    if len(VaryListChanges) > 1:
        G2frame.dataFrame.SequentialFile.Enable(wxID_ORGSEQSEL,True)
    else:
        G2frame.dataFrame.SequentialFile.Enable(wxID_ORGSEQSEL,False)
    #-----------------------------------------------------------------------------------
    # build up the data table by columns -----------------------------------------------
    nRows = len(histNames)
    colList = [nRows*[True]]
    colSigs = [None]
    colLabels = ['Use']
    Types = [wg.GRID_VALUE_BOOL]
    # start with Rwp values
    if 'IMG ' not in histNames[0][:4]:
        colList += [[data[name]['Rvals']['Rwp'] for name in histNames]]
        colSigs += [None]
        colLabels += ['Rwp']
        Types += [wg.GRID_VALUE_FLOAT+':10,3',]
    # add % change in Chi^2 in last cycle
    if histNames[0][:4] not in ['SASD','IMG '] and Controls.get('ShowCell'):
        colList += [[100.*data[name]['Rvals'].get('DelChi2',-1) for name in histNames]]
        colSigs += [None]
        colLabels += [u'\u0394\u03C7\u00B2 (%)']
        Types += [wg.GRID_VALUE_FLOAT,]
    deltaChiCol = len(colLabels)-1
    # add changing sample parameters to table
    for key in sampleParms:
        colList += [sampleParms[key]]
        colSigs += [None]
        colLabels += [key]
        Types += [wg.GRID_VALUE_FLOAT,]
    sampleDict = {}
    for i,name in enumerate(histNames):
        sampleDict[name] = dict(zip(sampleParms.keys(),[sampleParms[key][i] for key in sampleParms.keys()])) 
    # add unique cell parameters TODO: review this where the cell symmetry changes (when possible)
    if Controls.get('ShowCell',False):
        for pId in sorted(RecpCellTerms):
            pfx = str(pId)+'::' # prefix for A values from phase
            cells = []
            cellESDs = []
            colLabels += [pfx+cellUlbl[i] for i in uniqCellIndx[pId]]
            colLabels += [pfx+'Vol']
            Types += (1+len(uniqCellIndx[pId]))*[wg.GRID_VALUE_FLOAT,]
            for name in histNames:
                covData = {
                    'varyList': [Dlookup.get(striphist(v),v) for v in data[name]['varyList']],
                    'covMatrix': data[name]['covMatrix']
                    }
                A = RecpCellTerms[pId][:] # make copy of starting A values
                # update with refined values
                for i in range(6):
                    var = str(pId)+'::A'+str(i)
                    if var in ESDlookup:
                        val = data[name]['newCellDict'][ESDlookup[var]][1] # get refined value 
                        A[i] = val # override with updated value
                # apply symmetry
                Albls = [pfx+'A'+str(i) for i in range(6)]
                cellDict = dict(zip(Albls,A))
                A,zeros = G2stIO.cellFill(pfx,SGdata[pId],cellDict,zeroDict[pId])
                # convert to direct cell & add only unique values to table
                c = G2lat.A2cell(A)
                vol = G2lat.calc_V(A)
                cE = G2stIO.getCellEsd(pfx,SGdata[pId],A,covData)
                cells += [[c[i] for i in uniqCellIndx[pId]]+[vol]]
                cellESDs += [[cE[i] for i in uniqCellIndx[pId]]+[cE[-1]]]
            colList += zip(*cells)
            colSigs += zip(*cellESDs)
    # sort out the variables in their selected order
    varcols = 0
    for d in posdict.itervalues():
        varcols = max(varcols,max(d.keys())+1)
    # get labels for each column
    for i in range(varcols):
        lbl = ''
        for h in VaryListChanges:
            if posdict[h].get(i):
                if posdict[h].get(i) in lbl: continue
                if lbl != "": lbl += '/'
                lbl += posdict[h].get(i)
        colLabels.append(lbl)
    Types += varcols*[wg.GRID_VALUE_FLOAT]
    vals = []
    esds = []
    varsellist = None        # will be a list of variable names in the order they are selected to appear
    # tabulate values for each hist, leaving None for blank columns
    for name in histNames:
        if name in posdict:
            varsellist = [posdict[name].get(i) for i in range(varcols)]
            # translate variable names to how they will be used in the headings
            vs = [striphist(v,'*') for v in data[name]['varyList']]
            # determine the index for each column (or None) in the data[]['variables'] and ['sig'] lists
            sellist = [vs.index(v) if v is not None else None for v in varsellist]
            #sellist = [i if striphist(v,'*') in varsellist else None for i,v in enumerate(data[name]['varyList'])]
        if not varsellist: raise Exception()
        vals.append([data[name]['variables'][s] if s is not None else None for s in sellist])
        esds.append([data[name]['sig'][s] if s is not None else None for s in sellist])
        #GSASIIpath.IPyBreak()
    colList += zip(*vals)
    colSigs += zip(*esds)
                
    # tabulate constrained variables, removing histogram numbers if needed
    # from parameter label
    depValDict = {}
    depSigDict = {}
    for name in histNames:
        for var in data[name].get('depParmDict',{}):
            val,sig = data[name]['depParmDict'][var]
            svar = striphist(var,'*')
            if svar not in depValDict:
               depValDict[svar] = [val]
               depSigDict[svar] = [sig]
            else:
               depValDict[svar].append(val)
               depSigDict[svar].append(sig)
    # add the dependent constrained variables to the table
    for var in sorted(depValDict):
        if len(depValDict[var]) != len(histNames): continue
        colLabels.append(var)
        Types += [wg.GRID_VALUE_FLOAT,]
        colSigs += [depSigDict[var]]
        colList += [depValDict[var]]

    # add atom parameters to table
    colLabels += atomLookup.keys()
    Types += len(atomLookup)*[wg.GRID_VALUE_FLOAT]
    for parm in sorted(atomLookup):
        colList += [[data[name]['newAtomDict'][atomLookup[parm]][1] for name in histNames]]
        if atomLookup[parm] in data[histNames[0]]['varyList']:
            col = data[histNames[0]]['varyList'].index(atomLookup[parm])
            colSigs += [[data[name]['sig'][col] for name in histNames]]
        else:
            colSigs += [None] # should not happen
    # evaluate Pseudovars, their ESDs and add them to grid
    for expr in Controls['SeqPseudoVars']:
        obj = Controls['SeqPseudoVars'][expr]
        calcobj = G2obj.ExpressionCalcObj(obj)
        valList = []
        esdList = []
        for seqnum,name in enumerate(histNames):
            sigs = data[name]['sig']
            G2mv.InitVars()
            parmDict = data[name].get('parmDict')
            badVary = data[name].get('badVary',[])
            constraintInfo = data[name].get('constraintInfo',[[],[],{},[],seqnum])
            groups,parmlist,constrDict,fixedList,ihst = constraintInfo
            varyList = data[name]['varyList']
            parmDict = data[name]['parmDict']
            G2mv.GenerateConstraints(groups,parmlist,varyList,constrDict,fixedList,parmDict,SeqHist=ihst)
            derivs = np.array(
                [EvalPSvarDeriv(calcobj,parmDict.copy(),sampleDict[name],var,ESD)
                 for var,ESD in zip(varyList,sigs)]
                )
            esdList.append(np.sqrt(
                np.inner(derivs,np.inner(data[name]['covMatrix'],derivs.T))
                ))
            PSvarDict = parmDict.copy()
            PSvarDict.update(sampleDict[name])
            UpdateParmDict(PSvarDict)
            calcobj.UpdateDict(PSvarDict)
            valList.append(calcobj.EvalExpression())
        if not esdList:
            esdList = None
        colList += [valList]
        colSigs += [esdList]
        colLabels += [expr]
        Types += [wg.GRID_VALUE_FLOAT,]
    #---- table build done -------------------------------------------------------------

    # Make dict needed for creating & editing pseudovars (PSvarDict).
    name = histNames[0]
    parmDict = data[name].get('parmDict')
    PSvarDict = parmDict.copy()
    PSvarDict.update(sampleParms)
    UpdateParmDict(PSvarDict)
    # Also dicts of dependent (depVarDict) & independent vars (indepVarDict)
    # for Parametric fitting from the data table
    parmDict = dict(zip(colLabels,zip(*colList)[0])) # scratch dict w/all values in table
    parmDict.update(
        {var:val for var,val in data[name].get('newCellDict',{}).values()} #  add varied reciprocal cell terms
    )
    name = histNames[0]

    #******************************************************************************
    # create a set of values for example evaluation of pseudovars and 
    # this does not work for refinements that have differing numbers of variables.
    #raise Exception
    indepVarDict = {}     #  values in table w/o ESDs
    depVarDict = {}
    for i,var in enumerate(colLabels):
        if var == 'Use': continue
        if colList[i][0] is None:
            val,sig = firstValueDict.get(var,[None,None])
        elif colSigs[i]:
            val,sig = colList[i][0],colSigs[i][0]
        else:
            val,sig = colList[i][0],None
        if val is None:
            continue
        elif sig is None:
            indepVarDict[var] = val
        elif striphist(var) not in Dlookup:
            depVarDict[var] = val
    # add recip cell coeff. values
    depVarDict.update({var:val for var,val in data[name].get('newCellDict',{}).values()})

    G2frame.dataDisplay = GSGrid(parent=G2frame.dataFrame)
    G2frame.SeqTable = Table(
        [list(c) for c in zip(*colList)],     # convert from columns to rows
        colLabels=colLabels,rowLabels=histNames,types=Types)
    G2frame.dataDisplay.SetTable(G2frame.SeqTable, True)
    #G2frame.dataDisplay.EnableEditing(False)
    # make all but first column read-only
    for c in range(1,len(colLabels)):
        for r in range(nRows):
            G2frame.dataDisplay.SetCellReadOnly(r,c)
    G2frame.dataDisplay.Bind(wg.EVT_GRID_LABEL_LEFT_DCLICK, PlotSelect)
    G2frame.dataDisplay.Bind(wg.EVT_GRID_LABEL_RIGHT_CLICK, SetLabelString)
    G2frame.dataDisplay.SetRowLabelSize(8*len(histNames[0]))       #pretty arbitrary 8
    G2frame.dataDisplay.SetMargins(0,0)
    G2frame.dataDisplay.AutoSizeColumns(True)
    if prevSize:
        G2frame.dataDisplay.SetSize(prevSize)
    else:
        G2frame.dataFrame.setSizePosLeft([700,350])
    # highlight unconverged shifts 
    if histNames[0][:4] not in ['SASD','IMG ']:
        for row,name in enumerate(histNames):
            deltaChi = G2frame.SeqTable.GetValue(row,deltaChiCol)
            if deltaChi > 10.:
                G2frame.dataDisplay.SetCellStyle(row,deltaChiCol,color=wx.Colour(255,0,0))
            elif deltaChi > 1.0:
                G2frame.dataDisplay.SetCellStyle(row,deltaChiCol,color=wx.Colour(255,255,0))
    G2frame.dataDisplay.InstallGridToolTip(GridSetToolTip,GridColLblToolTip)
    G2frame.dataDisplay.SendSizeEvent() # resize needed on mac
    G2frame.dataDisplay.Refresh() # shows colored text on mac
    
################################################################################
#####  Main PWDR panel
################################################################################           
       
def UpdatePWHKPlot(G2frame,kind,item):
    '''Called when the histogram main tree entry is called. Displays the
    histogram weight factor, refinement statistics for the histogram
    and the range of data for a simulation.

    Also invokes a plot of the histogram.
    '''
    def onEditSimRange(event):
        'Edit simulation range'
        inp = [
            min(data[1][0]),
            max(data[1][0]),
            None
            ]
        inp[2] = (inp[1] - inp[0])/(len(data[1][0])-1.)
        names = ('start angle', 'end angle', 'step size')
        dictlst = [inp] * len(inp)
        elemlst = range(len(inp))
        dlg = G2G.ScrolledMultiEditor(
            G2frame,[inp] * len(inp), range(len(inp)), names,
            header='Edit simulation range',
            minvals=(0.001,0.001,0.0001),
            maxvals=(180.,180.,.1),
            )
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        dlg.Destroy()
        if val != wx.ID_OK: return
        if inp[0] > inp[1]:
            end,start,step = inp
        else:                
            start,end,step = inp
        step = abs(step)
        N = int((end-start)/step)+1
        newdata = np.linspace(start,end,N,True)
        if len(newdata) < 2: return # too small a range - reject
        data[1] = [newdata,np.zeros_like(newdata),np.ones_like(newdata),
            np.zeros_like(newdata),np.zeros_like(newdata),np.zeros_like(newdata)]
        Tmin = newdata[0]
        Tmax = newdata[-1]
        G2frame.PatternTree.SetItemPyData(GetPatternTreeItemId(G2frame,item,'Limits'),
            [(Tmin,Tmax),[Tmin,Tmax]])
        UpdatePWHKPlot(G2frame,kind,item) # redisplay data screen

    def OnPlot3DHKL(event):
        refList = data[1]['RefList']
        FoMax = np.max(refList.T[8+Super])
        Hmin = np.array([int(np.min(refList.T[0])),int(np.min(refList.T[1])),int(np.min(refList.T[2]))])
        Hmax = np.array([int(np.max(refList.T[0])),int(np.max(refList.T[1])),int(np.max(refList.T[2]))])
        Vpoint = [int(np.mean(refList.T[0])),int(np.mean(refList.T[1])),int(np.mean(refList.T[2]))]
        controls = {'Type' : 'Fosq','Iscale' : False,'HKLmax' : Hmax,'HKLmin' : Hmin,
            'FoMax' : FoMax,'Scale' : 1.0,'Drawing':{'viewPoint':[Vpoint,[]],'default':Vpoint[:],
            'backColor':[0,0,0],'depthFog':False,'Zclip':10.0,'cameraPos':10.,'Zstep':0.05,
            'Scale':1.0,'oldxy':[],'viewDir':[1,0,0]},'Super':Super,'SuperVec':SuperVec}
        G2plt.Plot3DSngl(G2frame,newPlot=True,Data=controls,hklRef=refList,Title=phaseName)
        
    def OnErrorAnalysis(event):
        G2plt.PlotDeltSig(G2frame,kind)
        
    def OnWtFactor(event):
        try:
            val = float(wtval.GetValue())
        except ValueError:
            val = data[0]['wtFactor']
        data[0]['wtFactor'] = val
        wtval.SetValue('%.3f'%(val))
        
    def onCopyPlotCtrls(event):
        '''Respond to menu item to copy multiple sections from a histogram.
        Need this here to pass on the G2frame object. 
        '''
        G2pdG.CopyPlotCtrls(G2frame)

    def onCopySelectedItems(event):
        '''Respond to menu item to copy multiple sections from a histogram.
        Need this here to pass on the G2frame object. 
        '''
        G2pdG.CopySelectedHistItems(G2frame)
           
    data = G2frame.PatternTree.GetItemPyData(item)
#patches
    if 'wtFactor' not in data[0]:
        data[0] = {'wtFactor':1.0}
    #if isinstance(data[1],list) and kind == 'HKLF':
    if 'list' in str(type(data[1])) and kind == 'HKLF':
        RefData = {'RefList':[],'FF':[]}
        for ref in data[1]:
            RefData['RefList'].append(ref[:11]+[ref[13],])
            RefData['FF'].append(ref[14])
        data[1] = RefData
        G2frame.PatternTree.SetItemPyData(item,data)
#end patches
    if G2frame.dataDisplay:
        G2frame.dataDisplay.Destroy()
    if kind in ['PWDR','SASD']:
        SetDataMenuBar(G2frame,G2frame.dataFrame.PWDRMenu)
        G2frame.dataFrame.Bind(wx.EVT_MENU, OnErrorAnalysis, id=wxID_PWDANALYSIS)
        G2frame.dataFrame.Bind(wx.EVT_MENU, onCopySelectedItems, id=wxID_PWDCOPY)
        G2frame.dataFrame.Bind(wx.EVT_MENU, onCopyPlotCtrls, id=wxID_PLOTCTRLCOPY)
    elif kind in ['HKLF',]:
        SetDataMenuBar(G2frame,G2frame.dataFrame.HKLFMenu)
#        G2frame.dataFrame.Bind(wx.EVT_MENU, OnErrorAnalysis, id=wxID_PWDANALYSIS)
        G2frame.dataFrame.Bind(wx.EVT_MENU, OnPlot3DHKL, id=wxID_PWD3DHKLPLOT)
#        G2frame.dataFrame.Bind(wx.EVT_MENU, onCopySelectedItems, id=wxID_PWDCOPY)
    G2frame.dataDisplay = wx.Panel(G2frame.dataFrame)
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add((5,5),)
    wtSizer = wx.BoxSizer(wx.HORIZONTAL)
    wtSizer.Add(wx.StaticText(G2frame.dataDisplay,-1,' Weight factor: '),0,WACV)
    wtval = wx.TextCtrl(G2frame.dataDisplay,-1,'%.3f'%(data[0]['wtFactor']),style=wx.TE_PROCESS_ENTER)
    wtval.Bind(wx.EVT_TEXT_ENTER,OnWtFactor)
    wtval.Bind(wx.EVT_KILL_FOCUS,OnWtFactor)
    wtSizer.Add(wtval,0,WACV)
    mainSizer.Add(wtSizer)
    if data[0].get('Dummy'):
        simSizer = wx.BoxSizer(wx.HORIZONTAL)
        Tmin = min(data[1][0])
        Tmax = max(data[1][0])
        num = len(data[1][0])
        step = (Tmax - Tmin)/(num-1)
        t = u'2\u03b8' # 2theta
        lbl =  u'Simulation range: {:.2f} to {:.2f} {:s}\nwith {:.4f} steps ({:d} points)'
        lbl += u'\n(Edit range resets observed intensities).'
        lbl = lbl.format(Tmin,Tmax,t,step,num)
        simSizer.Add(wx.StaticText(G2frame.dataDisplay,wx.ID_ANY,lbl),
                    0,WACV)
        but = wx.Button(G2frame.dataDisplay,wx.ID_ANY,"Edit range")
        but.Bind(wx.EVT_BUTTON,onEditSimRange)
        simSizer.Add(but,0,WACV)
        mainSizer.Add(simSizer)
    if 'Nobs' in data[0]:
        mainSizer.Add(wx.StaticText(G2frame.dataDisplay,-1,
            ' Data residual wR: %.3f%% on %d observations'%(data[0]['wR'],data[0]['Nobs'])))
        for value in data[0]:
            if 'Nref' in value:
                mainSizer.Add((5,5),)
                pfx = value.split('Nref')[0]
                name = data[0].get(pfx.split(':')[0]+'::Name','?')
                mainSizer.Add(wx.StaticText(G2frame.dataDisplay,-1,' For phase '+name+':'))
                mainSizer.Add(wx.StaticText(G2frame.dataDisplay,-1,
                    u' Unweighted phase residuals RF\u00b2: %.3f%%, RF: %.3f%% on %d reflections  '% \
                    (data[0][pfx+'Rf^2'],data[0][pfx+'Rf'],data[0][value])))
    mainSizer.Add((5,5),)
    mainSizer.Layout()    
    G2frame.dataDisplay.SetSizer(mainSizer)
    Size = mainSizer.Fit(G2frame.dataFrame)
    Size[1] += 10
    G2frame.dataFrame.setSizePosLeft(Size)
    G2frame.PatternTree.SetItemPyData(item,data)
    if kind in ['PWDR','SASD']:
        G2plt.PlotPatterns(G2frame,plotType=kind,newPlot=True)
    elif kind == 'HKLF':
        Name = G2frame.PatternTree.GetItemText(item)
        phaseName = G2pdG.IsHistogramInAnyPhase(G2frame,Name)
        if phaseName:
            pId = GetPatternTreeItemId(G2frame,G2frame.root,'Phases')
            phaseId =  GetPatternTreeItemId(G2frame,pId,phaseName)
            General = G2frame.PatternTree.GetItemPyData(phaseId)['General']
            Super = General.get('Super',0)
            SuperVec = General.get('SuperVec',[])
        else:
            Super = 0
            SuperVec = []       
        refList = data[1]['RefList']
        FoMax = np.max(refList.T[5+data[1].get('Super',0)])
        page = G2frame.G2plotNB.nb.GetSelection()
        tab = ''
        if page >= 0:
            tab = G2frame.G2plotNB.nb.GetPageText(page)
        if '3D' in tab:
            Hmin = np.array([int(np.min(refList.T[0])),int(np.min(refList.T[1])),int(np.min(refList.T[2]))])
            Hmax = np.array([int(np.max(refList.T[0])),int(np.max(refList.T[1])),int(np.max(refList.T[2]))])
            Vpoint = [int(np.mean(refList.T[0])),int(np.mean(refList.T[1])),int(np.mean(refList.T[2]))]
            Page = G2frame.G2plotNB.nb.GetPage(page)
            controls = Page.controls
            G2plt.Plot3DSngl(G2frame,newPlot=False,Data=controls,hklRef=refList,Title=phaseName)
        else:
            controls = {'Type' : 'Fo','ifFc' : True,     
                'HKLmax' : [int(np.max(refList.T[0])),int(np.max(refList.T[1])),int(np.max(refList.T[2]))],
                'HKLmin' : [int(np.min(refList.T[0])),int(np.min(refList.T[1])),int(np.min(refList.T[2]))],
                'FoMax' : FoMax,'Zone' : '001','Layer' : 0,'Scale' : 1.0,'Super':Super,'SuperVec':SuperVec}
            G2plt.PlotSngl(G2frame,newPlot=True,Data=controls,hklRef=refList)
                 
################################################################################
#####  Pattern tree routines
################################################################################           
       
def GetPatternTreeDataNames(G2frame,dataTypes):
    '''Needs a doc string
    '''
    names = []
    item, cookie = G2frame.PatternTree.GetFirstChild(G2frame.root)        
    while item:
        name = G2frame.PatternTree.GetItemText(item)
        if name[:4] in dataTypes:
            names.append(name)
        item, cookie = G2frame.PatternTree.GetNextChild(G2frame.root, cookie)
    return names
                          
def GetPatternTreeItemId(G2frame, parentId, itemText):
    '''Needs a doc string
    '''
    item, cookie = G2frame.PatternTree.GetFirstChild(parentId)
    while item:
        if G2frame.PatternTree.GetItemText(item) == itemText:
            return item
        item, cookie = G2frame.PatternTree.GetNextChild(parentId, cookie)
    return 0                

def MovePatternTreeToGrid(G2frame,item):
    '''Called from GSASII.OnPatternTreeSelChanged when a item is selected on the tree 
    '''
    
#    print G2frame.PatternTree.GetItemText(item)
    
    oldPage = None # will be set later if already on a Phase item
    if G2frame.dataFrame:
        SetDataMenuBar(G2frame)
        if G2frame.dataFrame.GetLabel() == 'Comments':
            try:
                data = [G2frame.dataDisplay.GetValue()]
                G2frame.dataDisplay.Clear() 
                Id = GetPatternTreeItemId(G2frame,G2frame.root, 'Comments')
                if Id: G2frame.PatternTree.SetItemPyData(Id,data)
            except:     #clumsy but avoids dead window problem when opening another project
                pass
        elif G2frame.dataFrame.GetLabel() == 'Notebook':
            try:
                data = [G2frame.dataDisplay.GetValue()]
                G2frame.dataDisplay.Clear() 
                Id = GetPatternTreeItemId(G2frame,G2frame.root, 'Notebook')
                if Id: G2frame.PatternTree.SetItemPyData(Id,data)
            except:     #clumsy but avoids dead window problem when opening another project
                pass
        elif 'Phase Data for' in G2frame.dataFrame.GetLabel():
            if G2frame.dataDisplay: 
                oldPage = G2frame.dataDisplay.GetSelection()
        G2frame.dataFrame.Clear()
        G2frame.dataFrame.SetLabel('')
    else:
        #create the frame for the data item window
        G2frame.dataFrame = DataFrame(parent=G2frame.mainPanel,frame=G2frame)
        G2frame.dataFrame.PhaseUserSize = None
        
    G2frame.dataFrame.Raise()            
    G2frame.PickId = 0
    parentID = G2frame.root
    #for i in G2frame.ExportPattern: i.Enable(False)
    defWid = [250,150]
    if item != G2frame.root:
        parentID = G2frame.PatternTree.GetItemParent(item)
    if G2frame.PatternTree.GetItemParent(item) == G2frame.root:
        G2frame.PatternId = item
        G2frame.PickId = item
        if G2frame.PatternTree.GetItemText(item) == 'Notebook':
            SetDataMenuBar(G2frame,G2frame.dataFrame.DataNotebookMenu)
            G2frame.PatternId = 0
            #for i in G2frame.ExportPattern: i.Enable(False)
            data = G2frame.PatternTree.GetItemPyData(item)
            UpdateNotebook(G2frame,data)
        elif G2frame.PatternTree.GetItemText(item) == 'Controls':
            G2frame.PatternId = 0
            #for i in G2frame.ExportPattern: i.Enable(False)
            data = G2frame.PatternTree.GetItemPyData(item)
            if not data:           #fill in defaults
                data = copy.copy(G2obj.DefaultControls)    #least squares controls
                G2frame.PatternTree.SetItemPyData(item,data)                             
            for i in G2frame.Refine: i.Enable(True)
            G2frame.EnableSeqRefineMenu()
            UpdateControls(G2frame,data)
        elif G2frame.PatternTree.GetItemText(item) == 'Sequential results':
            data = G2frame.PatternTree.GetItemPyData(item)
            UpdateSeqResults(G2frame,data)
        elif G2frame.PatternTree.GetItemText(item) == 'Covariance':
            data = G2frame.PatternTree.GetItemPyData(item)
            G2frame.dataFrame.setSizePosLeft(defWid)
            text = ''
            if 'Rvals' in data:
                Nvars = len(data['varyList'])
                Rvals = data['Rvals']
                text = '\nFinal residuals: \nwR = %.3f%% \nchi**2 = %.1f \nGOF = %.2f'%(Rvals['Rwp'],Rvals['chisq'],Rvals['GOF'])
                text += '\nNobs = %d \nNvals = %d'%(Rvals['Nobs'],Nvars)
                if 'lamMax' in Rvals:
                    text += '\nlog10 MaxLambda = %.1f'%(np.log10(Rvals['lamMax']))
            wx.TextCtrl(parent=G2frame.dataFrame,size=G2frame.dataFrame.GetClientSize(),
                value='See plot window for covariance display'+text,style=wx.TE_MULTILINE)
            G2plt.PlotCovariance(G2frame,data)
        elif G2frame.PatternTree.GetItemText(item) == 'Constraints':
            data = G2frame.PatternTree.GetItemPyData(item)
            G2cnstG.UpdateConstraints(G2frame,data)
        elif G2frame.PatternTree.GetItemText(item) == 'Rigid bodies':
            data = G2frame.PatternTree.GetItemPyData(item)
            G2cnstG.UpdateRigidBodies(G2frame,data)
        elif G2frame.PatternTree.GetItemText(item) == 'Restraints':
            data = G2frame.PatternTree.GetItemPyData(item)
            Phases = G2frame.GetPhaseData()
            phase = ''
            phaseName = ''
            if Phases:
                phaseName = Phases.keys()[0]
            G2frame.dataFrame.setSizePosLeft(defWid)
            G2restG.UpdateRestraints(G2frame,data,Phases,phaseName)
        elif 'IMG' in G2frame.PatternTree.GetItemText(item):
            G2frame.Image = item
            G2frame.dataFrame.SetTitle('Image Data')
            data = G2frame.PatternTree.GetItemPyData(GetPatternTreeItemId( \
                G2frame,item,'Image Controls'))
            G2imG.UpdateImageData(G2frame,data)
            G2plt.PlotImage(G2frame,newPlot=True)
        elif 'PKS' in G2frame.PatternTree.GetItemText(item):
            G2plt.PlotPowderLines(G2frame)
        elif 'PWDR' in G2frame.PatternTree.GetItemText(item):
            #for i in G2frame.ExportPattern: i.Enable(True)
            if G2frame.EnablePlot:
                UpdatePWHKPlot(G2frame,'PWDR',item)
        elif 'SASD' in G2frame.PatternTree.GetItemText(item):
            #for i in G2frame.ExportPattern: i.Enable(True)
            if G2frame.EnablePlot:
                UpdatePWHKPlot(G2frame,'SASD',item)
        elif 'HKLF' in G2frame.PatternTree.GetItemText(item):
            G2frame.Sngl = True
            UpdatePWHKPlot(G2frame,'HKLF',item)
        elif 'PDF' in G2frame.PatternTree.GetItemText(item):
            G2frame.PatternId = item
            for i in G2frame.ExportPDF: i.Enable(True)
            G2plt.PlotISFG(G2frame,type='S(Q)')
        elif G2frame.PatternTree.GetItemText(item) == 'Phases':
            G2frame.dataFrame.setSizePosLeft(defWid)
            wx.TextCtrl(parent=G2frame.dataFrame,size=G2frame.dataFrame.GetClientSize(),
                value='Select one phase to see its parameters')            
    elif 'I(Q)' in G2frame.PatternTree.GetItemText(item):
        G2frame.PickId = item
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        data = G2frame.PatternTree.GetItemPyData(GetPatternTreeItemId(G2frame,G2frame.PatternId,'PDF Controls'))
        G2pdG.UpdatePDFGrid(G2frame,data)
        G2plt.PlotISFG(G2frame,type='I(Q)',newPlot=True)
    elif 'S(Q)' in G2frame.PatternTree.GetItemText(item):
        G2frame.PickId = item
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        data = G2frame.PatternTree.GetItemPyData(GetPatternTreeItemId(G2frame,G2frame.PatternId,'PDF Controls'))
        G2pdG.UpdatePDFGrid(G2frame,data)
        G2plt.PlotISFG(G2frame,type='S(Q)',newPlot=True)
    elif 'F(Q)' in G2frame.PatternTree.GetItemText(item):
        G2frame.PickId = item
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        data = G2frame.PatternTree.GetItemPyData(GetPatternTreeItemId(G2frame,G2frame.PatternId,'PDF Controls'))
        G2pdG.UpdatePDFGrid(G2frame,data)
        G2plt.PlotISFG(G2frame,type='F(Q)',newPlot=True)
    elif 'G(R)' in G2frame.PatternTree.GetItemText(item):
        G2frame.PickId = item
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        data = G2frame.PatternTree.GetItemPyData(GetPatternTreeItemId(G2frame,G2frame.PatternId,'PDF Controls'))
        G2pdG.UpdatePDFGrid(G2frame,data)
        G2plt.PlotISFG(G2frame,type='G(R)',newPlot=True)            
    elif G2frame.PatternTree.GetItemText(parentID) == 'Phases':
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        G2phG.UpdatePhaseData(G2frame,item,data,oldPage)
    elif G2frame.PatternTree.GetItemText(item) == 'Comments':
        SetDataMenuBar(G2frame,G2frame.dataFrame.DataCommentsMenu)
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        UpdateComments(G2frame,data)
    elif G2frame.PatternTree.GetItemText(item) == 'Image Controls':
        G2frame.dataFrame.SetTitle('Image Controls')
        G2frame.PickId = item
        G2frame.Image = G2frame.PatternTree.GetItemParent(item)
        masks = G2frame.PatternTree.GetItemPyData(
            GetPatternTreeItemId(G2frame,G2frame.Image, 'Masks'))
        data = G2frame.PatternTree.GetItemPyData(item)
        G2imG.UpdateImageControls(G2frame,data,masks)
        G2plt.PlotImage(G2frame)
    elif G2frame.PatternTree.GetItemText(item) == 'Masks':
        G2frame.dataFrame.SetTitle('Masks')
        G2frame.PickId = item
        G2frame.Image = G2frame.PatternTree.GetItemParent(item)
        data = G2frame.PatternTree.GetItemPyData(item)
        G2imG.UpdateMasks(G2frame,data)
        G2plt.PlotImage(G2frame)
    elif G2frame.PatternTree.GetItemText(item) == 'Stress/Strain':
        G2frame.dataFrame.SetTitle('Stress/Strain')
        G2frame.PickId = item
        G2frame.Image = G2frame.PatternTree.GetItemParent(item)
        data = G2frame.PatternTree.GetItemPyData(item)
        G2plt.PlotImage(G2frame)
        G2plt.PlotStrain(G2frame,data,newPlot=True)
        G2imG.UpdateStressStrain(G2frame,data)
    elif G2frame.PatternTree.GetItemText(item) == 'PDF Controls':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        for i in G2frame.ExportPDF: i.Enable(True)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        G2pdG.UpdatePDFGrid(G2frame,data)
        G2plt.PlotISFG(G2frame,type='I(Q)')
        G2plt.PlotISFG(G2frame,type='S(Q)')
        G2plt.PlotISFG(G2frame,type='F(Q)')
        G2plt.PlotISFG(G2frame,type='G(R)')
    elif G2frame.PatternTree.GetItemText(item) == 'Peak List':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        for i in G2frame.ExportPeakList: i.Enable(True)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
#patch
        if 'list' in str(type(data)):
            data = {'peaks':data,'sigDict':{}}
            G2frame.PatternTree.SetItemPyData(item,data)
#end patch
        G2pdG.UpdatePeakGrid(G2frame,data)
        G2plt.PlotPatterns(G2frame)
    elif G2frame.PatternTree.GetItemText(item) == 'Background':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        G2pdG.UpdateBackground(G2frame,data)
        G2plt.PlotPatterns(G2frame)
    elif G2frame.PatternTree.GetItemText(item) == 'Limits':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        datatype = G2frame.PatternTree.GetItemText(G2frame.PatternId)[:4]
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        G2pdG.UpdateLimitsGrid(G2frame,data,datatype)
        G2plt.PlotPatterns(G2frame,plotType=datatype)
    elif G2frame.PatternTree.GetItemText(item) == 'Instrument Parameters':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)[0]
        G2pdG.UpdateInstrumentGrid(G2frame,data)
        if 'P' in data['Type'][0]:          #powder data only
            G2plt.PlotPeakWidths(G2frame)
    elif G2frame.PatternTree.GetItemText(item) == 'Models':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        G2pdG.UpdateModelsGrid(G2frame,data)
        G2plt.PlotPatterns(G2frame,plotType='SASD')
        if len(data['Size']['Distribution']):
            G2plt.PlotSASDSizeDist(G2frame)
    elif G2frame.PatternTree.GetItemText(item) == 'Substances':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        G2pdG.UpdateSubstanceGrid(G2frame,data)
    elif G2frame.PatternTree.GetItemText(item) == 'Sample Parameters':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        datatype = G2frame.PatternTree.GetItemPyData(G2frame.PatternId)[2][:4]

        if 'Temperature' not in data:           #temp fix for old gpx files
            data = {'Scale':[1.0,True],'Type':'Debye-Scherrer','Absorption':[0.0,False],'DisplaceX':[0.0,False],
                'DisplaceY':[0.0,False],'Diffuse':[],'Temperature':300.,'Pressure':1.0,
                    'FreePrm1':0.,'FreePrm2':0.,'FreePrm3':0.,
                    'Gonio. radius':200.0}
            G2frame.PatternTree.SetItemPyData(item,data)
    
        G2pdG.UpdateSampleGrid(G2frame,data)
        G2plt.PlotPatterns(G2frame,plotType=datatype)
    elif G2frame.PatternTree.GetItemText(item) == 'Index Peak List':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        for i in G2frame.ExportPeakList: i.Enable(True)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
#patch
        if len(data) != 2:
            data = [data,[]]
            G2frame.PatternTree.SetItemPyData(item,data)
#end patch
        G2pdG.UpdateIndexPeaksGrid(G2frame,data)
        if 'PKS' in G2frame.PatternTree.GetItemText(G2frame.PatternId):
            G2plt.PlotPowderLines(G2frame)
        else:
            G2plt.PlotPatterns(G2frame)
    elif G2frame.PatternTree.GetItemText(item) == 'Unit Cells List':
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        if not data:
            data.append([0,0.0,4,25.0,0,'P1',1,1,1,90,90,90]) #zero error flag, zero value, max Nc/No, start volume
            data.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0])      #Bravais lattice flags
            data.append([])                                 #empty cell list
            data.append([])                                 #empty dmin
            data.append({})                                 #empty superlattice stuff
            G2frame.PatternTree.SetItemPyData(item,data)                             
#patch
        if len(data) < 5:
            data.append({'Use':False,'ModVec':[0,0,0.1],'maxH':1,'ssSymb':''})                                 #empty superlattice stuff
            G2frame.PatternTree.SetItemPyData(item,data)  
#end patch
        G2pdG.UpdateUnitCellsGrid(G2frame,data)
        if 'PKS' in G2frame.PatternTree.GetItemText(G2frame.PatternId):
            G2plt.PlotPowderLines(G2frame)
        else:
            G2plt.PlotPatterns(G2frame)
    elif G2frame.PatternTree.GetItemText(item) == 'Reflection Lists':   #powder reflections
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        G2frame.PickId = item
        data = G2frame.PatternTree.GetItemPyData(item)
        G2frame.RefList = ''
        if len(data):
            G2frame.RefList = data.keys()[0]
        G2pdG.UpdateReflectionGrid(G2frame,data)
        G2plt.PlotPatterns(G2frame)
    elif G2frame.PatternTree.GetItemText(item) == 'Reflection List':    #HKLF reflections
        G2frame.PatternId = G2frame.PatternTree.GetItemParent(item)
        name = G2frame.PatternTree.GetItemText(G2frame.PatternId)
        data = G2frame.PatternTree.GetItemPyData(G2frame.PatternId)
        G2pdG.UpdateReflectionGrid(G2frame,data,HKLF=True,Name=name)
    G2frame.dataFrame.Raise()

def SetDataMenuBar(G2frame,menu=None):
    '''Set the menu for the data frame. On the Mac put this
    menu for the data tree window instead.

    Note that data frame items do not have menus, for these (menu=None)
    display a blank menu or on the Mac display the standard menu for
    the data tree window.
    '''
    if sys.platform == "darwin":
        if menu is None:
            G2frame.SetMenuBar(G2frame.GSASIIMenu)
        else:
            G2frame.SetMenuBar(menu)
    else:
        if menu is None:
            G2frame.dataFrame.SetMenuBar(G2frame.dataFrame.BlankMenu)
        else:
            G2frame.dataFrame.SetMenuBar(menu)

def HorizontalLine(sizer,parent):
    '''Draws a horizontal line as wide as the window.
    This shows up on the Mac as a very thin line, no matter what I do
    '''
    line = wx.StaticLine(parent,-1, size=(-1,3), style=wx.LI_HORIZONTAL)
    sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 10)

def HowDidIgetHere():
    '''Show a traceback with calls that brought us to the current location.
    Used for debugging.
    '''
    import traceback
    print 70*'*'    
    for i in traceback.format_list(traceback.extract_stack()[:-1]): print(i.strip.rstrip())
    print 70*'*'    
        