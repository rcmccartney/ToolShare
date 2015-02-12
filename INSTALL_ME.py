import os
import subprocess
import pip

def install(package):
    pip.main(['install', package])

def main():
	with open('requirements.txt') as f:
		for line in f:
			install(line.strip())
	#subprocess.call(["python", "django-grappelli-stable-2.5.x"+os.sep+"setup.py", "install"], shell=False)
	#subprocess.call(["python", "django-registration-1.0"+os.sep+"setup.py", "install"], shell=False)

if __name__ == "__main__":
	main()