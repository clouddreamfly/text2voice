#!/usr/bin/python3
#-*- coding:utf-8 -*-

import os
import sys
import datetime
import pyttsx3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PlayThread(QThread):
    """"""

    def __init__(self, frame):
        """Constructor"""
        super().__init__()
        self._frame = frame
    
    def run(self):
        
        self._frame._engine.runAndWait()
        self._frame.updateButtonStatus(True, True)
        
        

class Text2VoiceFrame(QWidget):
    """"""

    def __init__(self):
        """Constructor"""
        
        super().__init__()
        
        self._engine = pyttsx3.init()
        self._thread = None
        
        self.initUI()
  
        
    def __del__(self):
        
        self._engine.stop()
        if self._thread:
            self._thread.quit() 
            self._thread = None
            
        super().__del__()
        
    def initUI(self):
        
        self.setWindowTitle("文字转语音")
        self.resize(560, 420)

        group = QGroupBox("输入文字区域：", self)
        self.txt_speek = QTextEdit("床前明月光，疑是地上霜。举头望明月，低头思故乡。", group)
        
        glayout = QVBoxLayout()
        glayout.addWidget(self.txt_speek)
        group.setLayout(glayout)
        
        self.btn_play = QPushButton("播放", self)
        self.btn_save = QPushButton("保存", self)
        self.btn_play.setFixedSize(80, 36)
        self.btn_save.setFixedSize(80, 36)
        
        
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        
        layout1.addWidget(group)
 
        layout2.addWidget(self.btn_play)
        layout2.addWidget(self.btn_save)
        
        layout.addLayout(layout1)
        layout.addSpacing(10)
        layout.addLayout(layout2)
        
        self.setLayout(layout)
        
        self.btn_play.clicked.connect(self.onClickedPlay)
        self.btn_save.clicked.connect(self.onClickedSave)
        
        
        self.updateButtonStatus(True, True)
        
    def updateButtonStatus(self, status1 = True, status2 = True):
        
        self.btn_play.setEnabled(status1)
        self.btn_save.setEnabled(status2)        
        
    def onClickedPlay(self, evt):
        
        txt_say = self.txt_speek.toPlainText()
        if txt_say:
            self.updateButtonStatus(False, False) 
            
            self._engine.say(txt_say)
            self._thread = PlayThread(self)
            self._thread.start()
            
        else:
            QMessageBox.warning(self, "警告提示", "请先输入文字信息内容！")
       
        
    def onClickedSave(self, evt):
        
        txt_say = self.txt_speek.toPlainText()
        if txt_say:
            self.updateButtonStatus(False, False)
            #获取当前时间,转化成字符串
            timenow = datetime.datetime.now()
            timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")
            
            #保存二维码图片
            if not os.path.exists("voices"):
                os.makedirs("voices")
                
            filename = "voices/voice-" + timestr + '.mp3'          
            self._engine.save_to_file(txt_say, filename)
            self._engine.runAndWait()
            self.updateButtonStatus(True, True)
            QMessageBox.information(self, "温馨提示", "保存成功！")
        else:
            QMessageBox.warning(self, "警告提示", "请先输入文字信息内容！")
            
        


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    frame = Text2VoiceFrame()
    frame.show()
    
    code = app.exec_()
    sys.exit(code)