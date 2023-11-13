from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

class Generator():
    """
    Creates a generator instance that stays alive.
    Not bound per site.
    """
    
    def __init__(self, executable_path: str):
        self.set_up_browser(executable_path)
        
        self.is_working = False    
            
    def set_up_browser(self, executable_path: str) -> None:
        options: Options = Options()

        options.add_argument('--headless=new') # New version = OP
        options.add_argument('--no-sandbox') # Not needed?
        options.add_argument("--disable-blink-features=AutomationControlled") # This one is also needed to get not detected 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Not needed?
        options.add_experimental_option("useAutomationExtension", False) # Not needed?
        
        service: Service = Service(executable_path)
        service.start()

        self.driver: webdriver.Chrome = webdriver.Chrome(service=service, options=options)
        
    def generate(self, aihToken: str, reese_script: str) -> dict[dict[str, str], int]: # TODO: Check if dynamic loading the script fucks it up
        self.is_working = True
        self.driver.get('file://%s' % os.path.abspath('./files/enviroment/index.html'))
        
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.title_is("Incap"))
        
        self.driver.execute_script(reese_script)
        self.driver.execute_script("""
            window.DateTimer = new DateTimer(); 
            const interrogatorInstance = new window.reese84interrogator({
                    s: hasher.hash,
                    t: window.DateTimer,
                    aih: '""" + aihToken + """',
                    at: 1 // Token count
                })

            const logData = (data) => {
                window.incapdata = data; // Log the data
                window.timeSum = window.DateTimer.summary()
                return data; // Return the data
            };

            interrogatorInstance.interrogate(
                logData, // Pass the logData function as the success callback
                logData  // Pass the logData function as the error callback
            );
        """)
        
        incapData = None
        timeSum = None
        while incapData == None or timeSum == None:
            incapData = self.driver.execute_script('return window.incapdata')
            timeSum = self.driver.execute_script('return window.timeSum')

        self.driver.delete_all_cookies()
        
        self.is_working = False
        return {
            'data': incapData,
            'timeSum': int(timeSum['interrogation'])
        }
        
if __name__ == '__main__':
    executable_path = os.path.abspath('./files/chromedriver.exe')
    print(executable_path)
    gen = Generator(executable_path)
    gen.generate('test')