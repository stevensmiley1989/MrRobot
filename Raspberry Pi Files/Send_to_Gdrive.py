import os
import datetime

#def sync_Gdrive(path):
#    os.system('rclone sync -v {} remote:{}'.format(path,path))
    
#def backup_Gdrive(path):
#    os.system('rclone copy remote:{} remote:backup/{}'.format(path,path))
#path="/home/pi/Desktop/Output/Ball_Pictures"
#path="/home/pi/Desktop/Output/Water_Pictures"
#path="/home/pi/Desktop/Output/Toy_Pictures"
path="/home/pi/Desktop/Output/Toy_Pictures/reindeer/320x320"
#path="/home/pi/Desktop/Output/Toy_Pictures/reindeer/640x640"
def move_Gdrive(path):
    os.system('rclone move {} remote:{}'.format(path,path))
move_Gdrive(path)