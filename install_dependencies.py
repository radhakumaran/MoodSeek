import subprocess
import sys

def install(package):
        print ("Installing ", package)
        subprocess.call(["pip3", "install", "--user", package])
        print (package, " installed.")



install("scipy")
install("nltk")
install("requests")
install("pandas")
install("bs4")
install("scikit-learn")
install("watson_developer_cloud")
install("textblob")
install("matplotlib")
install("tweepy")
install("flask")
