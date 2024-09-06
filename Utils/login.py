import datetime
import json
import os

from loguru import logger

from Utils.config import LoginURL, headers, session
from Utils.deal_captcha import deal_captcha
from Utils.get_captcha import get_captcha


def req_login(USERNAME, PASSWORD, captcha_info, captcha_result) -> str:
    current_time = (
        datetime.datetime.now(datetime.timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )

    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "logindata": {"_v": "1.0.7", "datetime": current_time},
        "puzzle_id": captcha_info,
        "ans": "0",
    }
    data["ans"] = str(captcha_result)
    login_data = json.dumps(data)
    try:
        r = session.post(
            LoginURL, data=login_data, headers=headers, verify=False
        ).json()
        logger.debug(r)
        if r.get("success") is False:
            logger.warning(f"登录失败：{r['message']}")
            return False
        token = r["data"]["token"]
        logger.success(f"[√] 成功获取AuthToken {token}")
        return token
    except Exception:
        logger.exception("[x] 验证码错误，尝试重新获取...")
        return False


def login(USERNAME, PASSWORD, stack_count=0) -> str:
    # 获取并识别验证码
    captcha_result, captcha_info = get_captcha()
    if not captcha_result:
        if stack_count <= 5:
            return login(USERNAME, PASSWORD, stack_count + 1)
        logger.error(captcha_info)
        exit(1)
    captcha_str = deal_captcha(captcha_result)
    if not captcha_str:
        if stack_count <= 5:
            return login(USERNAME, PASSWORD, stack_count + 1)
        logger.error("验证码识别失败！！！")
        exit(1)
    # 登录
    token = req_login(USERNAME, PASSWORD, captcha_info, captcha_str)
    if not token:
        if stack_count <= 5:
            return login(USERNAME, PASSWORD, stack_count + 1)
        exit(1)
    return token
