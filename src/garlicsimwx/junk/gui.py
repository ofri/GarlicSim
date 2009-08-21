import wx
import os
from misc.stringsaver import s2i,i2s
import time
from core import *
import simulations.life.life as life
import simulations.life.lifegui as lifegui
import threading
import random
import functools

#import psyco
#psyco.full()


"""
class time_to_talk_with_manager_event(wx.PyCommandEvent):
    pass

myEVT_TIME_TO_TALK_WITH_MANAGER=wx.NewEventType()
EVT_TIME_TO_TALK_WITH_MANAGER=wx.PyEventBinder(myEVT_TIME_TO_TALK_WITH_MANAGER,1)
"""


class myframe(wx.Frame):
    def __init__(self,*args,**keywords):
        wx.Frame.__init__(self,*args,**keywords)
        self.SetDoubleBuffered(True)


        self.thing=wx.ScrolledWindow(self,-1)
        self.timeline=customwidgets.Timeline(self,-1)
        self.tree_browser=customwidgets.TreeBrowser(self,-1)



        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.thing,1,wx.EXPAND)
        self.sizer.Add(self.timeline,0,wx.EXPAND)
        self.sizer.Add(self.tree_browser,0,wx.EXPAND)


        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        #self.sizer.Fit(self)

        #self.Bind(wx.EVT_PAINT, self.draw)



        self.mygui=lifegui.LifeGuiProject(Project(life.Life),self.thing)
        self.root=self.mygui.make_random_root(28,40)

        self.timeline.path=self.mygui.path
        self.timeline.gui_project=self.mygui

        self.tree_browser.tree=self.mygui.project.tree
        self.tree_browser.gui_project=self.mygui

        self.mygui.project.leaves_to_render=[self.root]
        self.mygui.set_active_node(self.root)


        self.Bind(wx.EVT_IDLE,self.manage_workers_wrapper)

        filemenu=wx.Menu()
        filemenu.Append(s2i("Exit"),"E&xit"," Close the program")

        wx.EVT_MENU(self,s2i("Exit"),self.exit)

        stuffmenu=wx.Menu()
        stuffmenu.Append(s2i("Play"),"&Play","")
        stuffmenu.Append(s2i("Stop"),"&Stop","")

        wx.EVT_MENU(self,s2i("Play"),self.play)
        wx.EVT_MENU(self,s2i("Stop"),self.stop)

        self.nodemenu=nodemenu=wx.Menu()
        nodemenu.Append(s2i("Fork by editing"),"Fork by &editing"," Create a new edited node with the current node as the template")
        nodemenu.Append(s2i("Fork naturally"),"Fork &naturally"," Run the simulation from this node")
        nodemenu.AppendSeparator()
        nodemenu.Append(s2i("Delete..."),"&Delete..."," Delete the node")

        wx.EVT_MENU(self,s2i("Fork by editing"),self.mygui.edit_from_active_node)
        wx.EVT_MENU(self,s2i("Fork naturally"),self.mygui.step_from_active_node)








        menubar=wx.MenuBar()
        menubar.Append(filemenu,"&File")
        menubar.Append(stuffmenu,"&Stuff")
        menubar.Append(nodemenu,"&Node")
        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar.AddSimpleTool(s2i("Button New"), wx.Bitmap("images\\new.png", wx.BITMAP_TYPE_ANY),"New", " Create a new file")
        toolbar.AddSimpleTool(s2i("Button Open"), wx.Bitmap("images\\open.png", wx.BITMAP_TYPE_ANY),"Open", " Open a file")
        toolbar.AddSimpleTool(s2i("Button Save"), wx.Bitmap("images\\save.png", wx.BITMAP_TYPE_ANY),"Save", " Save to file")
        toolbar.Realize()

        self.Show()
        #self.draw()


    def play(self,e):
        self.mygui.start_playing()

    def stop(self,e):
        self.mygui.stop_playing()



    def draw(self,e=None):
        pass


    def exit(self,e):
        self.Close()

    def manage_workers_wrapper(self,e=None):
        self.mygui.project.manage_workers()
        self.Refresh()
        try:
            e.RequestMore()
        except:
            pass



if __name__=="__main__":
    app = wx.PySimpleApp()
    import customwidgets
    fugi=myframe(None,-1,"Title",size=(600,600))
    app.MainLoop()