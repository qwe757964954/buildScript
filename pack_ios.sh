#!/bin/sh

# 注意事项
# 1、如果提示permission denied: ./package.sh ， 则先附加权限，命令如下：chmod 777 package.sh
# 2、请根据自己项目的情况选择使用 workspace 还是 project 形式，目前默认为 workspace 形式

### 需要根据自己项目的情况进行修改，XXX都是需要进行修改的，可搜索进行修改 ###

# 注释内容块
# Project名称
ARGS=("$@")
PROJECT_NAME="266"

## Scheme名
SCHEME_NAME="266"

## 编译类型 Debug/Release二选一
BUILD_TYPE="Release"

TOOLS_PATH=$(dirname "$PWD")
## 项目根路径，xcodeproj/xcworkspace所在路径
PROJECT_ROOT_PATH=$TOOLS_PATH/build/ios/proj

## 打包生成路径
PRODUCT_PATH=$TOOLS_PATH/pack/pack
# 删除pack文件夹，可根据各自情况选择是否保留 
rm -rf ${PRODUCT_PATH}


## ExportOptions.plist文件的存放路径，该文件描述了导出ipa文件所需要的配置
## 如果不知道如何配置该plist，可直接使用xcode打包ipa结果文件夹的ExportOptions.plist文件
EXPORTOPTIONSPLIST_PATH=${TOOLS_PATH}/pack/ExportOptions.plist

# exec > $TOOLS_PATH//tools/temp/pack_log.out 2>&1

echo "\033[32m;PROJECT_ROOT_PATH=$PROJECT_ROOT_PATH"
echo "\033[32m;PRODUCT_PATH=$PRODUCT_PATH"
echo "\033[32m;EXPORTOPTIONSPLIST_PATH=$EXPORTOPTIONSPLIST_PATH"

## workspace路径
WORKSPACE_PATH=${PROJECT_ROOT_PATH}/${PROJECT_NAME}.xcworkspace

## project路径
PROJECT_PATH=${PROJECT_ROOT_PATH}/${PROJECT_NAME}.xcodeproj

### 编译打包过程 ###

echo "\033[35m;============Build Clean Begin============"

## 清理缓存

## project形式
# xcodebuild clean -project ${PROJECT_PATH} -scheme ${SCHEME_NAME} -configuration ${BUILD_TYPE} || exit

## workspace形式
# xcodebuild clean -workspace ${WORKSPACE_PATH} -scheme ${SCHEME_NAME} -configuration ${BUILD_TYPE} || exit

echo "\033[32m;============Build Clean End============"

#获取Version
VERSION_NUMBER=`sed -n '/MARKETING_VERSION = /{s/MARKETING_VERSION = //;s/;//;s/^[[:space:]]*//;p;q;}' ${PROJECT_PATH}/project.pbxproj`
# 获取build
BUILD_NUMBER=`sed -n '/CURRENT_PROJECT_VERSION = /{s/CURRENT_PROJECT_VERSION = //;s/;//;s/^[[:space:]]*//;p;q;}' ${PROJECT_PATH}/project.pbxproj`

## 编译开始时间,注意不可以使用标点符号和空格
BUILD_START_DATE="$(date +'%Y-%m-%d_%H-%M')"

## IPA所在目录路径
IPA_DIR_NAME=${VERSION_NUMBER}_${BUILD_NUMBER}_${BUILD_START_DATE}

##xcarchive文件的存放路径
ARCHIVE_PATH=${PRODUCT_PATH}/${SCHEME_NAME}.xcarchive
## ipa文件的存放路径
IPA_PATH=${PRODUCT_PATH}

# 解锁钥匙串 -p后跟为电脑密码
security unlock-keychain -p xing

echo  "\033[33m;============Build Archive Begin============"
##进入工程
cd ${PROJECT_ROOT_PATH}
## project形式

# xcodebuild -workspace ${PROJECT_NAME}.xcworkspace -scheme plugin_registry -configuration Release
xcodebuild -project 266.xcodeproj -target plugin_registry -configuration Release
# xcodebuild archive -project ${PROJECT_PATH} -scheme ${SCHEME_NAME} -archivePath ${ARCHIVE_PATH}
## workspace形式
xcodebuild archive -workspace ${WORKSPACE_PATH} -scheme ${SCHEME_NAME} -archivePath ${ARCHIVE_PATH} -quiet || exit

echo "\032[35m;============Build Archive Success============"


echo "\033[35m;============Export IPA Begin============"

xcodebuild -exportArchive -archivePath $ARCHIVE_PATH -exportPath ${IPA_PATH} -exportOptionsPlist ${EXPORTOPTIONSPLIST_PATH} -quiet || exit

echo ${IPA_PATH}/${PROJECT_NAME}.ipa

if [ -e ${IPA_PATH}/${PROJECT_NAME}.ipa ];
    then
    echo "\032[35m;============Export IPA SUCCESS============"
    # open ${IPA_PATH}
    else
    echo "\033[31m;============Export IPA FAIL============"
fi
echo "\033[36;1m使用AutoPackageScript打包总用时: ${SECONDS}s"


### 上传过程 ###

## 上传app store

# 验证
# xcrun altool --validate-app -f ${IPA_PATH}/${SCHEME_NAME}.ipa -t ios --apiKey xxx --apiIssuer xxx --verbose

# 上传
# xcrun altool --upload-app -f ${IPA_PATH}/${SCHEME_NAME}.ipa -t ios --apiKey xxx --apiIssuer xxx --verbose

## 上传到公网测试
echo "\033[35m;============Upload PGYER Begin============"
IOS_CHANEL="qsdkios"
cd $TOOLS_PATH/pack
python3 upload.py -p ${IPA_PATH}/${PROJECT_NAME}.ipa -n $IOS_CHANEL -v ${ARGS[0]} -l ${ARGS[1]}

