# this file is just for version numbers now, and based on the date the programs get processed

from datetime import datetime

# Get the current date and time
now = datetime.now()
# Format the current date as yyyy.mm.dd
formatted_date = now.strftime("%Y.%m.%d")

WriteR_version = formatted_date

QuartoWriteR_version = formatted_date

ScriptR_version = formatted_date
