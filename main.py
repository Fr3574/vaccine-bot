from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from time import sleep
from twilio.rest import Client 
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

class VaccineBot:
    def __init__(self):
        options = FirefoxOptions()
        if config['Mode']['Headless'] == "True":
            options.add_argument("--headless")
        self.url = "https://www.impfterminservice.de/impftermine"
        self.driver = webdriver.Firefox(options=options)
        self.driver.set_window_size(3840,2160)
    
    def checkCodes(self):
        locations = config['Data']['locations'].split("/")
        for location in locations:
            #Visit URL
            self.driver.get(self.url)        
            sleep(2)

            # Select Impfzentrum
            self.driver.find_element_by_xpath("/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[1]/label/span[2]/span[1]/span").click()
            self.driver.find_element_by_xpath("//li[contains(text(), ' {} ')]".format(config['Data']['federal_state'])).click()

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
                pass

            try:
                self.driver.find_element_by_xpath("//div[contains(text(), ' Es wurden keine freien Termine in Ihrer Region gefunden. Bitte probieren Sie es später erneut. ')]")
                pass
            except:
                self.driver.close()
                return location
        
    def checkAppointments(self):
        #Visit URL
        self.driver.get(self.url)        
        sleep(2)

        # Select Impfzentrum
        self.driver.find_element_by_xpath("/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[1]/label/span[2]/span[1]/span").click()
        self.driver.find_element_by_xpath("//li[contains(text(), ' {} ')]".format(config['Data']['federal_state'])).click()

        self.driver.find_element_by_xpath("/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[2]/label/span[2]/span[1]/span").click()
        self.driver.find_element_by_xpath("//li[contains(text(), '{}')]".format(config['Data']['locations'].split("/")[0])).click()
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
        code_list = config['Data']['code'].split("-")
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

    def sendNotification(self, text):
 
        client = Client(config['Twilio']['account_sid'],config['Twilio']['auth_token']) 
        
        message = client.messages.create( 
                                    from_='whatsapp:{}'.format(config['Twilio']['twilio_number']),  
                                    body=text,      
                                    to='whatsapp:{}'.format(config['Twilio']['your_number']) 
                                ) 

mybot = VaccineBot()
while True:
    if config['Mode']['MODE'] == "GETDATE":
        AppointmentsExist = mybot.checkAppointments()
        if AppointmentsExist:
            mybot.sendNotification("Impftermine sind frei.")
            break
        sleep(600)
    if config['Mode']['MODE'] == "GETCODE":
        Location = mybot.checkCodes()
        if isinstance(Location, str):
            mybot.sendNotification(f"Impfcodes sind verfügbar in{Location}.")
            break
        sleep(600)