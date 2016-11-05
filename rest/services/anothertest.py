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
    print(type(str_img))
    print str_img
    img = str_img.decode("utf-8")
#    print(str_img.decode("utf-8"))
    #print(img)
# Use matt's stuff
    arr = np.fromstring(img, np.uint8)
    fin_img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    print tuple(fin_img.shape[1::-1])
    cv2.imwrite('outertest.png', fin_img)
    cursor.close()
    cnx.close()

