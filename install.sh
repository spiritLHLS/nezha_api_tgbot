#!/bin/bash

#========================================================
#   System Required: CentOS 7+ / Debian 8+ / Ubuntu 16+ /
#     Arch 未测试
#   Description: nezha_api_tgbot安装脚本
#   Github: https://github.com/spiritLHLS/nezha_api_tgbot
#========================================================

#========================================================
#   本脚本修改自naiba的nezha项目
#   在此感谢nezha项目组的全体成员
#   Github: https://github.com/naiba/nezha/
#   源文件: /script/install.sh
#========================================================

utf8_locale=$(locale -a 2>/dev/null | grep -i -m 1 -E "UTF-8|utf8")
if [[ -z "$utf8_locale" ]]; then
  echo "No UTF-8 locale found"
else
  export LC_ALL="$utf8_locale"
  export LANG="$utf8_locale"
  export LANGUAGE="$utf8_locale"
  echo "Locale set to $utf8_locale"
fi

NZ_BOT_BASE_PATH="/opt/nezha_api_tgbot"
NZ_BOT_VERSION="v0.0.1"

red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'
export PATH=$PATH:/usr/local/bin

pre_check() {
    command -v systemctl >/dev/null 2>&1
    if [[ $? != 0 ]]; then
        echo "不支持此系统：未找到 systemctl 命令"
        exit 1
    fi

    # check root
    [[ $EUID -ne 0 ]] && echo -e "${red}错误: ${plain} 必须使用root用户运行此脚本！\n" && exit 1

    GITHUB_RAW_URL="raw.githubusercontent.com/spiritLHLS/nezha_api_tgbot/master"
    Get_Docker_URL="get.docker.com"
    Docker_IMG="ghcr.io/spiritlhls/nezhaapitgbot"
}

