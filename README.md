# nezha_api_tgbot

## 简介
适用于哪吒面板的单机版中文Tg机器人，可以便捷的通过Docker部署，随时随地快速获取机器信息。

## Docker安装(推荐)

### 环境要求

* 安装好curl、sudo

* CentOS 7+ / Debian 8+ / Ubuntu 16+ 等可通过官方脚本安装Docker的系统

```bash
curl -sSL get.docker.com | sh
```

通过上面的官方安装脚本安装docker完毕后，执行下面脚本一键安装

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/spiritLHLS/nezha_api_tgbot/main/quick.sh)
```

安装完毕后您可使用如下命令重新打开脚本

```bash
/opt/nezha_api_tgbot/install.sh
```

**如一键脚本安装失败请使用普通安装或者自行通过Docker安装**

## 普通安装

### 环境要求

* Python版本>=3.6
* 可以正常连接Telegram服务器
* 安装好git、screen、pip和任意文本编辑器

### 安装步骤

**以下Python命令均使用python3和pip3，不同系统命令不一，请根据实际情况使用**

```bash
cd /opt/
git clone https://github.com/spiritLHLS/nezha_api_tgbot
cd nezha_api_tgbot
pip3 install -r requirements.txt
cp config.py.example config.py
```

使用你喜欢的编辑器编辑配置文件config.py，请根据实际需要编辑配置项

```bash
# 根据喜好选取
nano config.py
vim config.py
vi config.py
```

编辑完成后，请使用screen挂起执行

```bash
python3 run.py
```

## 贡献者

* [spiritLHLS](https://github.com/spiritLHLS)
* [Erope](https://github.com/Erope/)

## 致谢

* 本项目基于[nezha项目](https://github.com/naiba/nezha)提供的API开发，也使用了部分nezha项目中的代码，在此感谢nezha项目组的全体成员
* 本项目基于[Python](https://www.python.org/)3.9开发，使用了[humanize](https://github.com/python-humanize/humanize) [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) [requests](https://github.com/psf/requests)，在此向所有有关的开发者表示感谢
* 尤其感谢所有的贡献者！
