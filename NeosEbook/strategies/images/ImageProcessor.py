import base64


async def get_regular_image(chapter):
    return chapter.content


async def get_base64_image(chapter):
    return base64.b64encode(get_regular_image(chapter))
