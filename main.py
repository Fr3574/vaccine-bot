from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from time import sleep
from twilio.rest import Client 


MODE = "GETCODE" # GETCODE or GETDATE
account_sid = '' #for twilio
auth_token = '' # for twilio


code = "XXXX-XXXX-XXXX" 
number = ""
locations = [''] # if you have a code only use one entry

class VaccineBot:
    def __init__(self):

        self.url = "https://www.impfterminservice.de/impftermine"
        self.driver = webdriver.Chrome()
    
    def checkCodes(self, locations):
        #Visit URL
        print("HERE")
        self.driver.get(self.url)        
        sleep(2)

        # Select Impfzentrum
        self.driver.find_element_by_xpath("/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[1]/label/span[2]/span[1]/span").click()
        self.driver.find_element_by_xpath("//li[contains(text(), ' Baden-Württemberg ')]").click()

        for location in locations:
            print(location)
            self.driver.find_element_by_xpath("/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[2]/label/span[2]/span[1]/span").click()
            self.driver.find_element_by_xpath(f"//li[contains(text(), '{location}')]").click()
            self.driver.find_element_by_xpath("//button[contains(text(), ' Zum Impfzentrum ')]").click()
            sleep(2)

            # Wait in queue
            try:
                self.driver.find_element_by_class_name("clock")
                element = WebDriverWait(self.driver, 600).until(lambda d: d.find_element_by_xpath("//h1[contains(text(), 'Wurde Ihr Anspruch auf eine Corona-Schutzimpfung bereits geprüft?')]"))
                sleep(2)
            except:
                pass

            # Get Code
            try:
                self.driver.find_element_by_xpath("//span[contains(text(), ' Nein ')]").click()
                sleep(10)
            except:
                return ""

            try:
                self.driver.find_element_by_xpath("//div[contains(text(), ' Es wurden keine freien Termine in Ihrer Region gefunden. Bitte probieren Sie es später erneut. ')]")
                return ""
            except:
                self.driver.close()
                return location
        
    def checkAppointments(self, code, location):
        #Visit URL
        self.driver.get(self.url)        
        sleep(2)

        # Select Impfzentrum
        self.driver.find_element_by_xpath("/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[1]/label/span[2]/span[1]/span").click()
        self.driver.find_element_by_xpath("//li[contains(text(), ' Baden-Württemberg ')]").click()

        self.driver.find_element_by_xpath("/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[2]/label/span[2]/span[1]/span").click()
        self.driver.find_element_by_xpath(f"//li[contains(text(), '{location}')]").click()
        self.driver.find_element_by_xpath("//button[contains(text(), ' Zum Impfzentrum ')]").click()
        sleep(2)

        # Wait in queue
        try:
            self.driver.find_element_by_class_name("clock")
            element = WebDriverWait(self.driver, 600).until(lambda d: d.find_element_by_xpath("//h1[contains(text(), 'Wurde Ihr Anspruch auf eine Corona-Schutzimpfung bereits geprüft?')]"))
            sleep(2)
        except:
            pass
        
        # Enter Code
        try:
            self.driver.find_element_by_xpath("//span[contains(text(), ' Ja ')]").click()
            sleep(1)
        except:
            return False
        code_list = code.split("-")
        for index, value in enumerate(code_list):
            self.driver.find_element_by_xpath(f"//input[@name='ets-input-code-{index}']").send_keys(value)

        self.driver.find_element_by_xpath("//button[contains(text(), ' Termin suchen ')]").click()
        sleep(2)

        # #Termine suchen
        self.driver.find_element_by_xpath("//button[contains(text(), ' Termine suchen ')]").click()
        sleep(2)

        try:
            self.driver.find_element_by_class_name("its-slot-pair-search-no-results")
            return False
        except:
            self.driver.close()
            return True

    def sendNotification(self, text, number):
 
        client = Client(account_sid, auth_token) 
        
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body=text,      
                                    to=f'whatsapp:{number}' 
                                ) 

mybot = VaccineBot()
while True:
    if MODE == "GETDATE":
        AppointmentsExist = mybot.checkAppointments(code, locations[0])
        if AppointmentsExist:
            mybot.sendNotification("Impftermine sind frei.", number)
            break
        sleep(600)
    if MODE == "GETCODE":
        Location = mybot.checkCodes(locations)
        if len(Location) > 0:
            mybot.sendNotification(f"Impfcodes sind verfügbar in{Location}.", number)
            break
        sleep(600)