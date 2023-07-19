import os
import json
import subprocess
import shlex
import plistlib
import shutil
from datetime import datetime, timedelta, timezone
class JenkinsWebDesktopJob(object):
    def __init__(self, args):
        super(JenkinsWebDesktopJob, self).__init__()
        self.jenkins_params = args

    def __create_web_desktop_project(self):
        project_path = self.jenkins_params.get("project_path")
        platform = self.jenkins_params.get("platform")
        env_vars = {'LC_ALL': 'en_US.UTF-8','LANG': 'en_US.UTF-8','LANGUAGE': 'en_US.UTF-8'}
        os.chdir(f"{project_path}/pack")
        COCOS_CREATOR=os.environ.get('COCOS_CREATOR')
        cmd = f'{COCOS_CREATOR}  --project {project_path} --build "configPath=buildConfig_{platform}.json"'
        print(cmd)
        subprocess.run(shlex.split(cmd),env=env_vars)

    def __build_web_desktop(self):
        print("run ios Pod install")
        project_path = self.jenkins_params.get("project_path")
        target_folder = f"{project_path}/build/web-desktop"
        source_folder = f"{project_path}/pack/web-desktop"
        # 删除目标文件夹中的所有内容
        shutil.rmtree(target_folder)
        
        # 将源文件夹复制到目标文件夹
        shutil.copytree(source_folder, target_folder)

    def run(self):
        jsonFile = "./pack/buildConfig_web-desktop.json"
        if os.path.isfile(jsonFile):
            self.buildConfig_params = json.load(open(jsonFile, 'r'))
        else:
            print("buildConfig_ios file not exist")
            exit(0)
        self.__create_web_desktop_project()
        print("create ios project finish")
        self.__build_web_desktop()
        print("build web desktop finish")