import os
import json
import subprocess
import shlex
import plistlib
class JenkinsIOSJob(object):
    def __init__(self, args):
        super(JenkinsIOSJob, self).__init__()
        self.jenkins_params = args

    def __create_ios_project(self):
        project_path = self.jenkins_params.get("project_path")
        platform = self.jenkins_params.get("platform")
        cmd = f"$COCOS_CREATOR --project {project_path} --build configPath=buildConfig_${platform}.json"
        subprocess.run(shlex.split(cmd), check=True)

    def __archive_ipa(self):
        print("run ios Pod install")
        PROJECT_PATH = self.jenkins_params.get("project_path")
        os.chdir(PROJECT_PATH + "/build/ios/proj")
        cmd = f"pod install --repo-update"
        subprocess.run(shlex.split(cmd), check=True)
        BUILD_TYPE = "Release"
        SCHEME_NAME="266"
        WORKSPACE_PATH= f"{PROJECT_PATH}/SCHEME_NAME.xcworkspace"
        PRODUCT_PATH= f"{PROJECT_PATH}/pack/pack"
        ARCHIVE_PATH= f"{PRODUCT_PATH}/{SCHEME_NAME}.xcarchive"
        EXPORTOPTIONSPLIST_PATH= f"{PROJECT_PATH}/pack/ExportOptions.plist"
        cmd = f"xcodebuild clean -workspace ${WORKSPACE_PATH} -scheme ${SCHEME_NAME} -configuration ${BUILD_TYPE} || exit"
        subprocess.run(shlex.split(cmd), check=True)
        cmd = f"xcodebuild -project 266.xcodeproj -target plugin_registry -configuration {BUILD_TYPE}"
        subprocess.run(shlex.split(cmd), check=True)
        cmd = f"xcodebuild archive -workspace ${WORKSPACE_PATH} -scheme ${SCHEME_NAME} -archivePath ${ARCHIVE_PATH} -quiet || exit"
        subprocess.run(shlex.split(cmd), check=True)
        cmd = f"xcodebuild -exportArchive -archivePath $ARCHIVE_PATH -exportPath ${PRODUCT_PATH} -exportOptionsPlist ${EXPORTOPTIONSPLIST_PATH} -quiet || exit"
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
        self.__archive_ipa()
        print("archive ipa finish")