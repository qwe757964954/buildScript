ARGS=("$@")

if [ ${ARGS[0]} = "ios" ]; then
    echo 'build ios'
    sh ./pack_ios.sh ${ARGS[1]} ${ARGS[2]}
else
    echo 'build android'
    sh ./pack_android.sh ${ARGS[1]} ${ARGS[2]}
fi