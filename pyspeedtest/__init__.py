from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import subprocess
import time

SHORT_TIME = 2
LONG_TIME = 120
XPATH_BANNER = '//*[@id="onetrust-accept-btn-handler"]'
XPATH_GO = '//span[@class="start-text"]'

XPATH_PING = '//span[@class="result-data-value ping-speed"]'
XPATH_DOWNLOAD = '//span[@class="result-data-large number result-data-value download-speed"]'
XPATH_UPLOAD = '//span[@class="result-data-large number result-data-value upload-speed"]'

XPATH_ORG = '//div[@class="result-label js-data-isp"]'
XPATH_IP = '//div[@class="result-data js-data-ip"]'
XPATH_SPONSOR = '//a[@class="js-data-sponsor"]'
XPATH_CITY = '//div[@class="result-data js-sponsor-name"]'

# OLDER PATHS
# XPATH_GO='//*[@id="container"]/div[2]/div/div/div/div[3]/div[1]/div[1]/a/span[4]'
# XPATH_PING     = '/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[3]/div/div[1]/div[2]/div[1]/div/div[2]/span'
# XPATH_DOWNLOAD = '/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/span'
# XPATH_UPLOAD   = '/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[3]/div/div[1]/div[2]/div[3]/div/div[2]/span'
# XPATH_ORG='//*[@id="container"]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[4]/div/div[2]/div/div[1]/div[2]'
# XPATH_IP='//*[@id="container"]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[4]/div/div[2]/div/div[1]/div[3]'
TCPDUMP_CMD = "{} -i {} -w {} {}"


def run_speedtest(browser="chrome", pcap_path="/tmp/a.pcap", pcap_opt="-s 60", pcap_iface='any', pcap_bin='tcpdump'):
    # Start Capture
    tcpdump = subprocess.Popen(TCPDUMP_CMD.format(pcap_bin, pcap_iface, pcap_path, pcap_opt).split())

    try:

        # Start WebDriver and go on https://www.speedtest.net/
        if browser.lower() == "firefox":
            driver = webdriver.Firefox()
        elif browser.lower() == "chrome":
            driver = webdriver.Chrome()
        elif browser.lower() == "safari":
            driver = webdriver.Safari()
        elif browser.lower() == "edge":
            driver = webdriver.Edge()
        elif browser.lower() == "explorer":
            ieCapabilities = webdriver.DesiredCapabilities().INTERNETEXPLORER.copy()
            ieCapabilities["nativeEvents"] = False
            ieCapabilities["unexpectedAlertBehaviour"] = "accept"
            ieCapabilities["ignoreProtectedModeSettings"] = True
            ieCapabilities["blocking"] = True
            ieCapabilities["enablePersistentHover"] = True
            ieCapabilities["ignoreZoomSetting"] = True
            ieCapabilities["ensureCleanSession"] = True
            driver = webdriver.Ie(desired_capabilities=ieCapabilities)
        else:
            print("Unsupported browser")
            return
        driver.get("https://www.speedtest.net/")

        # Click Banner
        elem = driver.find_elements("xpath", XPATH_BANNER)
        print("Element ", elem)
        if len(elem) > 0:
            if browser.lower() == "safari":
                driver.execute_script("arguments[0].click();", elem[0])
            else:
                elem[0].click()
        time.sleep(SHORT_TIME)

        # Click Go
        elem = driver.find_elements("xpath", XPATH_GO)
        if browser.lower() == "safari":
            driver.execute_script("arguments[0].click();", elem[0])
        else:
            elem[0].click()
        time.sleep(SHORT_TIME)

        # Wait Results
        def num_there(s):
            return any(i.isdigit() for i in s)

        element = WebDriverWait(driver, LONG_TIME).until(
            lambda driver: num_there(driver.find_elements("xpath", XPATH_UPLOAD)[0].text))
        time.sleep(SHORT_TIME)

        # Get Results
        ping = driver.find_elements("xpath", XPATH_PING)[0].text
        download = driver.find_elements("xpath", XPATH_DOWNLOAD)[0].text
        upload = driver.find_elements("xpath", XPATH_UPLOAD)[0].text
        org = driver.find_elements("xpath", XPATH_ORG)[0].text
        sip = driver.find_elements("xpath", XPATH_IP)[0].text
        sponsor = driver.find_elements("xpath", XPATH_SPONSOR)[0].text
        city = driver.find_elements("xpath", XPATH_CITY)[0].text

        # Close
        driver.close()
        tcpdump.terminate()

        return {"ping_ms": ping,
                "download_mbps": download,
                "upload_mbps": upload,
                "organization": org,
                "server_ip": sip,
                "sponsor": sponsor,
                "city": city}

    except:
        if 'tcpdump' in locals():
            tcpdump.terminate()
        if 'driver' in locals():
            driver.close()
        raise
