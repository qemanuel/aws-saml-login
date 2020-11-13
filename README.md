# aws-saml-login
## wizard for assume multimple aws roles by saml from multiple SSO

### prerequisites
* Python3
* Pip3
* awscli
* only for linux or macos

### How to use it

* git clone -b v1.0.0 git@github.com:qemanuel/aws-saml-login.git
* cd aws-saml-login
* edit the organizations.yaml with the desired values. You have to define: sso url, arn role, arn of the saml identity provider, profile name and default region
* pip3 install -r requirements.txt
* python3 main.py
* select chrome or firefox, the wizard will be check if you already have chromedriver or geckodriver (firefox) and if not, will be download it and move it to /usr/local/bin
* the wizard will open the sso url and wait for you complete the login, then will capture the SAML Response and create the aws profiles
* thats all ! you already have your profiles in $HOME/.aws/credentials and $HOME/.aws/config
