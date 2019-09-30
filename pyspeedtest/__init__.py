from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import subprocess
import time

SHORT_TIME=2
LONG_TIME=120
XPATH_BANNER='//*[@id="_evidon-banner-acceptbutton"]'
XPATH_GO='//*[@id="container"]/div[2]/div/div/div/div[3]/div[1]/div[1]/a/span[4]'
XPATH_PING     = '/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[3]/div/div[1]/div[2]/div[1]/div/div[2]/span'
XPATH_DOWNLOAD = '/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/span'
XPATH_UPLOAD   = '/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[3]/div/div[1]/div[2]/div[3]/div/div[2]/span'
XPATH_ORG='//*[@id="container"]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[4]/div/div[2]/div/div[1]/div[2]'
XPATH_IP='//*[@id="container"]/div[2]/div/div/div/div[3]/div[1]/div[3]/div/div[4]/div/div[2]/div/div[1]/div[3]'
TCPDUMP_CMD="tcpdump -i any -w {} {}"
KILL_TCPDUMP="killall -INT tcpdump"

def run_speedtest(browser="chrome", pcap_path="/tmp/a.pcap", pcap_opt="-s 60"):

    # Start Capture
    tcpdump = subprocess.Popen(TCPDUMP_CMD.format(pcap_path, pcap_opt), shell=True)

    # Start WebDriver and go on https://www.speedtest.net/
    if browser.lower() == "firefox":
        driver = webdriver.Firefox()
    elif browser.lower() == "chrome":
        driver = webdriver.Chrome()
    else:
        print("Unsupported browser")
        return
    driver.get("https://www.speedtest.net/")

    # Click Banner
    elem = driver.find_elements_by_xpath(XPATH_BANNER)
    elem[0].click()
    time.sleep(SHORT_TIME)

    # Click Go
    elem = driver.find_elements_by_xpath(XPATH_GO)
    elem[0].click()
    time.sleep(SHORT_TIME)

    # Wait Results
    def num_there(s):
        return any(i.isdigit() for i in s)
    element = WebDriverWait(driver, LONG_TIME).until(lambda driver : num_there(driver.find_elements_by_xpath(XPATH_UPLOAD)[0].text))
    time.sleep(SHORT_TIME)

    # Get Results
    ping     = driver.find_elements_by_xpath(XPATH_PING)[0].text
    download = driver.find_elements_by_xpath(XPATH_DOWNLOAD)[0].text
    upload   = driver.find_elements_by_xpath(XPATH_UPLOAD)[0].text
    org      = driver.find_elements_by_xpath(XPATH_ORG)[0].text
    sip      = driver.find_elements_by_xpath(XPATH_IP)[0].text

    # Close
    driver.close()
    _ = subprocess.call(KILL_TCPDUMP, shell=True)
    
    return {"ping_ms": ping,
            "download_mbps": download,
            "upload_mbps": upload,
            "organization": org,
            "server_ip": sip}
    
    
