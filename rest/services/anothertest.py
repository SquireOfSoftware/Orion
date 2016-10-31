import mysql.connector
import cv2
import base64
from mysql.connector import errorcode


dbconfig = {  "database" : "Drone_Surveying_System",
              "user"     : "root",
              "password" : "default" }

def test_image():
    img = cv2.imread('test.png')
    img_str = cv2.imencode('.png', img)[1]
    b64 = base64.encodestring(img)
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor(prepared=True)
    sql = "INSERT INTO Image (ImageTimestamp, ImageFilepath, Mission_MissionID) VALUES (%s, %s, 1);"
    cursor.execute(sql, (img_str))

    cursor.close()
    cnx.close()
