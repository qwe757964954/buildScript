import sys
import os
import getopt
import json
import traceback
from jenkins_ios import JenkinsIOSJob
from jenkins_android import JenkinsAndroidJob
from jenkins_mac import JenkinsMACJob  
from jenkins_web_desktop import JenkinsWebDesktopJob
from jenkins_web_mobile import JenkinsWebMobileJob

class JenkinsJob(object):
    # 构造方法
    def __init__(self, args):
        self.args = args
    def run(self):
        jsonFile = "./pack/jenkins_params.json"
        if self.args[1]:
            jsonFile = self.args[1]
        if os.path.isfile(jsonFile):
            self.jenkins_params = json.load(open(jsonFile, 'r'))
            self.build()
        else:
            print("jenkins_params file not exist")
            exit(0)
    def build(self):
        if not self.jenkins_params:
            print("not jenkins_params")
            exit(1)
        print(self.jenkins_params)
        platform = self.jenkins_params.get("platform")
        if platform == "android":
            self.__build_android()
        elif platform == "ios":
            self.__build_iOS()
        elif platform == "mac":
            self.__build_Mac()
        elif platform == "web-desktop":
            self.__build_web_desktop()
        elif platform == "web-mobile":
            self.__build_web_mobile()
    def __build_android(self):
        print(self.jenkins_params)
        job = JenkinsAndroidJob(self.jenkins_params)
        job.run()
    def __build_Mac(self):
        print(self.jenkins_params)
        job = JenkinsMACJob(self.jenkins_params)
        job.run()
    def __build_iOS(self):
        print(self.jenkins_params)
        job = JenkinsIOSJob(self.jenkins_params)
        job.run()
    def __build_web_desktop(self):
        print(self.jenkins_params)
        job = JenkinsWebDesktopJob(self.jenkins_params)
        job.run()
    def __build_web_mobile(self):
        print(self.jenkins_params)
        job = JenkinsWebMobileJob(self.jenkins_params)
        job.run()

if __name__ == '__main__':
    job = JenkinsJob(sys.argv)
    job.run()