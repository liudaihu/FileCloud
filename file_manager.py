import os
from zipfile import ZipFile

try:
    os.chdir("user_files")
except:
    os.makedirs("user_files")
    os.chdir("user_files")

if "files.zip" in os.listdir():
    os.remove("files.zip")

files = os.listdir()

file_indexes = []
for i in range(len(files)):
    file_indexes.append(i)

archive = ZipFile('files.zip', 'w')

for fl in files:
    archive.write(fl)
archive.close()
