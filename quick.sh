(command -v curl >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1) || (echo "请安装好sudo和curl" && exit 1)

NZ_BOT_BASE_PATH="/opt/nezha_api_tgbot"
if [ ! -d "${NZ_BOT_BASE_PATH}" ]; then
    sudo mkdir -p $NZ_BOT_BASE_PATH
fi
sudo curl -L https://raw.githubusercontent.com/spiritLHLS/nezha_api_tgbot/main/install.sh  -o ${NZ_BOT_BASE_PATH}/install.sh
if [[ $? != 0 ]]; then
    echo "下载脚本失败，请检查本机能否连接 raw.githubusercontent.com"
    return 0
fi
sudo chmod a+x ${NZ_BOT_BASE_PATH}/install.sh
exec sudo ${NZ_BOT_BASE_PATH}/install.sh