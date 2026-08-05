"""
媒体处理工具：视频解析、AI数字人生成（两种版本）
"""

import time
import requests


class MediaMixin:
    """媒体处理混入类，将被 Client 继承"""

    # ========== 视频解析 ==========
    def video_parse(self, url: str) -> dict:
        """
        解析抖音或 TikTok 视频链接，返回无水印视频直链
        :param url: 抖音或 TikTok 视频链接
        :return: 字典，包含 platform、title、duration、direct_url、uploader 等
        """
        api_url = f"{self.base_url}/key/v1/video_parse.php"
        data = {"api_key": self.api_key, "url": url}
        resp = requests.post(api_url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise Exception(f"视频解析失败：{result.get('error', '未知错误')}")
        return result

    # ========== AI数字人 V1（OmniHuman1.5）==========
    def digital_human(self, text: str, image_url: str,
                      voice: str = "BV007_streaming") -> "DigitalHumanTask":
        """
        提交 AI 数字人视频生成任务（OmniHuman1.5），消耗 50 次配额
        :param text: 播报文本，最长 300 字
        :param image_url: 人物图片 URL
        :param voice: 音色 ID，默认亲切女声 BV007_streaming
        :return: DigitalHumanTask 对象，调用 .wait() 自动轮询获取视频 URL
        """
        api_url = f"{self.base_url}/key/v1/digital_human.php"
        data = {"api_key": self.api_key, "text": text, "image_url": image_url, "voice": voice}
        resp = requests.post(api_url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise Exception(f"数字人任务提交失败：{result.get('error', '未知错误')}")
        return DigitalHumanTask(self, result["task_id"], api_type="v1")


    # ========== AI数字人 V2（单图音频驱动）==========
    def digital_human_v2(self, text: str, image_url: str,
                          voice: str = "BV007_streaming") -> "DigitalHumanTask":
        """
        提交 AI 数字人视频生成任务（单图音频驱动 V2），消耗 20 次配额
        :param text: 播报文本，最长 300 字
        :param image_url: 人物图片 URL
        :param voice: 音色 ID，默认亲切女声 BV007_streaming
        :return: DigitalHumanTask 对象，调用 .wait() 自动轮询获取视频 URL
        """
        api_url = f"{self.base_url}/key/v1/digital_human_volcv2.php"
        data = {"api_key": self.api_key, "text": text, "image_url": image_url, "voice": voice}
        resp = requests.post(api_url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise Exception(f"数字人V2任务提交失败：{result.get('error', '未知错误')}")
        return DigitalHumanTask(self, result["task_id"], api_type="v2")


class DigitalHumanTask:
    """AI数字人视频生成任务，封装自动轮询逻辑"""

    def __init__(self, client, task_id: str, api_type: str = "v1"):
        self.client = client
        self.task_id = task_id
        self.api_type = api_type

    def wait(self, interval: int = 10, timeout: int = 300) -> str:
        """
        等待视频生成完成，返回视频 URL
        :param interval: 轮询间隔（秒），默认 10
        :param timeout: 超时时间（秒），默认 300（5分钟）
        :return: 视频 URL
        """
        start = time.time()
        check_url = f"{self.client.base_url}/key/v1/digital_human_check.php" if self.api_type == "v1" else f"{self.client.base_url}/key/v1/digital_human_volcv2_check.php"
        params = {"api_key": self.client.api_key, "task_id": self.task_id}

        while True:
            if time.time() - start > timeout:
                raise TimeoutError(f"数字人视频生成超时（{timeout}秒），task_id={self.task_id}")
            resp = requests.get(check_url, params=params, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            if result.get("status") == "done" and result.get("video_url"):
                return result["video_url"]
            if result.get("status") == "failed":
                raise Exception(f"数字人视频生成失败")
            time.sleep(interval)