from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Node, Plain, Image, Video, Nodes
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api import logger
import astrbot.api.message_components as Comp
from .utils.novelai_plugin import generate_novelai_image
@register("nai_picgen", "喵喵", "一个简单的使用nai来绘图的插件", "1.0.3")
class MyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.apikey = config.get("apikey")
        self.preset = config.get("preset")
        self.proxy = config.get("proxy")
        self.modle = config.get("model")
        self.width = config.get("width")
        self.height = config.get("height")
    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        logger.info("插件初始化完成。")

    @filter.command("nai_picgen")
    async def nai_picgen(self, event: AstrMessageEvent, prompt: str ):
        apikey = self.apikey
        preset = self.preset
        proxy = self.proxy
        width = self.width
        height = self.height
        input_model = self.modle

        if proxy != "none":
            proxy = self.proxy
        if not prompt:
            yield event.plain_result("请提供提示词！例如：/nai_picgen 一个美丽的森林")
            return

        try:
            generated_files = await generate_novelai_image(
                prompt=preset+prompt,
                jwt_token = apikey,
                output_dir = "data/plugins/astrbot_plugin_novelai_pic/pic_gen",
                model = input_model,
                width = width,  
                height = height,
                proxy= None,
            )
            if generated_files:
                chain = [
                    Comp.image.fromFileSystem(path = generated_files)
                ]
                yield event.chain_result(chain)
            else:
                yield event.plain_result("未生成任何图像，请检查提示词或稍后再试。")
        except Exception as e:
            logger.error(f"生成图像时发生错误: {e}")
            yield event.plain_result("生成图像时发生错误，请稍后再试。")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        logger.info("插件已卸载。")
