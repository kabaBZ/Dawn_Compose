from base64 import b64decode
from io import BytesIO
from typing import Union

from Utils.config import captcha_id_url, capthca_img_url, headers, session
from loguru import logger
from PIL import Image


def get_captcha(stack_count=0) -> tuple[Union[bytes, bool], str]:
    captcha_id_response = session.request(
        "GET", captcha_id_url, headers=headers, verify=False
    )
    id_result = captcha_id_response.json()
    if id_result["success"] is not True:
        logger.error(captcha_id_response.text)
        if stack_count <= 5:
            return get_captcha(stack_count + 1)
        return False, "请求capthca_id失败"

    captcha_id = id_result["puzzle_id"]
    logger.info(f"captcha_id: {captcha_id}")

    querystring = {"puzzle_id": captcha_id}

    captcha_img_response = session.request(
        "GET",
        capthca_img_url,
        headers=headers,
        params=querystring,
        verify=False,
    )
    img_result = captcha_img_response.json()

    if img_result["success"] is not True:
        logger.error(captcha_img_response.text)
        if stack_count <= 5:
            return get_captcha(stack_count + 1)
        return False, "请求capthca_img失败"

    captcha_img_base64 = img_result["imgBase64"]

    # 二值化验证码图片，将浅色的文字抹掉
    image = Image.open(BytesIO(b64decode(captcha_img_base64)))

    # 灰度图
    gray_image = image.convert("L")

    # 设置二值化的阈值
    threshold = 150

    binary_image = gray_image.point(lambda x: 255 if x > threshold else 0, "1")

    # 保存处理后的二值化图像
    binary_image.save("binary_output_image.png")
    output_buffer = BytesIO()
    binary_image.save(output_buffer, format="JPEG")
    binary_data = output_buffer.getvalue()
    return binary_data, captcha_id
