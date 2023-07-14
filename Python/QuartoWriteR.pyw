## N.B. the code used to copy settings files is a purely temporary measure. 
##   Once it is replaced by a more sophisticated way to know which app is running, many of the lines  in this file will be removed.

from FrontEnd  import *


## removals will start here
import os
import shutil

# Delete the existing global settings file
file_to_delete = "GlobalSettings.py"
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"File '{file_to_delete}' has been deleted.")
else:
    print(f"File '{file_to_delete}' does not exist.")

# Copy the right global settings file and rename it to be the default
file_to_copy = "GlobalSettingsQ.py"
new_file_name = "GlobalSettings.py"
shutil.copy(file_to_copy, new_file_name)
print(f"File '{file_to_copy}' has been copied as '{new_file_name}'.")
## removals will end here


# mandatory lines to get program running.
if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    app.MainLoop()
