import random

from nonebot import on_command, get_driver
from nonebot.adapters import Bot, Event, Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from .data import DATA
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="发病语录",
    description="随机返回一条发病语录",
    usage="命令：发病 [发病对象]\n例如：发病 测试",
)

plugin_config = Config.parse_obj(get_driver().config)

catch_str = on_command("发病", aliases={"发癫"}, rule=to_me() if plugin_config.to_me else None, priority=10, block=True)


@catch_str.handle()
async def _(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if event.get_plaintext().strip():
        matcher.set_arg("target", args)


@catch_str.got("target", "你要对哪个人发病呢？")
async def _(matcher: Matcher, args: Message = CommandArg()):
    black_word = plugin_config.black_word
    # target_str = event.get_plaintext().strip()
    target_str = args.extract_plain_text().strip()
    for word in black_word:
        if word in target_str:
            # await matcher.reject("你发的消息中包含了黑名单词语，请重新输入！")
            return

    if not target_str:
        await matcher.reject("你发的消息中没有文本，请重新输入！")

    msg = random.choice(DATA).format(target_name=target_str)
    await matcher.finish(msg)
