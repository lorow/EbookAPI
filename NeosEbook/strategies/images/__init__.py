from .ImageProcessor import get_regular_image, get_base64_image
from NeosEbook import exceptions


__strategy_map = {
    "image": get_regular_image,
    "base64": get_base64_image,
}

async def get_image_processing_strategy(format_type):
    if strategy := __strategy_map.get(format_type):
        return strategy

    raise exceptions.StrategyNotImplementedException()