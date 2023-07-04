import os
import json
import subprocess
import shlex

class JenkinsAndroidJob(object):
    def __init__(self, args):
        super(JenkinsAndroidJob, self).__init__()
        self.jenkins_params = args

    def __create_android_project(self):
        project_path = self.jenkins_params.get("project_path")
        platform = self.jenkins_params.get("platform")
        env_vars = {'LC_ALL': 'en_US.UTF-8','LANG': 'en_US.UTF-8','LANGUAGE': 'en_US.UTF-8'}
        os.chdir(f"{project_path}/pack")
        COCOS_CREATOR=os.environ.get('COCOS_CREATOR')
        cmd = f'{COCOS_CREATOR} --project {project_path} --build "configPath=buildConfig_{platform}.json"'
        print(cmd)
        subprocess.run(cmd, shell=True, check=True,env=env_vars)
        

    def __build_apk(self):
        PROJECT_PATH = self.jenkins_params.get("project_path")
        os.chdir(PROJECT_PATH + "/build/android/proj")
        cmd = f"chmod 777 gradlew"
        subprocess.run(shlex.split(cmd), check=True)
        cmd = f"./gradlew clean && ./gradlew 266:buildEnv && ./gradlew assembleBoyaaPluginDebug && ./gradlew --no-daemon assembleRelease --stacktrace"
        subprocess.run(shlex.split(cmd), check=True)
    def run(self):
        jsonFile = "./pack/buildConfig_android.json"
        if os.path.isfile(jsonFile):
            self.buildConfig_params = json.load(open(jsonFile, 'r'))
        else:
            print("buildConfig_ios file not exist")
            exit(0)

        self.__create_android_project()
        print("create build android project finish")
        self.__build_apk()
        print("build android apk finish")
