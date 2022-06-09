# nezha_api_tgbot

## 简介
适用于哪吒面板的单机版中文Tg机器人，可以便捷的通过Docker部署，随时随地快速获取机器信息。

## Docker安装(推荐)

### 环境要求

* CentOS 7+ / Debian 8+ / Ubuntu 16+ 等可通过官方脚本安装Docker的系统
* 安装好curl、sudo

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