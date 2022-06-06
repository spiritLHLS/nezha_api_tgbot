import requests
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from datetime import datetime, timedelta
from datetime import timedelta
from datetime import timezone

# BOT API TOKEN
TOKEN = 'BOTTOKEN'
# 版本
version = "05.31"
# 线程
TGWORKERS = 20
# 面板API
link_of_nezha = ""
# 面板token
token_of_nezha = ""

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

# 协调世界时
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
# 北京时间
beijing_now = utc_now.astimezone(SHA_TZ)


def get_ori():
    return link_of_nezha, token_of_nezha

def get_tag(tag, link, token):
    headers = {
        "Authorization": token
    }
    datas = requests.get(f"{link}api/v1/server/details?tag={tag}", headers=headers).json()["result"]
    names = []
    for i in datas:
        names.append(i['name'])
    return datas, names

def get_list(link, token):
    headers = {
        "Authorization": token
    }
    datas = requests.get(f"{link}api/v1/server/list", headers=headers).json()["result"]
    names = []
    for i in datas:
        names.append(i['name'])
    return datas, names

def checkid(id, link, token):
    headers = {
        "Authorization": token
    }
    # datas, names = get_list()
    data = requests.get(f"{link}api/v1/server/details?id={id}", headers=headers)
    detail = data.json()['result'][0]
    ### toal
    try:
        MemTotal = format(detail['host']['MemTotal'] / (1024 * 1024 * 1024), '0.2f')
    except:
        MemTotal = "0"
    try:
        DiskTotal = format(detail['host']['DiskTotal'] / (1024 * 1024 * 1024), '0.2f')
    except:
        DiskTotal = "0"
    try:
        SwapTotal = format(detail['host']['SwapTotal'] / (1024 * 1024 * 1024), '0.2f')
    except:
        SwapTotal = "0"
    ### use
    try:
        CPU = format(detail['status']['CPU'], '0.2f')
    except:
        CPU = "0"
    try:
        MemUsed = format(detail['status']['MemUsed'] / (1024 * 1024 * 1024), '0.2f')
    except:
        MemUsed = "0"
    try:
        Mempercent = format((detail['status']['MemUsed'] / detail['host']['MemTotal'])*100, '0.2f')
    except:
        Mempercent = 0
    try:
        SwapUsed = format(detail['status']['SwapUsed'] / (1024 * 1024 * 1024), '0.2f')
    except:
        SwapUsed = "0"
    try:
        Swapercent = format((detail['status']['SwapUsed'] / detail['host']['SwapTotal'])*100, '0.2f')
    except:
        Swapercent = "0"
    try:
        DiskUsed = format(detail['status']['DiskUsed'] / (1024 * 1024 * 1024), '0.2f')
    except:
        DiskUsed = "0"
    try:
        Diskpercent = format((detail['status']['DiskUsed'] / detail['host']['DiskTotal'])*100, '0.2f')
    except:
        Diskpercent = "0"
    try:
        NetInTransfer = format(detail['status']['NetInTransfer'] / (1024 * 1024 * 1024), '0.2f')
    except:
        NetInTransfer = "0"
    try:
        NetOutTransfer = format(detail['status']['NetOutTransfer'] / (1024 * 1024 * 1024), '0.2f')
    except:
        NetOutTransfer = "0"
    try:
        NetInSpeed = format(detail['status']['NetInSpeed'] / (1024 * 1024), '0.2f')
    except:
        NetInSpeed = "0"
    try:
        NetOutSpeed = format(detail['status']['NetOutSpeed'] / (1024 * 1024), '0.2f')
    except:
        NetOutSpeed = "0"
    try:
        Load1 = format(detail['status']['Load1'], '0.2f')
    except:
        Load1 = "0"
    try:
        Load5 = format(detail['status']['Load5'], '0.2f')
    except:
        Load5 = "0"
    try:
        Load15 = format(detail['status']['Load15'], '0.2f')
    except:
        Load15 = "0"
    m1 = f"{detail['name']}\n" \
         f"CPU {CPU}% [{detail['host']['Arch']}]\n" \
         f"负载 {Load1} {Load5} {Load15}\n" \
         f"内存 {Mempercent}% [{MemUsed} GB/{MemTotal} GB]\n" \
         f"交换 {Swapercent}% [{SwapUsed}/{SwapTotal} GB]\n" \
         f"硬盘 {Diskpercent}% [{DiskUsed}/{DiskTotal} GB]\n" \
         f"网速 ↓{NetInSpeed} MB/s ↑{NetOutSpeed} MB/s\n" \
         f"流量 ↓{NetInTransfer} GB ↑{NetOutTransfer} GB\n"
    return m1


def check_is_member_of_channel(update: Update):
    try:
        bot = Bot(TOKEN)
        result = bot.get_chat_member("@VPS_spiders", update.effective_user.id)
        if result['status'] == 'left':
            update.message.reply_text(text="服务器由频道 @VPS_spiders 提供，关注频道免除本消息提示")
    except Exception as e:
        print(e)
        update.message.reply_text(text="服务器由频道 @VPS_spiders 提供，关注频道免除本消息提示")

