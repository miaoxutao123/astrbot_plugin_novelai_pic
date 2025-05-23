import asyncio
import os
from pathlib import Path
from typing import Optional, Union, Literal
from novelai_image_generator import NovelAIImageGenerator
from novelai_python.sdk.ai.generate_image import Model

# 定义可用的模型类型
ModelType = Literal[
    "nai-diffusion-3",  # NovelAI Diffusion 3
    "nai-diffusion-3-inpainting",  # NovelAI Diffusion 3 Inpainting
    "nai-diffusion-4",  # NovelAI Diffusion 4
    "nai-diffusion-4-inpainting",  # NovelAI Diffusion 4 Inpainting
    "nai-diffusion-4-5",  # NovelAI Diffusion 4.5
    "nai-diffusion-4-5-inpainting",  # NovelAI Diffusion 4.5 Inpainting
    "nai-diffusion-4-5-curated",  # NovelAI Diffusion 4.5 Curated
    "nai-diffusion-4-5-curated-inpainting",  # NovelAI Diffusion 4.5 Curated Inpainting
]

# 模型映射字典
MODEL_MAPPING = {
    "nai-diffusion-3": Model.NAI_DIFFUSION_3,
    "nai-diffusion-3-inpainting": Model.NAI_DIFFUSION_3_INPAINTING,
    "nai-diffusion-4": Model.NAI_DIFFUSION_4,
    "nai-diffusion-4-inpainting": Model.NAI_DIFFUSION_4_INPAINTING,
    "nai-diffusion-4-5": Model.NAI_DIFFUSION_4_5,
    "nai-diffusion-4-5-inpainting": Model.NAI_DIFFUSION_4_5_INPAINTING,
    "nai-diffusion-4-5-curated": Model.NAI_DIFFUSION_4_5_CURATED,
    "nai-diffusion-4-5-curated-inpainting": Model.NAI_DIFFUSION_4_5_CURATED_INPAINTING,
}

async def generate_novelai_image(
    prompt: str,
    jwt_token: str,
    output_dir: Union[str, Path] = "generated_images",
    width: int = 512,
    height: int = 512,
    proxy: Optional[str] = None,
    negative_prompt: str = "worst quality, low quality, blurry, distorted",
    filename: Optional[str] = None,
    model: ModelType = "nai-diffusion-4-5-curated"  # 默认使用4.5 curated模型
) -> str:
    """
    使用NovelAI生成图像的异步函数
    
    Args:
        prompt (str): 图像生成提示词
        jwt_token (str): NovelAI的JWT令牌
        output_dir (Union[str, Path]): 输出目录，默认为"generated_images"
        width (int): 图像宽度，默认512
        height (int): 图像高度，默认512
        proxy (Optional[str]): 代理地址，例如"socks5://127.0.0.1:1080"，默认不使用代理
        negative_prompt (str): 负向提示词，用于提高图像质量
        filename (Optional[str]): 输出文件名，默认自动生成
        model (ModelType): 使用的模型，默认为"nai-diffusion-4-5-curated"
        
    Returns:
        str: 生成图像的文件路径
        
    Raises:
        Exception: 当生成失败时抛出异常
    """
    try:
        # 设置代理（如果提供）
        if proxy:
            if proxy.startswith("http"):
                os.environ["HTTP_PROXY"] = proxy
                os.environ["HTTPS_PROXY"] = proxy
            elif proxy.startswith("socks"):
                os.environ["ALL_PROXY"] = proxy
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 初始化生成器
        generator = NovelAIImageGenerator(jwt_token=jwt_token)
        
        # 获取模型
        selected_model = MODEL_MAPPING.get(model)
        if not selected_model:
            raise ValueError(f"不支持的模型: {model}")
        
        # 生成图像
        filepath = await generator.generate_simple_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            filename=filename,
            model=selected_model
        )
        
        return str(filepath)
        
    except Exception as e:
        raise Exception(f"图像生成失败: {str(e)}")
        
    finally:
        # 清理代理设置
        for key in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"]:
            if key in os.environ:
                del os.environ[key]

# 使用示例
async def example_usage():
    """使用示例"""
    try:
        # 你的JWT令牌
        jwt_token = "your_jwt_token_here"
        
        # 生成图像
        filepath = await generate_novelai_image(
            prompt="1girl, beautiful, anime style, masterpiece",
            jwt_token=jwt_token,
            proxy="socks5://127.0.0.1:1080",  # 可选
            width=768,
            height=768,
            filename="test_image.png",
            model="nai-diffusion-4-5-curated"  # 使用4.5 curated模型
        )
        
        print(f"图像已生成: {filepath}")
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    asyncio.run(example_usage()) 