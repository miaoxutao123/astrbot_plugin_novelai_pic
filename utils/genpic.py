import aiohttp
import asyncio
import os

async def generate_image(
    prompt,
    api_key,
    save_path="output_image.png",
    model="nai-diffusion-4-full",
    width=512,
    height=512,
    steps=50,
    scale=12.0
):
    """
    Generate an image using NovelAI API.

    Args:
        prompt (str): The text prompt for image generation.
        api_key (str): Your NovelAI API key.
        save_path (str): Path to save the generated image. Default is "output_image.png".
        model (str): The model to use for image generation. Default is "nai-diffusion-4-full".
        width (int): Width of the generated image. Default is 512.
        height (int): Height of the generated image. Default is 512.
        steps (int): Number of steps for image generation. Default is 50.
        scale (float): Scale factor for image generation. Default is 12.0.

    Returns:
        str: The file path of the saved image if successful.
    """
    url = "https://image.novelai.net/ai/generate-image"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": prompt,
        "model": model,
        "parameters": {
            "width": width,
            "height": height,
            "steps": steps,
            "scale": scale
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                # Save the image
                with open(save_path, "wb") as f:
                    f.write(await response.read())
                print(f"Image generated and saved as {save_path}")
                return save_path
            else:
                error_message = await response.text()
                print(f"Failed to generate image: {response.status} - {error_message}")
                return None

# Example usage
# To test, call this function in an async context, e.g., asyncio.run(main())
async def main():
    api_key = "your_api_key_here"  # Replace with your NovelAI API key
    prompt = "A beautiful fantasy landscape with mountains and a river"
    save_path = "images/generated_image.png"  # Customize save path
    await generate_image(prompt, api_key, save_path=save_path, width=256, height=256, steps=30, scale=7.5)

# Uncomment the following line to test the function
# asyncio.run(main())