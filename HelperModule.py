import re;
import os;
import time;
import hashlib;
import smtplib;
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class FileOperationInfo:
    def __init__(self):
        self.StartTime = 0.0;
        self.EndTime = 0.0;
        self.TotalTime = 0.0;
        self.TotalFileNumber=0;
        self.DuplicateFileNumber=0;
        self.LogFile=str

def isValidEmail(emailid):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return (re.search(regex, emailid))

def isNumber(n):
    return n.isnumeric()

def isAbsolutePath(path):
    return os.path.isabs(path) and os.path.exists(path)


def DuplicateFileRemoval(path):

    FOI=FileOperationInfo();
    tfn=0
    dfn=0
    data={}
    line = "~" * 80;

    Startsec=time.time()
    if not os.path.exists("LogFolder"):
        os.mkdir("LogFolder")
    filename=os.path.join("LogFolder", "log_%s.txt" % time.ctime());
    f=open(filename, 'w');
    for Folder, Subfolder, Files in os.walk(path):
        for name in Files:
            tfn+=1
            name = os.path.join(Folder, name);
            checksum = Checksum(name);
            if checksum in data:
                dfn+=1
                f.write(line + "\n");
                f.write(str(name) + "->"+str(checksum) + "\n")
                f.write(line + "\n");
                data[checksum].append(name);
                os.remove(name)
            else:
                data[checksum] = [name];

    Endsec=time.time()
    FOI.StartTime =time.ctime(Startsec)
    FOI.EndTime=time.ctime(Endsec)
    FOI.TotalTime=Startsec-Endsec
    FOI.TotalFileNumber=tfn
    FOI.DuplicateFileNumber=dfn
    FOI.LogFile=filename
    return FOI;




def Checksum(path,blocksize=1024):
    fd=open(path,'rb')
    hasher=hashlib.md5()
    buf=fd.read(blocksize)

    while len(buf)>0:
        hasher.update(buf)
        buf=fd.read(blocksize)

    fd.close()

    return hasher.hexdigest()


def sendMail(foi:FileOperationInfo,toaddr):
    fromaddr="Valid email ID"
    password="Valid password"

    try:
        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Log file of duplicate file removal"
        body = """
        hello %s,
        Duplicate file are %s,
        total file scanned are %s,
        Operation started at: %s,
        Operation finished at: %s,
        total time required to complete is: %s.
        Thank you ;-)
        """%(toaddr,foi.DuplicateFileNumber,foi.TotalFileNumber,foi.StartTime,foi.EndTime,foi.TotalTime)
        msg.attach(MIMEText(body, 'plain'))

        
        attachment = open(str(foi.LogFile),'rb')

        p = MIMEBase('application', 'octet-stream')
        
        p.set_payload(attachment.read())

        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % foi.LogFile)
        msg.attach(p)
          
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        

        s.login(fromaddr, password)

        text = msg.as_string()
        
        s.sendmail(fromaddr, toaddr, text)

        s.quit()
        return True

    except:
        print("in exception of sending mail")
        return False


