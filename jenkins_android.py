import os
import json
import subprocess
import shlex
import shutil
from pathlib import Path
from datetime import datetime, timedelta, timezone

 #替换字符串
def replace_project_pbxproj(filepath, key_string, value_string):
    if key_string is None or value_string is None:
        raise TypeError

    content = ""
    f1 = open(filepath, "rb")
    for line in f1:
        strline = line.decode('utf8')
        if key_string in strline:
            str_arr = strline.split(key_string)
            new_line_str = str_arr[0] + key_string + " " + value_string + "\n"
            content += new_line_str
        else:
            content += strline
    f1.close()
    f2 = open(filepath, "wb")
    f2.write(content.encode('utf8'))
    f2.close()

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
        cmd = f'{COCOS_CREATOR}  --project {project_path} --build "configPath=buildConfig_{platform}.json"'
        print(cmd)
        subprocess.run(shlex.split(cmd),env=env_vars)
        

    def __build_apk(self):
        PROJECT_PATH = self.jenkins_params.get("project_path")
        ANDROID_PRO_PATH = f"{PROJECT_PATH}/build/android/proj"
        os.chdir(ANDROID_PRO_PATH)
        BUILD_TYPE = "Release"
        tz_utc_8 = timezone(timedelta(hours=8))
        date_str = datetime.utcnow().replace(tzinfo=tz_utc_8).strftime("%Y-%m-%d-%H-%M-%S")
        output_apk = f"{ANDROID_PRO_PATH}/build/266/outputs/apk/boyaaPlugin/{BUILD_TYPE}/266-boyaaPlugin-{BUILD_TYPE}.apk"
        output_file= f"{PROJECT_PATH}/pack/{date_str}"

        
        cmd = f"chmod 777 gradlew"
        subprocess.run(shlex.split(cmd), check=True)
        build_cmd = f"./gradlew clean"
        subprocess.run(shlex.split(build_cmd), check=True)
        build_cmd = f"./gradlew 266:buildEnvironment"
        subprocess.run(shlex.split(build_cmd), check=True)
        build_cmd = f"./gradlew --no-daemon assembleBoyaaPlugin{BUILD_TYPE.capitalize()}"
        subprocess.run(shlex.split(build_cmd), check=True)

        Path(output_file).mkdir(parents=True, exist_ok=True)
        shutil.move(output_apk, output_file)

        # cmd = f"./gradlew clean && ./gradlew 266:buildEnv && ./gradlew assembleBoyaaPluginDebug && ./gradlew --no-daemon assembleRelease --stacktrace"
        # subprocess.run(shlex.split(build_cmd), check=True)
    def __modify_android_version(self):
        project_path = self.jenkins_params.get("project_path")
        version_path = os.path.join(project_path, f"native/engine/android/app/version.properties")
        BUILD_VERSION = self.jenkins_params.get("buildVer")
        VERSION = self.jenkins_params.get("version")

        replace_project_pbxproj(version_path,"version.name=",f"{VERSION}")
        replace_project_pbxproj(version_path,"version.code=",f"{BUILD_VERSION}")

    def run(self):
        jsonFile = "./pack/buildConfig_android.json"
        if os.path.isfile(jsonFile):
            self.buildConfig_params = json.load(open(jsonFile, 'r'))
        else:
            print("buildConfig_ios file not exist")
            exit(0)
        self.__modify_android_version()
        print("modify android version finish")
        self.__create_android_project()
        print("create build android project finish")
        self.__build_apk()
        print("build android apk finish")
