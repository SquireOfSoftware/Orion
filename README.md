# Team Orion
# Sputnik - The Drone Surveying System

How to recreate Sputnik
Dependencies
# General Drone Management System
    Python 2.7 - used by ardrone_autonomy https://www.python.org/download/releases/2.7/ 
      Provides the DMS Django and Mission Reader’s environment language
    Ubuntu 16 for ROS - http://wiki.ros.org/ROS/Installation/ 
      Provides the framework for interacting with the drone
      We used ROS Kinetic’s full install
    Apache 2.7 https://httpd.apache.org/download.cgi#apache24
      Serve static html pages
      Look at httpd.conf to see setup in apache_config
      Static root points to directly into web-gui
      Used redirects to django server on port 5001 for django request forwarding
# Mission Process/Launcher/Executor
    ARDrone autonomy http://ardrone-autonomy.readthedocs.io/en/latest/installation.html 
      Provides the API for interacting with the drone - relies on having ROS installed 
    MySQLDB http://mysql-python.sourceforge.net/MySQLdb.html 
      Provides the API for sending and updating queries to the database
# MySQL Database
    MySQL Workbench https://dev.mysql.com/downloads/workbench/
      Provides easy management and configuration of the database
      Also used to forward engineer the WorkBench database schema file into an SQL file, enabling the insert queries will also insert the relevant lookup table data (such as the drone status table)
      Our setup was localhost:3306 with “root” as the username and “default” as the password
      Refer to Drone_Surveying_System.mwb under db_model folder for full schema and CSV dumps
    MySQL Server https://dev.mysql.com/downloads/mysql/ 
# Front end DMS
    Django https://docs.djangoproject.com/en/1.10/topics/install/ - apt-get or pip2.7
      Provides the REST interactions to the Database
    MySQLClient https://pypi.python.org/pypi/mysqlclient - put on pip2.7
      Builds on top of MySQLDB
      Links very cleanly with Django to form database model objects
# Front end HTML
    Angular JS - https://angularjs.org/ - provides the logic in the front end
      $interval for polling
      $http + services for POST and GET requests - look at dependency injection
      Bootstrap 3 - http://getbootstrap.com/ responsive mobile/desktop designs
        Copied over glyphicons for all the icons (not on the home page)
      Font Awesome http://fontawesome.io/
        Used for the front page
# Drone
    HC-SR04 ultrasonic sensors - detects 2cm to 400cm
    Arduino (full or mini (if using mini you need serial cable)) https://www.arduino.cc/
      Required to write ultrasonic data into a file
    Raspberry Pi https://www.raspberrypi.org/
      Used to communicate with the router and ROS
      ROS also needed to be installed on the raspberry pi
      Shortened cable (USB to USB-A) was selected to power the arduino
      Needs WiFi dongle
    Oliver’s bash script to override server daemon on the drone server (look at ultrasonic_sensor.ino https://github.com/SquireOfSoftware/Orion/blob/develop/onboarddrone/ultrasonic_sensor.ino)
      Modify the drone to automatically connect to our WiFi access point (via SSID) with a set IP address on boot
      https://github.com/AutonomyLab/ardrone_autonomy/wiki/Multiple-AR-Drones 
      1. kill active connections
      2. assign itself ip, ssid drone_net
      Set the ip of drone net to 192.168.1.1, and default gateway (“drone_net”)
      Note that this might need to be “hijacked” on boot (place the script in the bash_rc or on the profile to prevent this from happening) - to prevent drone going into “Access Point” mode, this prevents the drone from going into AP mode and keeps it a “slave to the router”
    A router (please select an appropriate frequency channel 1, 6 or 11 to avoid overlap and interference. UTS WPA runs on 11, we ran our drone wifi successfully on channel 11 or 6)
      Name should be “drone_net”
# Tools used
    Pycharm https://www.jetbrains.com/pycharm/ 
      Note this is free if you are student (You can sign up as a student and get the full version licensed for a year, this is better than the EDU version)
    Webstorm https://www.jetbrains.com/webstorm/?fromMenu 
      Note this is free if you are student
    MySQL Workbench as previously mentioned
    GitHub
      https://github.com/SquireOfSoftware/Orion 

# Other notes
    Gazebo http://gazebosim.org/ is a 3D simluation and modeling program for drones. It was not used due to the extremely low frame rate when run on the provided hardware or in VMs on our own machines.
    Drone weight limit is approximately 180 grams including the full foam hull (speedster hull is approximately 45 grams), any heavier and you will fail to take off (insert video link here)
    Commands - please note that the queue has been set to zero to prevent any “stacking” of commands - if the code has a stack it may build up on ROS if the drone disconnects, we dont want this since the sleep also occurs on the machine as well
      roscore 
        This starts ROS up
      rosrun ardrone_autonomy ardrone_driver -ip XXX.XXX.XXX.XXX
        This launches ARDrone Autonomy
        Note that if you get “Getting Drone Version” then you need to kill the pid of ardrone until it displays something that isn’t “Getting Drone version”
        We assumed our drone was on 192.168.1.10
      rostopic echo ardrone/navdata
        This sets up a subscriber to listen in on the output
      rostopic pub ardrone/takeoff Std_msgs/Empty
        This will issue the land command
        All drone commands, dumps and other pieces are all “callbacks” to the rostopic publishers
      rostopic list
        Lists all the rostopics that you can subscribe or publish to
      rostopic echo /us
        This is the custom ultrasonics package that data was dumped into
      source devel/setup.bash
        Followed by:
        env | grep ROS
            This is to check if the master address is 192.168.1.148
            Otherwise:
        export ROS_MASTER_URI=http://192.168.1.148:11311
            Then:
        rosrun us main
            Sensors 0 to 3 should start being dumped into ROS

# Videos
  https://www.youtube.com/playlist?list=PLFE1soEirSeYSN21s1mMcTJl_1ayu5DAi
