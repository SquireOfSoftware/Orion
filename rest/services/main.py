from resource_locator import resource_locator
#from drone_metadata import drone_metadata
from drone_control import drone_control
#from drone_media import drone_media
from database_access_layer import connector
from mission_reader import mission_reader


drone_control(resource_locator.Instance())

resource_locator.get("drone_control")
