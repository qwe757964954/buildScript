source ~/.bash_profile

source ~/.zshrc

ARGS=("$@")

$COCOS_CREATOR --project ${ARGS[0]} --build "configPath=buildConfig_${ARGS[1]}.json"

echo "\032[35m;============COCOS_CREATOR ${ARGS[1]} SUCCESS============"