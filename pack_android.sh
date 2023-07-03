#!/bin/sh

#android打包脚本
source ~/.bash_profile

ARGS=("$@")
TOOLS_PATH=$(dirname "$PWD")
## 项目根路径，android所在路径
PROJECT_ROOT_PATH=$TOOLS_PATH/build/android/proj

## 打包生成路径
PRODUCT_PATH=$PROJECT_ROOT_PATH/build/266
# 删除pack文件夹，可根据各自情况选择是否保留 
rm -rf ${PRODUCT_PATH}

cd $PROJECT_ROOT_PATH

chmod 777 gradlew

./gradlew clean && ./gradlew 266:buildEnv && ./gradlew assembleBoyaaPluginDebug && ./gradlew --no-daemon assembleRelease --stacktrace

APK_PATH=$PRODUCT_PATH/outputs/apk/dev/release/266-dev-release.apk

if [ -e ${APK_PATH} ];
    then
    echo "\032[35m;============Export APK SUCCESS============"
    # open ${IPA_PATH}
    else
    echo "\033[31m;============Export APK FAIL============"
fi
echo "\033[36;1m使用GRADLE打包总用时: ${SECONDS}s"
echo "$APK_PATH"
ANDROID_CHANEL="qsdkandroid"

cd $TOOLS_PATH/pack
python3 upload.py -p $APK_PATH -n $ANDROID_CHANEL -v ${ARGS[0]} -l ${ARGS[1]}

echo "\033[32m;${POST_UPLOAD_RESULT}"
echo "\033[32m;============POST PACK END============"

