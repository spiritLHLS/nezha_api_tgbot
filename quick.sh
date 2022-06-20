#!/bin/bash

# 必须以root运行脚本
check_root(){
  [[ $(id -u) != 0 ]] && red " The script must be run as root, you can enter sudo -i and then download and run again." && exit 1
}

# 判断系统，并选择相应的指令集
check_operating_system(){
  CMD=("$(grep -i pretty_name /etc/os-release 2>/dev/null | cut -d \" -f2)"
       "$(hostnamectl 2>/dev/null | grep -i system | cut -d : -f2)"
       "$(lsb_release -sd 2>/dev/null)" "$(grep -i description /etc/lsb-release 2>/dev/null | cut -d \" -f2)"
       "$(grep . /etc/redhat-release 2>/dev/null)"
       "$(grep . /etc/issue 2>/dev/null | cut -d \\ -f1 | sed '/^[ ]*$/d')"
      )

  for i in "${CMD[@]}"; do SYS="$i" && [[ -n $SYS ]] && break; done

  REGEX=("debian" "ubuntu" "centos|red hat|kernel|oracle linux|amazon linux|alma|rocky")
  RELEASE=("Debian" "Ubuntu" "CentOS")
  PACKAGE_UPDATE=("apt -y update" "apt -y update" "yum -y update")
  PACKAGE_INSTALL=("apt -y install" "apt -y install" "yum -y install")
  PACKAGE_UNINSTALL=("apt -y autoremove" "apt -y autoremove" "yum -y autoremove")

  for ((int = 0; int < ${#REGEX[@]}; int++)); do
    [[ $(echo "$SYS" | tr '[:upper:]' '[:lower:]') =~ ${REGEX[int]} ]] && SYSTEM="${RELEASE[int]}" && break
  done

  [[ -z $SYSTEM ]] && red " ERROR: The script supports Debian, Ubuntu, CentOS or Alpine systems only.\n" && exit 1
}

# 判断宿主机的 IPv4 或双栈情况,没有拉取不了 docker
check_ipv4(){
  ! curl -s4m8 ip.sb | grep -q '\.' && red " ERROR：The host must have IPv4. " && exit 1
}

# 主程序
check_root
check_operating_system
check_ipv4

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