confirm() {
    if [[ $# > 1 ]]; then
        echo && read -e -p "$1 [默认$2]: " temp
        if [[ x"${temp}" == x"" ]]; then
            temp=$2
        fi
    else
        read -e -p "$1 [y/n]: " temp
    fi
    if [[ x"${temp}" == x"y" || x"${temp}" == x"Y" ]]; then
        return 0
    else
        return 1
    fi
}

update_script() {
    echo -e "> 更新脚本"

    curl -sL https://${GITHUB_RAW_URL}/install.sh -o /tmp/install.sh
    new_version=$(cat /tmp/install.sh | grep "NZ_BOT_VERSION" | head -n 1 | awk -F "=" '{print $2}' | sed 's/\"//g;s/,//g;s/ //g')
    if [ ! -n "$new_version" ]; then
        echo -e "脚本获取失败，请检查本机能否链接 https://${GITHUB_RAW_URL}/install.sh"
        return 1
    fi
    echo -e "当前最新版本为: ${new_version}"
    mv -f /tmp/install.sh ${NZ_BOT_BASE_PATH}/install.sh && chmod a+x ${NZ_BOT_BASE_PATH}/install.sh

    echo -e "3s后执行新脚本"
    sleep 3s
    clear
    exec ${NZ_BOT_BASE_PATH}/install.sh
    exit 0
}

before_show_menu() {
    echo && echo -n -e "${yellow}* 按回车返回主菜单 *${plain}" && read temp
    show_menu
}

install_base() {
    (command -v curl >/dev/null 2>&1 && command -v wget >/dev/null 2>&1 && command -v getenforce >/dev/null 2>&1) ||
        (install_soft curl wget)
}

install_soft() {
    # Arch官方库不包含selinux等组件
    (command -v yum >/dev/null 2>&1 && yum makecache && yum install $* selinux-policy -y) ||
        (command -v apt >/dev/null 2>&1 && apt update && apt install $* selinux-utils -y) ||
        (command -v pacman >/dev/null 2>&1 && pacman -Syu $*) ||
        (command -v apt-get >/dev/null 2>&1 && apt-get update && apt-get install $* selinux-utils -y)
}

install_bot() {
    install_base

    echo -e "> 安装Bot"

    command -v docker >/dev/null 2>&1
    if [[ $? != 0 ]]; then
        echo -e "正在安装 Docker"
        bash <(curl -sL https://${Get_Docker_URL}) ${Get_Docker_Argu} >/dev/null 2>&1
        if [[ $? != 0 ]]; then
            echo -e "${red}下载脚本失败，请检查本机能否连接 ${Get_Docker_URL}${plain}"
            return 0
        fi
        systemctl enable docker.service
        systemctl start docker.service
        echo -e "${green}Docker${plain} 安装成功"
    fi

    command -v docker-compose >/dev/null 2>&1
    if [[ $? != 0 ]]; then
        echo -e "正在安装 Docker Compose"
        wget -t 2 -T 10 -O /usr/local/bin/docker-compose "https://${GITHUB_URL}/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" >/dev/null 2>&1
        if [[ $? != 0 ]]; then
            echo -e "${red}下载脚本失败，请检查本机能否连接 ${GITHUB_URL}${plain}"
            return 0
        fi
        chmod +x /usr/local/bin/docker-compose
        echo -e "${green}Docker Compose${plain} 安装成功"
    fi

    modify_bot_config

    if [[ $# == 0 ]]; then
        before_show_menu
    fi
}

selinux(){
    #判断当前的状态
    getenforce | grep '[Ee]nfor'
    if [ $? -eq 0 ];then
        echo -e "SELinux是开启状态，正在关闭！" 
        setenforce 0 &>/dev/null
        find_key="SELINUX="
        sed -ri "/^$find_key/c${find_key}disabled" /etc/selinux/config
    fi
}

modify_bot_config() {
    echo -e "> 修改Bot配置"

    echo -e "正在下载 Docker 脚本"
    wget -t 2 -T 10 -O ${NZ_BOT_BASE_PATH}/docker-compose.yaml https://${GITHUB_RAW_URL}/docker-compose.yaml >/dev/null 2>&1
    if [[ $? != 0 ]]; then
        echo -e "${red}下载脚本失败，请检查本机能否连接 ${GITHUB_RAW_URL}${plain}"
        return 0
    fi

    wget -t 2 -T 10 -O ${NZ_BOT_BASE_PATH}/config.py https://${GITHUB_RAW_URL}/config.py.example >/dev/null 2>&1
    if [[ $? != 0 ]]; then
        echo -e "${red}下载配置文件失败，请检查本机能否连接 ${GITHUB_RAW_URL}${plain}"
        return 0
    fi

    echo "关于 Telegram Bot Token：在 http://t.me/BotFather 创建" &&
        read -ep "请输入 Bot Token: " Bot_TOKEN &&
        read -ep "请输入 面板地址，格式应如 https://ops.naibahq.com/ ，注意需以http(s)开头，以/结尾: " link_of_nezha &&
        read -ep "请输入 面板API Token: " token_of_nezha &&
        read -ep "请输入欢迎语，注意不要出现\ /等符号: (默认 本机器人提供对接nezha探针面板的API提供TG查询功能)" wellcome_msg

    if [[ -z "${Bot_TOKEN}" || -z "${link_of_nezha}" || -z "${token_of_nezha}" ]]; then
        echo -e "${red}所有选项都不能为空${plain}"
        before_show_menu
        return 1
    fi

    if [[ -z "${wellcome_msg}" ]]; then
        wellcome_msg="本机器人提供对接nezha探针面板的API提供TG查询功能"
    fi

    sed -i "s/BotToken_Get_From_BotFather/${Bot_TOKEN}/" ${NZ_BOT_BASE_PATH}/config.py
    sed -i "s/https:\/\/ops.naibahq.com\//${link_of_nezha//\//\\\/}/" ${NZ_BOT_BASE_PATH}/config.py
    sed -i "s/DashboardToken_Get_AdminPanel/${token_of_nezha}/" ${NZ_BOT_BASE_PATH}/config.py
    sed -i "s/本机器人提供对接nezha探针面板的API提供TG查询功能/${wellcome_msg}/" ${NZ_BOT_BASE_PATH}/config.py

    echo -e "Bot配置 ${green}修改成功，请稍等重启生效${plain}"

    restart_and_update

    if [[ $# == 0 ]]; then
        before_show_menu
    fi
}


restart_and_update() {
    echo -e "> 重启并更新Bot"

    cd $NZ_BOT_BASE_PATH
    docker-compose pull
    docker-compose down
    docker-compose up -d
    if [[ $? == 0 ]]; then
        echo -e "${green}Bot 重启成功${plain}"
    else
        echo -e "${red}重启失败，可能是因为启动时间超过了两秒，请稍后查看日志信息${plain}"
    fi

    if [[ $# == 0 ]]; then
        before_show_menu
    fi
}

start_bot() {
    echo -e "> 启动Bot"

    cd $NZ_BOT_BASE_PATH && docker-compose up -d
    if [[ $? == 0 ]]; then
        echo -e "${green}Bot 启动成功${plain}"
    else
        echo -e "${red}启动失败，请稍后查看日志信息${plain}"
    fi

    if [[ $# == 0 ]]; then
        before_show_menu
    fi
}

stop_bot() {
    echo -e "> 停止Bot"

    cd $NZ_BOT_BASE_PATH && docker-compose down
    if [[ $? == 0 ]]; then
        echo -e "${green}Bot 停止成功${plain}"
    else
        echo -e "${red}停止失败，请稍后查看日志信息${plain}"
    fi

    if [[ $# == 0 ]]; then
        before_show_menu
    fi
}

show_bot_log() {
    echo -e "> 获取Bot日志"

    cd $NZ_BOT_BASE_PATH && docker-compose logs -f

    if [[ $# == 0 ]]; then
        before_show_menu
    fi
}

uninstall_bot() {
    echo -e "> 卸载Bot及脚本"

    cd $NZ_BOT_BASE_PATH &&
        docker-compose down
    rm -rf $NZ_BOT_BASE_PATH
    docker rmi -f ${Docker_IMG} > /dev/null 2>&1

    echo -e "卸载成功，3s后退出脚本"
    sleep 3s
    exit 0
}

show_menu() {
    echo -e "
    ${green}哪吒单机Bot管理脚本${plain} ${red}${NZ_BOT_VERSION}${plain}
    --- https://github.com/spiritLHLS/nezha_api_tgbot ---
    ${green}1.${plain}  安装Bot
    ${green}2.${plain}  修改Bot配置
    ${green}3.${plain}  启动Bot
    ${green}4.${plain}  停止Bot
    ${green}5.${plain}  重启并更新Bot
    ${green}6.${plain}  查看Bot日志
    ${green}7.${plain}  卸载Bot及脚本
    ————————————————-
    ${green}8.${plain}  更新脚本
    ————————————————-
    ${green}0.${plain}  退出脚本
    "
    echo && read -ep "请输入选择 [0-8]: " num

    case "${num}" in
    0)
        exit 0
        ;;
    1)
        install_bot
        ;;
    2)
        modify_bot_config
        ;;
    3)
        start_bot
        ;;
    4)
        stop_bot
        ;;
    5)
        restart_and_update
        ;;
    6)
        show_bot_log
        ;;
    7)
        uninstall_bot
        ;;
    8)
        update_script
        ;;
    *)
        echo -e "${red}请输入正确的数字 [0-8]${plain}"
        ;;
    esac
}

pre_check
show_menu
