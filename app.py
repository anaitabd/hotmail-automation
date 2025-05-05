import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import csv
#hotmail import 
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as options
import requests
from datetime import datetime, timedelta
import random
from fakename import load_fake_names, get_fake_name
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
#URLS
SINGN_UP:str = "https://signup.live.com/signup"
FAKE_USER_GENERATOR:str ="https://www.fakenamegenerator.com/gen-random-us-uk.php"
PROOFS_ADD:str = "https://account.live.com/proofs/Add"
LOGIN:str = "https://outlook.live.com/owa/?nlp=1"

# PROXY VARIABLES
HOST :list[str] = []
PORT :str= "3128"

# creating a hotmail class 

class Hotmail:
    ''' hotmail class for creation and saving seeds '''

    def __init__(self) -> None:
        self.host = str
        self.port = str
        self.firstname = str
        self.lastname = str
        self.email = str
        self.password = str
        self.birthday = str
        self.confirmation_mail = str
    
    def get_host(self)->str:
        ''' get host'''
        return self.host
    def set_host(self,host)->None:
        ''' set host'''
        self.host = host
    
    def get_port(self)->str:
        ''' get port'''
        return self.port
    def set_port(self,port)->None:
        '''set port'''
        self.port = port

    def get_email(self)->str:
        '''get email'''
        return self.email
    def set_email(self,email)->None:
        '''set email'''
        self.email = email
    
    def get_password(self)->str:
        ''' get password'''
        return self.password
    def set_password(self,password)->None:
        ''' set password'''
        self.password = password
    
    def get_confirmation_mail(self)->str:
        '''get_confirmation_mail'''
        return self.confirmation_mail
    
    def set_confirmation_mail(self,confirmation_mail)->None:
        '''set_confirmation_mail'''
        self.confirmation_mail = confirmation_mail

    def my_proxy(self) -> webdriver:
        ''' open a Chrome profile using a specific proxy '''        
        try:
            browser = Chrome(service=ChromeService(ChromeDriverManager().install()))
        except Exception:
            print("chrome not installed")
            browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        except Exception as e:
            print(f"Error: {e}")
            return None
        return browser

    def clear_and_input(self,id:any,value:str,browser:webdriver)->None:
        """ clear and put value in input field """
        elem = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.ID, id))
        )
        elem.clear()
        elem.send_keys(value)
    
    def click_(self,browser,id:any)->None:
        """ click on submit button """
        elem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, id))
        )
        elem.click()

    def generate_user_info(self):
        """Génère les informations utilisateur en utilisant l'API de fakenamegenerator"""
        try:
            fake_names = load_fake_names('fake_names.csv')
            self.firstname, self.lastname = get_fake_name(fake_names)
            self.email = f"{self.lastname}_{self.firstname}_{random.randint(1, 1000)}@hotmail.com"
            self.password = f"{self.firstname}{self.lastname}{random.randint(1, 500)}@"
            
            # Generate a random birthday between 1970-01-01 and 2005-12-31
            start_date = datetime(1970, 1, 1)
            end_date = datetime(2005, 12, 31)
            delta = end_date - start_date
            random_days = random.randint(0, delta.days)
            birthday = start_date + timedelta(days=random_days)
            self.birthday = birthday.strftime('%d/%m/%Y')  # Format: DD/MM/YYYY
            
        except Exception as e:
            print(f"Erreur lors de la génération des données utilisateur : {e}")
        
    def create(self) -> None:
        ''' create a hotmail account '''
        #get user info {firstname,lastname,email,password}
        self.generate_user_info()    
        # get a random proxy
        while True:
            try:
                self.set_host(random.choice(HOST))
                self.set_port(int(PORT))
                browser = self.my_proxy()
                print(f'{self.firstname} {self.lastname} {self.host}:{self.port}')

                break
            except Exception:
                print(f'{self.host} not working')
        
        #get sign-up url
        browser.get(SINGN_UP)
        browser.maximize_window()

        try:
            print("email : ",self.email)
            self.clear_and_input("usernameInput",self.email,browser)
            print("next button")
            self.click_(browser=browser,id="nextButton")
            print("password : ",self.password)
            self.clear_and_input(id="Password",value=self.password,browser=browser)
            self.click_(browser=browser,id="nextButton")

            self.clear_and_input(id="firstNameInput",value=self.firstname,browser=browser)
            self.clear_and_input(id="lastNameInput",value=self.lastname,browser=browser)
            self.click_(browser=browser,id="nextButton")

            #create a random date of birth 
            day = int(random.randint(2,29))
            month = int(random.randint(2,13))
            year = random.randint(1976,2004)
            self.birthday = str(day)+'/'+str(month-1)+'/'+str(year)
            _day = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.ID, "BirthDay"))
            )
            Select(_day).select_by_index(day)
            _month = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.ID, "BirthMonth"))
            )
            Select(_month).select_by_index(month)
            self.clear_and_input(id="BirthYear",value=str(year),browser=browser)

            #submit all info to get the captcha
            browser.find_element(By.ID,"nextButton").click()
            self.confirmation_mail = self.firstname+'_'+self.lastname+str(random.randint(1,20))

            #get the captcha
            sleep(5000000)
        except Exception:
            print(f'{self.get_host()}:{self.get_port} // email : {self.get_email()}')
            browser.close()

    def get_code(self,email)->str:
        ''' get code from the mail box '''
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.maximize_window()
        driver.get("https://www.guerrillamail.com/")
        self.click_(browser=driver,id="inbox-id")
        elem = driver.find_element(By.ID,'inbox-id').find_element(By.TAG_NAME,'input')
        elem.clear()
        elem.send_keys(email)
        driver.find_element(By.CLASS_NAME,'save').click()
        domain = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "gm-host-select"))
        )
        Select(domain).select_by_value('guerrillamail.info')
        sleep(10)
        mail = driver.find_element(By.ID,'email_list')
        tr = mail.find_elements(By.TAG_NAME,'tr')
        td =tr[0].find_elements(By.TAG_NAME,'td')
        td[1].click()
        email_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "email_body"))
        )
        _tr = email_body.find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr')
        td = _tr[3].find_element(By.TAG_NAME,'td')
        code :str = td.find_element(By.TAG_NAME,'span').text  
        driver.quit()
        return code
    
    def recover(self) ->None:
        ''' add recovery mail to the email created'''        
        browser = self.my_proxy()
        try:
            browser.get(PROOFS_ADD)
            try:
                self.clear_and_input(id="i0116",value=self.email,browser=browser)
                self.click_(browser=browser,id="idSIButton9")
                sleep(3)
                pwd = browser.find_element(By.ID,"i0118")
                pwd.send_keys(self.password)
                browser.find_element(By.ID,"idSIButton9").click()
                sleep(5)
                browser.find_element(By.ID,'EmailAddress').send_keys(self.confirmation_mail+'@guerrillamail.info')
                self.click_(browser=browser,id="iNext")

                # get email verification code 
                code = self.get_code(email=self.confirmation_mail)
                
                self.clear_and_input(id="iOttText",value=code,browser=browser)
                self.click_(browser=browser,id="iNext")
            except Exception:
                pass
            elem = WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'table'))
                )
            elem.click()
            self.clear_and_input(id="idTxtBx_SAOTCS_ProofConfirmation", value=self.confirmation_mail+'@guerrillamail.info',browser=browser)    
            self.click_(browser=browser,id="idSubmit_SAOTCS_SendCode")       

            # get email verification code
            code = self.get_code(email=self.confirmation_mail)

            self.clear_and_input(id="idTxtBx_SAOTCC_OTC",value=code,browser=browser)
            self.click_(browser=browser,id="idSubmit_SAOTCC_Continue")
            sleep(3)
            browser.quit()
        except Exception:
            print(self.toString())
            browser.quit()  

    def go_junk(self,browser):
        browser.get("https://outlook.live.com/mail/junkemail")

    def reply(self,browser):
        pass

    def flag(self,browser):
        button = browser.find_elements(By.CLASS_NAME,"splitPrimaryButton ")   
        button[4].click()

    def ping(self,browser):
        self.click_(browser=browser,id="548")

    def reporting(self):    
        browser = self.my_proxy()     
        browser.get(LOGIN)
        try:
            self.clear_and_input(id="i0116",value=self.email,browser=browser)
            self.click_(browser=browser,id="idSIButton9")
            sleep(3)
            pwd = browser.find_element(By.ID,"i0118")
            pwd.send_keys(self.password)
            browser.find_element(By.ID,"idSIButton9").click()   
            try: 
                elem = WebDriverWait(browser,30).until(
                    EC.presence_of_element_located((By.id,'iShowSkip'))
                )
                elem.click()
            except Exception:
                self.click_(browser=browser,id="idBtn_Back")
            sleep(1)
            self.go_junk(browser=browser)
            try:
                elem = WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "zXLz3"))
                )
                mails = elem.find_elements(By.TAG_NAME,"div")
                total_mails = len(mails)
                for i in range(total_mails):
                    n = random.randrange(1,150)
                    mails[1].click()
                    sleep(5)
                    if n%2 == 0:
                        self.flag(browser=browser)
                        sleep(5)
                    browser.find_element(By.ID,"540").click()
                    try:
                        inbox = WebDriverWait(browser, 30).until(
                            EC.presence_of_element_located((By.NAME, "Boîte de réception"))
                        )
                        inbox.click()
                    except:
                        inbox = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.NAME, "Inbox"))
                        )
                        inbox.click()
                    try:
                        form = WebDriverWait(browser, 20).until(
                            EC.presence_of_element_located((By.TAG_NAME, "form"))
                        )
                        form.submit()
                    except Exception:
                        pass
                    try:
                        elem = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "zXLz3"))
                        )
                        mails = elem.find_elements(By.TAG_NAME,"div")
                    except Exception:
                        browser.close()
                        return True
            except Exception:
                print(self.get_email())
                browser.close()
                return True
        except Exception:
            print(self.get_email)
            browser.close()
            
    def send(self,to,subject):
        browser = self.my_proxy()     
        browser.get(LOGIN)
        try: 
            self.clear_and_input(id="i0116",value=self.email,browser=browser)
            self.click_(browser=browser,id="idSIButton9")
            sleep(3)
            pwd = browser.find_element(By.ID,"i0118")
            pwd.send_keys(self.password)
            browser.find_element(By.ID,"idSIButton9").click()  
            try: 
                elem1 = WebDriverWait(browser,5).until(
                    EC.presence_of_element_located((By.id,'iShowSkip'))
                )
                elem.click()
            except Exception:
                self.click_(browser=browser,id="idBtn_Back")
            sleep(30)
            buttons =browser.find_elements(By.CLASS_NAME,"splitPrimaryButton")
            buttons[0].click()
            elem = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "UKx9j"))
                )
            sub_elem = elem.find_elements(By.TAG_NAME,"div")
            sub_elem[1].send_keys(to)
            elem = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ms-TextField-field"))
                )
            elem.send_keys(subject)
            try:
                browser.find_element(By.XPATH,'//*[@title="Envoyer (Ctrl+Entrée)"]').click()
            except Exception:
                browser.find_element(By.XPATH,'//*[@title="Send (Ctrl+Entrée)"]').click()

            sleep(5)
        except Exception:
            print(self.email)
        finally:
            browser.close()
    
    def delete_spam(self):
        browser = self.my_proxy()     
        browser.get(LOGIN)
        try:
            self.clear_and_input(id="i0116",value=self.email,browser=browser)
            self.click_(browser=browser,id="idSIButton9")
            sleep(3)
            pwd = browser.find_element(By.ID,"i0118")
            pwd.send_keys(self.password)
            browser.find_element(By.ID,"idSIButton9").click()   
            
            self.click_(browser=browser,id="idBtn_Back")
            sleep(1)
            self.go_junk(browser=browser)
        
            sleep(5)
            elem = WebDriverWait(browser,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'vQae6'))
            )
            elem.click()
            buttons = browser.find_elements(By.CLASS_NAME,'splitPrimaryButton')
            buttons[1].click()
            ok = WebDriverWait(browser,10).until(
                EC.presence_of_element_located((By.ID,'ok-1'))
            )
            ok.click()
            sleep(5)
        except Exception:
            print(self.email)
        finally:
            browser.close()

    def login(self):
        browser = self.my_proxy()     
        browser.get(LOGIN)
        try:
            self.clear_and_input(id="i0116",value=self.email,browser=browser)
            self.click_(browser=browser,id="idSIButton9")
            sleep(3)
            pwd = browser.find_element(By.ID,"i0118")
            pwd.send_keys(self.password)
            browser.find_element(By.ID,"idSIButton9").click()   
            
            self.click_(browser=browser,id="idBtn_Back")
        except Exception:
            browser.close()

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
                h.set_email(seed[2])
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