def start(update: Update, context: CallbackContext) -> None:
    try:
        query = context.args[0]
        check_is_member_of_channel(update)
        keyboard = [
            [
                InlineKeyboardButton("开始查询", callback_data='1'),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            f'版本：{version}\n你好，{update.effective_user.first_name}\n'
            f'本机器人提供对接nezha探针面板的API提供TG查询功能\n'
            f'查询前请先绑定面板链接和API的token\n'
            f'重要声明：\n'
            f'本机器人使用您的面板API默认获取您服务器的信息\n'
            f'其中包含您的服务器IP(但不包含密码)\n'
            f'如需使用，默认同意本机器人进行上述操作\n'
            f'敏感信息本机器人保证不泄露，自行承担风险', reply_markup=reply_markup)
    except:
        check_is_member_of_channel(update)
        keyboard = [
            [
                InlineKeyboardButton("开始查询", callback_data='1'),
                InlineKeyboardButton("绑定面板", callback_data='3'),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.effective_message.reply_text(
            f'版本：{version}\n你好，{update.effective_user.first_name}\n'
            f'本机器人提供对接nezha探针面板的API提供TG查询功能\n'
            f'查询前请先绑定面板链接和API的token\n'
            f'重要声明：\n'
            f'本机器人使用您的面板API默认获取您服务器的信息\n'
            f'其中包含您的服务器IP(但不包含密码)\n'
            f'如需使用，默认同意本机器人进行上述操作\n'
            f'敏感信息本机器人保证不泄露，自行承担风险', reply_markup=reply_markup)



def check(update: Update, context: CallbackContext) -> None:
    try:
        id = context.args[0]
    except:
        update.effective_message.reply_text("输入为空")
    try:
        try:
            query = context.args[1]
            link, token = get_ori()
            msg = checkid(id, link, token)
            keyboard = [
                [
                    InlineKeyboardButton("刷新", callback_data=f'2|{id}'),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            date = (beijing_now.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            msg = msg + "\n" + date
            query.edit_message_text(msg, reply_markup=reply_markup)
        except:
            link, token = get_ori()
            msg = checkid(id, link, token)
            date = (beijing_now.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            msg = msg + "\n" + date
            keyboard = [
                [
                    InlineKeyboardButton("刷新", callback_data=f'2|{id}'),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.effective_message.reply_text(msg, reply_markup=reply_markup)
    except:
        update.effective_message.reply_text("未知错误")


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == "1":
        query.edit_message_text(text="正在获取服务器列表")
        link, token = get_ori()
        datas, names = get_list(link, token)
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
            msg += f"{count} {i}\n"
            count += 1
        msg = msg + "点击你要查询的tag列出服务器列表"
        query.edit_message_text(msg, reply_markup=reply_markup)
        # update.effective_message.reply_text("输入\n/tag 你的面板tag名字前的id\n进行tag查询")
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
    try:
        link, token = get_ori()
        datas, names = get_list(link, token)
        tags = []
        temp = ""
        for m in datas:
            if temp != m["tag"]:
                tags.append(m["tag"])
                temp = m["tag"]
        datas, names = get_tag(tagname, link, token)
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
        except Exception as e:
            print(e)
            update.effective_message.reply_text(msg)
            update.effective_message.reply_text("\n/check 你的服务器名字前的id\n进行服务器信息查询")
    except:
        update.effective_message.reply_text("输入错误")


def add(update: Update, context: CallbackContext) -> None:
    try:
        url = context.args[0]
        token = context.args[1]
        userid = update.effective_user.id
        with open("users.txt", "r", encoding='utf-8') as fp:
            tp = fp.read()
        if str(userid) not in tp:
            try:
                headers = {
                    "Authorization": token
                }
                requests.get(f"{url}api/v1/server/list", headers=headers)
                with open("users.txt", "a", encoding='utf-8') as fp:
                    fp.write(f"\n{str(userid)} {url} {token}")
                    update.effective_message.reply_text("用户绑定成功，输入 /start 返回主菜单")
            except Exception as e:
                print(e)
                pass
        else:
            update.effective_message.reply_text("用户已绑定，输入 /start 返回主菜单")
    except:
        update.effective_message.reply_text(text="请按照格式输入绑定面板\n/add 面板链接 token\n绑定，注意链接带http或https前缀，并以/结尾")

def delete(update: Update, context: CallbackContext) -> None:
    with open("users.txt", "r", encoding='utf-8') as fp:
        tp = fp.read().split("\n")
    cp = []
    for i in tp:
        if str(update.effective_user.id) not in i:
            cp.append(i+"\n")
    with open("users.txt", "w", encoding='utf-8') as fp:
        fp.writelines(cp)
    update.effective_message.reply_text("已删除绑定，输入 /start 返回主菜单")

############################################################################################# 主体

def main() -> None:
    updater = Updater(TOKEN, workers=TGWORKERS)
    updater.dispatcher.add_handler(CommandHandler('start', start, run_async=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(button, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('tag', tag, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('check', check, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('add', add, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('delete', delete, run_async=True))
    updater.start_polling(read_latency=1)
    updater.idle()

if __name__ == '__main__':
    main()