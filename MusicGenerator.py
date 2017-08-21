import urllib.request
import zipfile
import nottingham_util


print("music generator....")



url = "http://www-etud.iro.umontreal.ca/~boulanni/Nottingham.zip"

urllib.request.urlretrieve(url, "dataset.zip")
#urllib.urlretrieve(url,"dataset.zip")

zip = zipfile.ZipFile(r"dataset.zip")
zip.extractall('data')

