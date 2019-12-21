import sys;
import HelperModule as HM;
from urllib import request

import schedule;
import time;

def isConnected():
    try:
        request.urlopen('http://216.58.192.142')
        return True
    except:
        return False

def errormsg():
	print("First write valid emailid and password in 'sendmail()' of 'HelperModule' and your account should have permission for 'Less secure app access'")
	print("Right way to give cmdline arguments is below:")
	print("python3   python-script-name.py    Absolute-directory-name    numassign13ber-of-time-interval-in-Minutes   valid-email-address_of_sender")
	print("thats it..press enter...thank you")

def jodtoschedule(emailid,abspath):
	foi = HM.DuplicateFileRemoval(abspath)

	if isConnected():
		if not HM.sendMail(foi, emailid):
			exit(-1)
	else:
		exit(-1)


def main():

	if sys.argv[1] and sys.argv[2] and sys.argv[3]:
		if not HM.isValidEmail(sys.argv[3]) or not HM.isNumber(sys.argv[2]) or not HM.isAbsolutePath(sys.argv[1]):
			print("Invalid Command Line Argument")
			exit(-1)
	else:
		errormsg()
		exit(-1)

	schedule.every(int(sys.argv[2])).minutes.do(jodtoschedule,sys.argv[3],sys.argv[1])
	while True:
		schedule.run_pending()
		time.sleep(1)
    



if __name__ == "__main__":
    main();
