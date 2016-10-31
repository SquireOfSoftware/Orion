import mysql.connector
import cv2
import base64
import numpy as np
import sys
from datetime import datetime, date, time
from mysql.connector import errorcode


dbconfig = {  "database" : "Drone_Surveying_System",
              "user"     : "root",
              "password" : "default"}

def test_image():
    img = cv2.imread('test.png')[1]
    img_str = cv2.imencode('.png', img)[1]
    b64 = base64.b64encode(img_str)
    print(b64)
    print(type(b64))
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor(prepared=True)
    now = datetime.now()
    print now
    sql = u"INSERT INTO Image (ImageTimestamp, ImageBlob, Mission_MissionID) VALUES (%s, %s, 3);"
    try:
        cursor.execute(sql, (now.strftime('%Y-%m-%d %H:%M:%S'),b64))
        print now
    except mysql.connector.Error as e:
        print e.msg
    cursor.close()
    cnx.close()

def open_image():
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor(prepared=True)
    sql = "SELECT ImageBlob from Image WHERE ImageID = 1;"

    cursor.execute(sql)
    row = cursor.fetchone()
    print(row)
    img = base64.b64decode(row[0])
    print(img)
    arr = np.fromstring(img, np.uint8)
    cv2.imshow('Image', arr)
    cv2.waitKey(0)

    cursor.close()
    cnx.close()

test_image()
open_image()
