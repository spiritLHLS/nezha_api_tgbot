# by spiritlhls
import socket
import requests
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from datetime import datetime, timedelta
from datetime import timedelta
from datetime import timezone
import logging
import humanize
from config import *

# 版本
version = "2022.06.08"

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

# 协调世界时
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
# 北京时间
beijing_now = utc_now.astimezone(SHA_TZ)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(module)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=log_level)

socket.setdefaulttimeout(30)
s = requests.Session()
s.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=TGWORKERS * 2))
s.mount('http://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=TGWORKERS * 2))

headers = {
    "Authorization": token_of_nezha
}
s.headers.update(headers)

if link_of_nezha.endswith('/'):
    link = link_of_nezha
else:
    link = link_of_nezha + '/'

def get_tag(tag):
    # tag为空，即查询默认时，由于面板BUG会显示所有鸡，等待面板修复
    logging.debug(f"查询Tag:{tag}的服务器详细信息")
    datas = s.get(f"{link}api/v1/server/details?tag={tag}").json()["result"]
    names = []
    for i in datas:
        names.append(i['name'])
    return datas, names

def get_list():
    logging.debug(f"获取全部服务器列表")
    datas = s.get(f"{link}api/v1/server/list").json()["result"]
    names = []
    for i in datas:
        names.append(i['name'])
    return datas, names

def checkid(id):
    # datas, names = get_list()
    logging.debug(f"查询ID:{id}的服务器详细信息")
    data = s.get(f"{link}api/v1/server/details?id={id}").json()
    assert len(data['result']) == 1, f"ID:{id}号服务器不存在"
    detail = data['result'][0]
    ### toal
    MemTotal = humanize.naturalsize(detail['host']['MemTotal'], gnu=True)
    DiskTotal = humanize.naturalsize(detail['host']['DiskTotal'], gnu=True)
    SwapTotal = humanize.naturalsize(detail['host']['SwapTotal'], gnu=True)
    CPU = f"{detail['status']['CPU']:.2f}"
    MemUsed = humanize.naturalsize(detail['status']['MemUsed'], gnu=True)
    Mempercent = f"{(detail['status']['MemUsed'] / detail['host']['MemTotal'])*100:.2f}" if detail['host']['MemTotal'] !=0 else "0"
    SwapUsed = humanize.naturalsize(detail['status']['SwapUsed'], gnu=True)
    Swapercent = f"{(detail['status']['SwapUsed'] / detail['host']['SwapTotal'])*100:.2f}" if detail['host']['SwapTotal'] !=0 else "0"
    DiskUsed = humanize.naturalsize(detail['status']['DiskUsed'], gnu=True)
    Diskpercent = f"{(detail['status']['DiskUsed'] / detail['host']['DiskTotal'])*100:.2f}" if detail['host']['DiskTotal'] !=0 else "0"
    NetInTransfer = humanize.naturalsize(detail['status']['NetInTransfer'], gnu=True)
    NetOutTransfer = humanize.naturalsize(detail['status']['NetOutTransfer'], gnu=True)
    NetInSpeed = humanize.naturalsize(detail['status']['NetInSpeed'], gnu=True)
    NetOutSpeed = humanize.naturalsize(detail['status']['NetOutSpeed'], gnu=True)
    Load1 = f"{detail['status']['Load1']:.2f}"
    Load5 = f"{detail['status']['Load1']:.2f}"
    Load15 = f"{detail['status']['Load1']:.2f}"
    status_msg = f"{detail['name']}\n" \
        f"CPU {CPU}% [{detail['host']['Arch']}]\n" \
        f"负载 {Load1} {Load5} {Load15}\n" \
        f"内存 {Mempercent}% [{MemUsed}/{MemTotal}]\n" \
        f"交换 {Swapercent}% [{SwapUsed}/{SwapTotal}]\n" \
        f"硬盘 {Diskpercent}% [{DiskUsed}/{DiskTotal}]\n" \
        f"网速 ↓{NetInSpeed}/s ↑{NetOutSpeed}/s\n" \
        f"流量 ↓{NetInTransfer} ↑{NetOutTransfer}\n"
    return status_msg
    
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
            [
                InlineKeyboardButton("开始查询", callback_data='1')
            ],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query = context.args[0]
        query.edit_message_text(
            f'版本：{version}\n你好，{update.effective_user.first_name}\n'
            f'{wellcome_msg}\n', reply_markup=reply_markup)
    except:
        update.effective_message.reply_text(
            f'版本：{version}\n你好，{update.effective_user.first_name}\n'
            f'{wellcome_msg}\n', reply_markup=reply_markup)

def check(update: Update, context: CallbackContext) -> None:
    try:
        id = context.args[0]
    except:
        update.effective_message.reply_text("输入为空")
        return
    logging.info(f"刷新ID:{id}的服务器")
    try:
        msg = checkid(id)
        keyboard = [
            [
                InlineKeyboardButton("刷新", callback_data=f'2|{id}'),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        date = (beijing_now.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        msg = msg + "\n" + date
        try:
            query = context.args[1]
            query.edit_message_text(msg, reply_markup=reply_markup)
        except:
            update.effective_message.reply_text(msg, reply_markup=reply_markup)
    except BaseException as e:
        update.effective_message.reply_text("未知错误")
        logging.error(f"获取第{id}号信息时发生错误", exc_info=True)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == "1":
        logging.info(f"获取服务器列表")
        query.edit_message_text(text="正在获取服务器列表")
        datas, _ = get_list()
        tags = []
        keys = []
        temp = ""
        count = 0
        for m in datas:
            if temp != m["tag"] and m["tag"] not in tags:
                tags.append(m["tag"])
                temp = m["tag"]
                keys.append(InlineKeyboardButton(str(count), callback_data=f'4|{m["tag"]}'))
                count += 1
        temp = [[]]
        count = 0
        for i in keys:
            if (count % 6) == 0:
                temp.append([])
            temp[int(count / 6)].append(i)
            count += 1
        temp.append([InlineKeyboardButton("返回主菜单", callback_data=f'5')])
        keyboard = temp
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = f"TAGID  TAGNAME\n"
        count = 0
        for i in tags:
            if len(i) == 0:
                i = "默认"
            msg += f"{count} {i}\n"
            count += 1
        msg = msg + "点击你要查询的tag列出服务器列表"
        query.edit_message_text(msg, reply_markup=reply_markup)
    elif query.data[0] == "2":
        context.args = [query.data[2:], query]
        check(update, context)
    elif query.data[0] == "4":
        context.args = [query.data[2:], query]
        tag(update, context)
    elif query.data == "5":
        context.args = [query]
        start(update, context)

def tag(update: Update, context: CallbackContext) -> None:
    try:
        tagname = context.args[0]
    except:
        update.effective_message.reply_text("输入为空")
        return
    logging.info(f"获取Tag:{tagname}的服务器列表")
    try:
        datas, names = get_tag(tagname)
        msg = f"ID  NAME\n"
        keys = []
        for i, j in zip(datas, names):
            msg += f"{i['id']} {j}\n"
            keys.append(InlineKeyboardButton(i['id'], callback_data=f'2|{i["id"]}'))
        temp = [[]]
        count = 0
        for i in keys:
            if (count % 6) == 0:
                temp.append([])
            temp[int(count/6)].append(i)
            count += 1
        temp.append([InlineKeyboardButton("返回主菜单", callback_data=f'5')])
        keyboard = temp
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = msg + "\n点击你的服务器名字前的id对应的按钮\n进行服务器信息查询"
        try:
            query = context.args[1]
            query.edit_message_text(msg, reply_markup=reply_markup)
        except:
            update.effective_message.reply_text(msg)
            update.effective_message.reply_text("\n/check 你的服务器名字前的id\n进行服务器信息查询")
    except BaseException as e:
        logging.error(f"获取Tag:{tagname}的服务器列表时发生错误", exc_info=True)
        update.effective_message.reply_text("输入错误")

############################################################################################# 主体

def main() -> None:
    updater = Updater(TOKEN, workers=TGWORKERS)
    updater.dispatcher.add_handler(CommandHandler('start', start, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('help', start, run_async=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(button, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('tag', tag, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('check', check, run_async=True))
    logging.debug("准备启动轮询")
    updater.start_polling(read_latency=1)
    logging.debug("启动完成，进入阻塞状态")
    updater.idle()
    logging.debug("结束程序")

if __name__ == '__main__':
    print("本Bot由spiritlhl编写")
    print("开源地址: https://github.com/spiritLHLS/nezha_api_tgbot")
    print("欢迎关注我的Tg频道: @VPS_spiders")
    print("Bot开始运行...")
    main()
