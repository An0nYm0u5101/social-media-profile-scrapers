try:
    from bs4 import BeautifulSoup
    import argparse
    import selenium
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.options import Options as FirefoxOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from fake_headers import Headers
    from settings import DRIVER_SETTINGS
except ModuleNotFoundError:
    print("Please download dependencies from requirement.txt")
except Exception as ex:
    print(ex)    
class Reddit:
    @staticmethod   
    def init_driver(driver_path,browser_name):
        def set_properties(browser_option):
            ua = Headers().generate()      #fake user agent
            browser_option.add_argument('--headless')
            browser_option.add_argument('--disable-extensions')
            browser_option.add_argument('--incognito')
            browser_option.add_argument('--disable-gpu')
            browser_option.add_argument('--log-level=3')
            browser_option.add_argument(f'user-agent={ua}')
            browser_option.add_argument('--disable-notifications')
            browser_option.add_argument('--disable-popup-blocking')
            return browser_option
        try:
            browser_name = browser_name.strip().title()

            ua = Headers().generate()      #fake user agent
            #automating and opening URL in headless browser
            if browser_name == "Chrome":
                browser_option = ChromeOptions()
                browser_option = set_properties(browser_option)    
                driver = webdriver.Chrome(driver_path,options=browser_option) #chromedriver's path in first argument
            elif browser_name == "Firefox":
                browser_option = FirefoxOptions()
                browser_option = set_properties(browser_option)
                driver = webdriver.Firefox(executable_path=driver_path,options=browser_option)
            else:
                driver = "Browser Not Supported!"
            return driver
        except Exception as ex:
            print(ex)
    
    @staticmethod
    def scrap(username):
        try:
            URL = "https://reddit.com/user/{}".format(username)

            if DRIVER_SETTINGS['PATH'] != "" and DRIVER_SETTINGS['BROWSER_NAME'] != "":
                driver_path = DRIVER_SETTINGS['PATH']      
                browser = DRIVER_SETTINGS['BROWSER_NAME']    
                driver = Reddit.init_driver(driver_path,browser)  
            else:
                print("Driver is not set!. Please edit settings file for driver configurations.")
                exit()
            
            driver.get(URL)
            
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains("{}".format(username)))
            response = driver.page_source.encode('utf-8').strip()
             
            soup = BeautifulSoup(response,"html.parser")
                
            bio = soup.find("div",{
                    "class" : "bVfceI5F_twrnRcVO1328"
                }).text.strip()
                
            banners = soup.find("div",{
                    "class" : "_39u8lkB0jifV2dCyGxhTst"
                })
                
            profile = soup.find("img",{
                    "class" : "_2TN8dEgAQbSyKntWpSPYM7 M_wdt3XN_OW7h8RYbg38W"
                })
                
            karma = soup.find("span",{
                    "id" : "profile--id-card--highlight-tooltip--karma"
                }).text.strip()
                
            cake_date = soup.find("span",{
                    "id" : "profile--id-card--highlight-tooltip--cakeday"
                }).text.strip()
                
            driver.close()
            driver.quit()
            return {
                    "bio" : bio,
                    "banner" : banners['style'].split("(")[1].split("?")[0] if banners is not None else "Banner Not Found!",
                    "profile_image" : profile['src'].split("?")[0] if profile is not None else "Profile Image Not Found!",
                    "karma" : karma,
                    "cake_date" : cake_date
                }
        except Exception as ex:
            driver.close()
            driver.quit()
            print(ex)        
    
       

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username",help="username to search")
    args = parser.parse_args()
    print(Reddit.scrap(args.username))

#last updated - 31st july, 2020    
