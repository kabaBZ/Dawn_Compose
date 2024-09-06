from Utils.config import headers, KeepAliveURL, GetPointURL, session
import json
from loguru import logger
import curl_cffi


def KeepAlive(USERNAME, TOKEN):
    logger.info("准备Heartbeat")
    data = {
        "username": USERNAME,
        "extensionid": "fpdkjdnhkakefebpekbdhillbhonfjjp",
        "numberoftabs": 0,
        "_v": "1.0.7",
    }
    json_data = json.dumps(data)
    headers["authorization"] = "Berear " + str(TOKEN)
    try:
        r = session.post(KeepAliveURL, data=json_data, headers=headers, verify=False)
    except curl_cffi.requests.errors.RequestsError:
        logger.exception("Heartbeat超时")
        return False
    try:
        response = r.json()
    except json.decoder.JSONDecodeError:
        logger.exception("Heartbeat失败")
        return False
    logger.info(f"Heartbeat：{response}")
    if response.get("success") is True:
        return True
    return False


def GetPoint(TOKEN):
    try:
        logger.info("准备获取积分")
        headers["authorization"] = "Berear " + str(TOKEN)
        r = session.get(GetPointURL, headers=headers, verify=False).json()
        logger.success(f"Point：{r}")
    except:
        logger.error("获取积分失败")
