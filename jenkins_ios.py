import os
import json
import subprocess
import shlex
import plistlib
import shutil
from datetime import datetime, timedelta, timezone


class JenkinsIOSJob(object):
    def __init__(self, args):
        super(JenkinsIOSJob, self).__init__()
        self.jenkins_params = args

    def __create_ios_project(self):
        project_path = self.jenkins_params.get("project_path")
        platform = self.jenkins_params.get("platform")
        env_vars = {'LC_ALL': 'en_US.UTF-8','LANG': 'en_US.UTF-8','LANGUAGE': 'en_US.UTF-8'}
        os.chdir(f"{project_path}/pack")
        COCOS_CREATOR=os.environ.get('COCOS_CREATOR')
        cmd = f'{COCOS_CREATOR}  --project {project_path} --build "configPath=buildConfig_{platform}.json"'
        print(cmd)
        subprocess.run(shlex.split(cmd),env=env_vars)

    def __archive_ipa(self):
        print("run ios Pod install")
        PROJECT_PATH = self.jenkins_params.get("project_path")
        os.chdir(PROJECT_PATH + "/build/ios/proj")

        tz_utc_8 = timezone(timedelta(hours=8))
        date_str = datetime.utcnow().replace(tzinfo=tz_utc_8).strftime("%Y-%m-%d-%H-%M-%S")

        cmd = f"pod install --repo-update"
        subprocess.run(shlex.split(cmd), check=True)
        BUILD_TYPE = "Release"
        SCHEME_NAME="266"
        WORKSPACE_PATH= f"{PROJECT_PATH}/build/ios/proj/{SCHEME_NAME}.xcworkspace"
        PRODUCT_PATH= f"{PROJECT_PATH}/pack/{date_str}"
        ARCHIVE_PATH= f"{PRODUCT_PATH}/{SCHEME_NAME}.xcarchive"
        EXPORTOPTIONSPLIST_PATH= f"{PROJECT_PATH}/pack/ExportOptions.plist"
        # if os.path.exists(PRODUCT_PATH):
        #     print("文件夹存在")
        #     shutil.rmtree(PRODUCT_PATH)
        
        cmd = f"xcodebuild clean -workspace {WORKSPACE_PATH} -scheme {SCHEME_NAME} -configuration {BUILD_TYPE}"
        subprocess.run(shlex.split(cmd), check=True)
        cmd = f"xcodebuild -project 266.xcodeproj -target plugin_registry -configuration {BUILD_TYPE}"
        subprocess.run(shlex.split(cmd), check=True)
        cmd = f"xcodebuild archive -workspace {WORKSPACE_PATH} -scheme {SCHEME_NAME} -archivePath {ARCHIVE_PATH}"
        subprocess.run(shlex.split(cmd), check=True)
        cmd = f"xcodebuild -exportArchive -archivePath {ARCHIVE_PATH} -exportPath {PRODUCT_PATH} -exportOptionsPlist {EXPORTOPTIONSPLIST_PATH}"
        subprocess.run(shlex.split(cmd), check=True)
    
    def __setup_info_plist__(self):
        PROJECT_PATH = self.jenkins_params.get("project_path")
        BUILD_VERSION = self.jenkins_params.get("buildVer")
        VERSION = self.jenkins_params.get("version")
        file = f"{PROJECT_PATH}/native/engine/ios/Info.plist"
        print(f"__setup_info_plist__, file:{file}")
        fp = open(file=file, mode='rb+')
        info_dict = plistlib.load(fp=fp)
        info_dict["CFBundleShortVersionString"] = VERSION
        info_dict["CFBundleVersion"] = f"{VERSION}.{BUILD_VERSION}"
        fp.seek(0)
        plistlib.dump(info_dict, fp)
        fp.truncate()
        fp.close()
        pass
    
    def __copy_ios_xcodeproj(self):
        PROJECT_PATH = self.jenkins_params.get("project_path")
        # 源文件夹路径
        source_folder = f"{PROJECT_PATH}/native/engine/ios/266.xcodeproj"

        # 目标文件夹路径
        destination_folder = f"{PROJECT_PATH}/build/ios/proj/266.xcodeproj"

        # 拷贝文件夹
        shutil.copytree(source_folder, destination_folder)

    def run(self):
        jsonFile = "./pack/buildConfig_ios.json"
        if os.path.isfile(jsonFile):
            self.buildConfig_params = json.load(open(jsonFile, 'r'))
        else:
            print("buildConfig_ios file not exist")
            exit(0)
        self.__setup_info_plist__()
        print("setip info plist ")
        self.__create_ios_project()
        print("create ios project finish")
        self.__copy_ios_xcodeproj()
        print("copy ios project finish")
        self.__archive_ipa()
        print("archive ipa finish")