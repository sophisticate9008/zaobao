#!/usr/bin/python3
"""
# @Author         : Sakuracio
# @Date           : 2021/12/18 23:56
# @FileName       : zaobao.py
# @Description    :
# @GitHub         :
# @Modify Time    : 2022年3月1日 20:04:13
# @Project        : Zhenxun_bot
# @Software       : PyCharm
"""
from pathlib import Path
from os.path import isfile
from datetime import datetime
from nonebot import on_command
from ._data_source import get_data
from nonebot.typing import T_State
from utils.message_builder import image
from utils.http_utils import AsyncHttpx
from configs.path_config import IMAGE_PATH
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

__zx_plugin_name__ = "今日早报"
__plugin_usage__ = """
usage：
    每日的60秒早报
    指令：
        今日早报
""".strip()
__plugin_des__ = "每日的60秒早报"
__plugin_cmd__ = ["今日早报", "早报"]
__plugin_version__ = 0.6
__plugin_author__ = "Sakuracio"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["今日早报", "早报"],
}

daily = on_command("早报", aliases={'今日早报'}, priority=5, block=True)
url = "https://v2.alapi.cn/api/zaobao"


@daily.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    date = datetime.now().date()
    errmsg = '发生一了点错误...请稍后再试...'
    source = Path(IMAGE_PATH) / "zaobao" / f'{date}.png'
    # 检查缓存
    if isfile(source):
        await daily.send(image(source))
    else:
        data, code = await get_data(url)
        if code != 200:
            await daily.finish(errmsg, at_sender=True)
        result = data['data']['image'].strip('!/format/webp')
        if not result:
            await daily.finish(errmsg, at_sender=True)
        else:
            # noinspection PyBroadException
            try:
                if await AsyncHttpx.download_file(result, source):
                    await daily.send(image(source))
            except Exception as e:
                await daily.finish(errmsg, at_sender=True)
