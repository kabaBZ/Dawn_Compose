import os
import time

from dotenv import load_dotenv
from loguru import logger

from Utils.Dawn_api import GetPoint, KeepAlive
from Utils.login import login

load_dotenv(override=True)

logger.add("./log/Dawn.log", rotation="1 MB", retention="5 days", level="INFO")


def work(USERANEM, PASSWORD, reLoginCount, token):
    # 初始化计数器
    count = 0
    while True:
        # 执行保持活动和获取点数的操作
        heart_beat = KeepAlive(USERANEM, token)
        if heart_beat:
            logger.info(f"{USERANEM} 签到成功")
            GetPoint(token)
            time.sleep(60)
        else:
            logger.error(f"{USERANEM} 签到失败")
        # 更新计数器
        count += 1
        # 每达到 reLoginCount 次后重新获取 TOKEN
        if count >= reLoginCount:
            logger.debug(f"重新登录获取Token...")
            while True:
                token = login(USERANEM, PASSWORD)
                if token:
                    break
            count = 0  # 重置计数器


def main():
    USERNAME = os.getenv("email", False)
    PASSWORD = os.getenv("pw", False)
    reLoginCount = os.getenv("reLoginCount", 200)
    if not USERNAME or not PASSWORD:
        logger.error("请先设置环境变量 email 和 pw")
        exit(1)
    token = login(USERNAME, PASSWORD)
    work(USERNAME, PASSWORD, int(reLoginCount), token)


if __name__ == "__main__":
    main()

# docker run --name=Dawn -d --restart=on-failure:100 kaba5643/dawn:0.1
