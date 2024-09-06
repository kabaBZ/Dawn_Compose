import ddddocr
from loguru import logger

ocr = ddddocr.DdddOcr()


def deal_captcha(img_binary):
    result = ocr.classification(img_binary)
    if len(result) != 6:
        return False
    logger.info(f"验证码结果：{result}")
    return result
