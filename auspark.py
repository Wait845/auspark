import requests
import re
import getpass
import time
from bs4 import BeautifulSoup

#GET USER'S ID AND PSW
print("LOGIN IN ......")
StudentId = input("Id:")
StudentPsw = getpass.getpass("Password:")

if StudentId == "" or StudentPsw == "":
    print("Infomation does'nt enough")
    exit()

#LOGIN TO AUSPARK WEBSITE
session = requests.session()
getTokenUrl = "https://auspark.au.edu"
html_str = session.get(getTokenUrl)
html_str = html_str.text
token = re.findall(r"<input name=__RequestVerificationToken type=hidden value=(.*)></form>",html_str)[0] #get token from main page for login

getCookieUrl = "https://auspark.au.edu/Account/Login?returnurl=/"
data = {
    "Username":StudentId,
    "Password":StudentPsw,
    "__RequestVerificationToken":token
}
html_str = session.post(getCookieUrl, data) #post to target url with username, password, and token to login then return information.
infomationPage = html_str.text


#START ANALYSIS THE MAIN PAGE'S CODE
soup = BeautifulSoup(infomationPage, "html.parser")

#TEST IF THE PASSWORD RIGHT
for tag in soup.find_all("form"):
    if tag.get("action") == "/Account/Login?returnurl=%2F":
        print("Your Password Is Wrong!")
        exit()


print("")
print("")
for tag in soup.find_all("div"):
    #GET USER'S FULL NAME
    if tag.get("class") ==  ['d-block', 'align-self-center']:
        info = tag.find_all("h4")
        firstName = info[0].text
        lastName = info[1].text
        print("Hello {} {}".format(firstName, lastName))

    #GET USER'S MAJOR
    if tag.get("class") == ['media-body', 'align-self-center']:
        major = tag.h4.text
        faculty = tag.div.span.text
        print("From {} | {}".format(major, faculty))

    #GET USER'S CREDIT
    if tag.get("class") == ['profile-box__basic-info', 'mx-2']:
        info = tag.find_all("div")
        #pattern = r"[0-9]{7}"
        #studentId = re.findall(pattern, info[0].p.text)[0]

        pattern = r"[0-4]{1}.[0-9]{2}"
        gpa = re.findall(pattern, info[1].p.text)[0]

        pattern = r"[0-9]{1,3}"
        credit = re.findall(pattern, info[2].p.text)[0]
        
        print("Your GPA {}, Credit {}".format(gpa, credit))
        print("")
        print("")
        break
