from selenium import webdriver
import time
from bs4 import BeautifulSoup
import boto3
import os
from shutil import which
import yaml
from sys import platform



def check_browser(use_browser):

    if use_browser == "chrome":

        install_driver(use_browser)
        browser = webdriver.Chrome()

    elif use_browser == "firefox":

        install_driver(use_browser)
        browser = webdriver.Firefox()

    return browser


def install_driver(browser):

    if browser == "chrome":

        check_driver = str(which("chromedriver"))

        if check_driver == "None":

            print('\n' + " chromedriver not found, installing..." + '\n')

            if platform == "linux" or platform == "linux2":
                # linux
                cmd="wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip"
                os.system(cmd)
                cmd="unzip chromedriver_linux64.zip"
                os.system(cmd)
                cmd="chmod +x chromedriver"
                os.system(cmd)
                cmd="mv chromedriver /usr/local/bin"
                os.system(cmd)    
                cmd="rm chromedriver_linux64.zip"
                os.system(cmd)                

            elif platform == "darwin":
                # OS X
                cmd="wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_mac64.zip"
                os.system(cmd)
                cmd="unzip chromedriver_mac64.zip"
                os.system(cmd)            
                cmd="chmod +x chromedriver"
                os.system(cmd)    
                cmd="mv chromedriver /usr/local/bin"
                os.system(cmd)    
                cmd="rm chromedriver_mac64.zip"
                os.system(cmd)



    elif browser == "firefox":

        check_driver = str(which("geckodriver"))

        if check_driver == "None":

            print('\n' + " geckodriver not found, installing..." + '\n')

            if platform == "linux" or platform == "linux2":
                # linux
                os.system("rm geckodriver.log")    
                cmd="wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz"
                os.system(cmd)
                cmd="tar -xvzf geckodriver*"
                os.system(cmd)
                cmd="chmod +x geckodriver"
                os.system(cmd)
                cmd="mv geckodriver /usr/local/bin"
                os.system(cmd)
                cmd="rm geckodriver-v0.24.0-linux64.tar.gz"
                os.system(cmd)

            elif platform == "darwin":
                # OS X
                os.system("rm geckodriver.log")    
                cmd="wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-macos.tar.gz"
                os.system(cmd)
                cmd="tar -xvzf geckodriver*"
                os.system(cmd)
                cmd="chmod +x geckodriver"
                os.system(cmd)
                cmd="mv geckodriver /usr/local/bin"
                os.system(cmd)
                cmd="rm geckodriver-v0.24.0-macos.tar.gz"
                os.system(cmd)
                                

    return browser


def configure_profiles(url, accounts, browser):

    browser.get(url)

    time.sleep(5)
    html_response = browser.page_source

    saml_response = ""

    while saml_response == "":
        time.sleep(5)


        try:
            soup = BeautifulSoup(html_response, 'html.parser')
            saml_response = soup.find('input', {'name': 'SAMLResponse'}).get('value')

        except:
            html_response = browser.page_source
            

    browser.close()

    sts = boto3.client('sts')

    for account in accounts:

        role = account['role_arn']
        principal = account['saml_arn']
        profile = account['aws_profile']
        region = account['aws_region']

        response = sts.assume_role_with_saml(
            RoleArn=role,
            PrincipalArn=principal,
            SAMLAssertion=saml_response
        )

        access_key_id = response['Credentials']['AccessKeyId']
        secret_access_key = response['Credentials']['SecretAccessKey']
        session_token = response['Credentials']['SessionToken']

        cmd="aws configure set aws_access_key_id " + access_key_id + " --profile " + profile
        os.system(cmd)

        cmd="aws configure set aws_secret_access_key " + secret_access_key + " --profile " + profile
        os.system(cmd)

        cmd="aws configure set aws_session_token " + session_token + " --profile " + profile
        os.system(cmd)

        cmd="aws configure set region " + region + " --profile " + profile
        os.system(cmd)

use_browser=""

while use_browser != "chrome" and use_browser != "firefox":
    use_browser = input('\n' + "What browser are you going to use? type \"chrome\" or \"firefox\"" + '\n' + '\n')


organizations = open('organizations.yaml').read()

organizations = yaml.safe_load(organizations)

for organization in organizations['organizations']:

    url = organization['sso_url']

    browser = check_browser(use_browser)

    accounts = organization['accounts']

    configure_profiles(url, accounts, browser)
