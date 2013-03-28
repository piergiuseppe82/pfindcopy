#Python script to search files by content. 
#Each found file is copied to the destination path, while keeping the original directory structure.
#When done the generated structure is printed as tree
#by piergiuseppe82
#
# import the os.path library
import os
import mmap
import re
import sys
import shutil

pathContent = '/home/piergiuseppe82/projects/java/mywebapp' # Source folder
pattern = re.compile(r'piergiuseppe82[A-Za-z0-9 -]*Defect 12058')#regex pattern to search
pathTarget = '/home/piergiuseppe82/pfindcopy' #Target folder
# The class name
class FindCopy (object):
	
	def run(self):
	    self.findCopy(pathContent,pattern,pathTarget)
	    print '\033[94m'+pathTarget+''
	    self.printContentTree(pathTarget)
	    print '\033[0m'+''
	
	def printContentTree(self, directory,pre=""):
		if os.path.exists(directory):
		    if os.path.isdir(directory):
		        dirFileList = os.listdir(directory)
		        files = list()
		        dirs = list()
		        for filename in dirFileList:
		            if os.path.isdir(os.path.join(directory,filename)):
		            	dirs.append(filename)
		            elif os.path.isfile(os.path.join(directory,filename)):
		                files.append('\033[92m'+pre+"|_"+'\033[95m'+filename+'')
                for d in range(0,len(dirs)):
                	print '\033[92m'+pre+"|_"+'\033[94m'+dirs[d]+''
                	if d < len(dirs) - 1 or len(files) > 0:
	             		self.printContentTree(os.path.join(directory,dirs[d]),pre+"|\t")
	             	else:
	             		self.printContentTree(os.path.join(directory,dirs[d]),pre+"\t")
                for itemFile in files:
                	print itemFile

	def findCopy(self,directory,pattern,target=None):
		if os.path.exists(directory):
			if os.path.isdir(directory):
				dirFileList = os.listdir(directory)
				for filename in dirFileList:
					resource = os.path.join(directory,filename)
					if os.path.isdir(resource):
						if self.supportedDir(resource):
							self.findCopy(resource,pattern,target)
					elif os.path.isfile(resource):
						if self.supportedFile(resource):
							if self.checkPattern(resource,pattern):
								if target:
									self.copyFile(pathContent,directory,filename,target)
								else:
									print resource

	def supportedFile(self,filename):
		supportedExtenstions = [".java",".jsp",".xml",".sqlj",".properties",".js",".css"]#file extension to search
		for ext in supportedExtenstions:
			if filename.endswith(ext):
				return True
		return False

	def supportedDir(self,directory):
		unsupportedDirectories = ["WEB-INF/classes","WEB-INF/lib",".settings"]#directories to esclude
		for unsupportedDir in unsupportedDirectories:
			if directory.endswith(unsupportedDir):
				return False
		return True

	def checkPattern(self,filename,pattern):
		if re.search(pattern, open(filename).read()):
			return True
		return False

	def copyFile(self,basepath,source,filename,targetDir):
		destPart = targetDir+"/"+re.sub(basepath+"/", "", source)
		if not os.path.exists(destPart):
			os.makedirs(destPart)
		shutil.copy2(source+"/"+filename, destPart+"/"+filename)
		#print destPart


if __name__ == '__main__':
    obj = FindCopy()
    obj.run()
