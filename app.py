from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from hotmail import Hotmail


# creating a hotmail class 

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.numSeedsToCreate = QSpinBox()
        self.to = QLineEdit()
        self.subject = QLineEdit()
        self.textEdit = QTextEdit()

        grid = QGridLayout()
        grid.addWidget(self.create(), 0, 0)
        grid.addWidget(self.recover(), 0, 1)
        grid.addWidget(self.reporting(),0, 2)
        grid.addWidget(self.send(), 1, 0)
        grid.addWidget(self.proxy(), 1, 1)
        grid.addWidget(self.features(), 1, 2)


        self.setLayout(grid)
        
        self.setWindowTitle("hotmail app")
        self.setFixedSize(1000, 700)
    def use_list(self):        
        _host = self.textEdit.toPlainText().split("\n")

        if len(_host) > 0:
            for h in _host:
                HOST.append(h)
            print(len(HOST))
            QMessageBox.about(self, "success","proxies added succesfully")
            
        else:
            QMessageBox.about(self, "error","proxy list is empty")

    def add_proxy(self):
        filepath = QFileDialog.getOpenFileName(self, 'Select Folder')
        if list(filepath)[0]:
            with open(list(filepath)[0], 'r',encoding='UTF-8') as f:   
                reader = csv.reader(f, delimiter=',')
                for line in reader:
                    if line:
                        HOST.append(line[0])
        print(len(HOST))
    # functional logique
    def _create(self):  
        i = 0
        if len(HOST) != 0:
            if int(self.numSeedsToCreate.text()) > 0:
                folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
                if folderpath:
                    while i < int(self.numSeedsToCreate.text()):
                        #create a hotmail obj
                        _hotmail = Hotmail()
                        #create a hotmail mail
                        try:
                            _hotmail.create()
                            DATA = {
                                'host':_hotmail.get_host(),
                                'port':_hotmail.get_port(),
                                'email':_hotmail.get_email(),
                                'password':_hotmail.get_password(),
                                'confirmation_mail':_hotmail.get_confirmation_mail()
                            }
                            _date = datetime.datetime.now()
                            filename =str(f'{_date.day}-{_date.month}-{_date.year}.csv')
                            with open(f"{folderpath}\{filename}",'a') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(DATA.values())
                        except Exception:
                            pass
                        #incriment
                        i+=1
         
            else:
                QMessageBox.about(self, "Error", "number must be greater then 0")
        else:
            QMessageBox.about(self,"Error"," proxy empty")
    def _reporting(self):
        filepath = QFileDialog.getOpenFileName(self, 'Select Folder')
        if list(filepath)[0]:
            seeds:list=[]
            with open(list(filepath)[0],'r',encoding='UTF-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for line in reader:
                    if line:
                        seeds.append(line)
            for seed in seeds:
                h = Hotmail()
                h.set_host(seed[0])
                h.set_port(seed[1])
                h.set_email(seed[2])
                h.set_password(seed[3])
                h.reporting()
    
    def _recover(self):
        filepath = QFileDialog.getOpenFileName(self, 'Select Folder')
        if list(filepath)[0]:
            seeds:list=[]
            with open(list(filepath)[0],'r',encoding='UTF-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for line in reader:
                    if line:
                        seeds.append(line)
            for seed in seeds:
                h = Hotmail()
                h.set_host(seed[0])
                h.set_port(seed[1])
                h.set_email(seed[2])
                h.set_password(seed[3])
                h.set_confirmation_mail(seed[4])
                h.recover()
    
    def _send(self):
        filepath = QFileDialog.getOpenFileName(self, 'Select Folder')
        if list(filepath)[0]:
            seeds:list=[]
            with open(list(filepath)[0],'r',encoding='UTF-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for line in reader:
                    if line:
                        seeds.append(line)
            for seed in seeds:
                h = Hotmail()
                h.set_host(seed[0])
                h.set_port(seed[1])
                h.set_email(seed[2]
                h.set_password(seed[3])
                h.send(self.to.text(),self.subject.text())
    
    def delete_spam(self):
        filepath = QFileDialog.getOpenFileName(self, 'Select Folder')
        if list(filepath)[0]:
            seeds:list=[]
            with open(list(filepath)[0],'r',encoding='UTF-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for line in reader:
                    if line:
                        seeds.append(line)
            for seed in seeds:
                h = Hotmail()
                h.set_host(seed[0])
                h.set_port(seed[1])
                h.set_email(seed[2])
                h.set_password(seed[3])
                h.delete_spam()
    
    def login(self):
        filepath = QFileDialog.getOpenFileName(self, 'Select Folder')
        if list(filepath)[0]:
            seeds:list=[]
            with open(list(filepath)[0],'r',encoding='UTF-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for line in reader:
                    if line:
                        seeds.append(line)
            for seed in seeds:
                h = Hotmail()
                h.set_host(seed[0])
                h.set_port(seed[1])
                h.set_email(seed[2])
                h.set_password(seed[3])
                h.login()
   # layout 
    def create(self):
        groupBox = QGroupBox("create seeds")
        label = QLabel("")

        buttonBox = QPushButton("create")
        buttonBox.clicked.connect(self._create)
        buttonBox.setFixedSize(100,30)

        vbox = QVBoxLayout()
        vbox.addWidget(self.numSeedsToCreate)
        vbox.addWidget(label)
        vbox.addWidget(buttonBox)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        groupBox.setFixedSize(300,250)
        return groupBox
    
    def recover(self):
        groupBox = QGroupBox("recover seeds")
        label = QLabel("import csv file with this form: ")
        labe2 = QLabel("host,port,email,password,mailrecovery")

        buttonBox = QPushButton("recover")
        buttonBox.clicked.connect(self._recover)

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(labe2)

        vbox.addWidget(buttonBox)        
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        groupBox.setFixedSize(300,250)

        return groupBox
    
    def reporting(self):
        groupBox = QGroupBox("reporting junck to inbox")
        label = QLabel("import csv file with this form")
        labe2 = QLabel(": host,port,email,password")

        buttonBox = QPushButton("reporting")
        buttonBox.clicked.connect(self._reporting)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(labe2)
        vbox.addWidget(buttonBox)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)    
        groupBox.setFixedSize(300,250)

        return groupBox
    
    def send(self):
        groupBox = QGroupBox("send mail a spesific mail box")
        label = QLabel("to")
        labe2 = QLabel("subject")

        buttonBox = QPushButton("send")
        buttonBox.clicked.connect(self._send)
        buttonBox.setFixedSize(100,30)

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(self.to)
        vbox.addWidget(labe2)
        vbox.addWidget(self.subject)
        vbox.addWidget(buttonBox)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)  
        groupBox.setFixedSize(300,250)

        return groupBox
    
    def proxy(self):
        groupBox = QGroupBox("import proxies")
        
        buttonBox = QPushButton("add proxy")
        buttonBox.clicked.connect(self.add_proxy)
        buttonBox2 = QPushButton("use this list")
        buttonBox2.clicked.connect(self.use_list)

        vbox = QVBoxLayout()

        vbox.addWidget(buttonBox)
        vbox.addWidget(self.textEdit)
        vbox.addWidget(buttonBox2)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)  
        groupBox.setFixedSize(300,250)

        return groupBox
    
    def features(self):
        groupBox = QGroupBox("login or delete spam ")
        
        label = QLabel("import csv file with this form:")
        labe2 = QLabel(" host,port,email,password")

        buttonBox = QPushButton("login")
        buttonBox2 = QPushButton("empty spam folder")
        buttonBox.clicked.connect(self.login)
        buttonBox2.clicked.connect(self.delete_spam)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(labe2)

        vbox.addWidget(buttonBox)
        vbox.addWidget(buttonBox2)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)  
        groupBox.setFixedSize(300,250)

        return groupBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())