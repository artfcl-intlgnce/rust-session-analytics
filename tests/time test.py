import datetime

bmtime = datetime.datetime.now().replace(microsecond=0).isoformat()
bmtime = str(bmtime) + "Z"
print(str(bmtime))