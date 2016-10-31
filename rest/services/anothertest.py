import mysql.connector
import cv2
import base64
import numpy as np
from datetime import datetime, date, time
from mysql.connector import errorcode


dbconfig = {  "database" : "Drone_Surveying_System",
              "user"     : "root",
              "password" : "default" }

def test_image():
    img = cv2.imread('test.png')[1]
    img_str = cv2.imencode('.png', img)[1]
    b64 = base64.encodestring(img_str)
    print b64
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor(prepared=True)
    now = datetime.now()
    print now
    sql = "INSERT INTO Image (ImageTimestamp, ImageBlob, Mission_MissionID) VALUES (%s, %s, 3);"
    cursor.execute(sql, (now.strftime('%Y-%m-%d %H:%M:%S'),b64))

    cursor.close()
    cnx.close()

def open_image():
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor(prepared=True)
    sql = "SELECT ImageBlob from Image WHERE ImageID = 1;"

    cursor.execute(sql)
    row = cursor.fetchone()
    img = base64.decodestring(row[0])
    arr = np.fromstring(img, np.uint8)
    cv2.imshow('Image', arr)
    cv2.waitKey(0)

    cursor.close()
    cnx.close()
