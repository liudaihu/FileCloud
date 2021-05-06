import os
from zipfile import ZipFile

try:
    os.chdir("user_files")
except:
    os.makedirs("user_files")

files = os.listdir()

archive = ZipFile('files.zip', 'w')

for fl in files:
    archive.write(fl)
archive.close()
