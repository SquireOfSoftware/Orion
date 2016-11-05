from PIL import Image
from StringIO import StringIO
import mysql.connector
import cv2
import base64
import numpy as np
import sys
from datetime import datetime, date, time
from mysql.connector import errorcode


dbconfig = {  "database" : "Drone_Surveying_System",
              "user"     : "root",
              "password" : "default",
              "use_unicode" : "False" }

def test_image():
    img = cv2.imread('test.png')
    print(img)
    print(type(img))
    img_str = cv2.imencode('.png', img)[1:]
    b64 = base64.b64encode(img_str)
    b64 = open('test.png').read().decode('latin-1').encode('utf-8')
    b64 = open('test.png').read().decode('utf-8')
    cnx = mysql.connector.connect(**dbconfig)
    cnx.start_transaction(isolation_level='READ COMMITTED')
    cursor = cnx.cursor(prepared=True)
    now = datetime.now()
    print now
    sql = "INSERT INTO Image (ImageTimestamp, ImageBlob, Mission_MissionID) VALUES (%s, %s, %s);"
    try:
        data = (now.strftime("%Y-%m-%d %H:%M:%S"), b64, 3)
        cursor.execute(sql, data)
        print now
    except mysql.connector.Error as e:
        print e.msg
    cnx.commit()
    cursor.close()
    cnx.close()

def open_image():
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor(prepared=True)
    sql = "SELECT ImageBlob from Image ORDER BY ImageID DESC LIMIT 1;"
    cursor.execute(sql)
    for row in cursor:
        str_img = row[0];

    fh = open("hopeful.png", "wb")
    fh.write(str_img.decode('base64'))
    fh.close()
#    print(type(str_img))
#    print str_img
#    sbuf = StringIO()
#    sbuf.write((str_img.decode('base64')))
#    pimg = Image.open(sbuf)
#    newimg = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)


#    cv2.imshow("img",newimg)
#    cv2.waitKey()
    cursor.close()
    cnx.close()

