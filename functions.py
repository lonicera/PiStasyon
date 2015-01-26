#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging, os, datetime, urllib2, gspread
import sqlite3
import socket, struct, fcntl, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import MySQLdb

def send_mail(subject):
    fromaddr = 'palynology@gmail.com'
    #toaddrs  = 'mustafa.halim.demirci@gmail.com'
    toaddrs  = 'palynology@gmail.com'
    msg = MIMEMultipart()
    username = ''
    password = ''
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    msg['Subject'] = subject
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def sqltogsp():
    db = sqlite3.connect("aeromet.sqlite")
    cursor = db.cursor()
    for i in cursor.execute('''select tarih, sicaklik, nem, basinc, yagis, rhizi, hkalite, isik, K, KB, B, GB, G, GD, D, KD from temp ORDER BY id asc'''):
        gwrite(i)
    #text_formatting(i, 1, 'info')
    #time.sleep(0.5)
    #row = cursor.fetchall()
    cursor.execute('''delete  from temp''')
    db.commit()

    
def sqlin(values):
    db = sqlite3.connect("aeromet.sqlite")
    #tarih = datetime.now()
    #conn = sqlite3.connect('veri.db')
    cursor = db.cursor()
    try:
        cursor.execute('''INSERT INTO temp(tarih, sicaklik, nem, basinc, yagis, rhizi, hkalite, isik, K, KB, B, GB, G, GD, D, KD)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (values))
    except:
        print "Sql Hata"
    db.commit()

def mysqlin(values):
    global offline
    #try:
    mysqldb = MySQLdb.connect(host= "php.beun.edu.tr",
                  user="",
                  passwd="",
                  db="aeroalerjen")
        #tarih = datetime.now()
        #conn = sqlite3.connect('veri.db')
    mysqlcursor = mysqldb.cursor()
    #try:
    mysqlcursor.execute('''INSERT INTO temp(tarih, sicaklik, nem, basinc, yagis, rhizi, hkalite, isik, K, KB, B, GB, G, GD, D, KD)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (values))
    mysqldb.commit()
    mysqldb.close()
    #except:
    #    print "Sql Hata"
    #    
    #    offline = True
    #    sqlin(values)


log_file = 'aero.log'
def text_formatting(source,level, log_level):
    if not os.path.isfile(log_file):
        logging.basicConfig(filename=log_file, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        text_formatting("Günlük dosyası oluşturuldu", 0, 'info')
    elif float(os.path.getsize(log_file))/(1024*1024) > 0.5:
       os.rename(log_file, str(log_file[:-4]) + "_ydk_" + str(datetime.datetime.now().date()) + ".log")
       logging.basicConfig(filename=log_file, format='%(asctime)s:%(levelname)s:%(message)s',  datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
       text_formatting("Log dosyası yedeklendi", 0, 'info')
    logging.basicConfig(filename=log_file, format='%(asctime)s:%(levelname)s:%(message)s',  datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    tab_space = "   "
    for i in range(level):
        source = tab_space + source
    if log_level == "info":
        logging.info(source)   
    elif log_level == "warning":
        logging.warning(source)
    elif log_level == "debug":
        logging.debug(source)
    elif log_level == "error":
        logging.error(source)    
    print(source)

def internet_on():
    try:
        response=urllib2.urlopen('http://www.google.com.tr',timeout=1)
        return True
    #except urllib2.URLError as err: pass
    except:
        #app = Flask(__name__)
        #app.run(host="0.0.0.0", use_reloader=False)
        pass
        return False


def login_open_sheet(email, password, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet."""
	try:
		gc = gspread.login(email, password)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except Exception,e:
		#print 'Unable to login and get spreadsheet.  Check email, password, spreadsheet name.'
                text_formatting("Veritabanı dosyasına ulaşılamadı", 1, 'error')
                text_formatting(str(e), 1, 'error')
                pass
		#sys.exit(1)


def gwrite(values):
    global offline
    global worksheet_temp
    worksheet = None
    GDOCS_EMAIL            = 'palynology@gmail.com'
    GDOCS_PASSWORD         = 'haticem-000-'
    GDOCS_SPREADSHEET_NAME = 'AeroMet'
    if worksheet is None:
        try:
            text_formatting("Gdoca bağlanma denemesi", 1, 'info')
            worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)
            text_formatting("Gdoca bağlandı.", 1, 'info')
            if int(worksheet.row_count) > 50000:
                worksheet.resize(1,3)
        except Exception,e:
            text_formatting("Oturum açılamadı", 1, 'info')
            text_formatting(str(e), 1, 'error')
            offline = True
            sqlin(values)
            pass
            #worksheet_temp = []
    if not worksheet is None:
        try:
            text_formatting("Yeni satır ekleme denemesi", 1, 'info')   
            worksheet.append_row(values)
            text_formatting("Yeni satır eklendi.", 1, 'info')   
            # Wait 30 seconds before continuing
            #print 'Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME)
            #time.sleep(FREQUENCY_SECONDS)
            #worksheet = None
        except Exception,e:
            # Error appending data, most likely because credentials are stale.
            # Null out the worksheet so a login is performed at the top of the loop.
            #print 'Append error, logging in again'
            sqlin(values)
            offline = True
            text_formatting("Veritabanına yeni satır eklenemedi", 1, 'error')
            text_formatting(str(e), 1, 'error')
            #worksheet = None
            pass

