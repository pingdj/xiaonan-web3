"""
多模态生成模块：文生图、文生视频、视频查询
"""

import time
import requests

from errors import XiaoNanError

class MultimodalMixin:
    """多模态功能混入类，将被 Client 继承"""

    def list_multimodal_models(self) -> list:
        """
        查询可用的多模态模型列表（无需 API Key）
        :return: 模型列表
        """
        resp = requests.get(f"{self.base_url}/v1/multimodal/models", timeout=10)
        resp.raise_for_status()
        return resp.json()["data"]

    def image(self, prompt: str, size: str = "1024x768",
              image_url: str = "", negative_prompt: str = "",
              seed: int = None) -> str:
        """
        文生图
        :param prompt: 提示词
        :param size: 图像尺寸，支持 1024x768、1024x1024、768x1024
        :param image_url: 参考图 URL（可选，用于图生图）
        :param negative_prompt: 反向提示词（可选）
        :param seed: 随机种子（可选）
        :return: 图片 URL
        """
        data = {
            "model": "agnes-image-2.1-flash",
            "prompt": prompt,
            "size": size
        }
        if image_url:
            data["image_url"] = image_url
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = seed

        result = self._post("/v1/multimodal/completions", data)
        # OpenAI 兼容格式 {"created":..., "data":[{"url":"..."}]}
        if "data" in result and len(result["data"]) > 0:
            return result["data"][0]["url"]
        # 后备：直接返回 url 字段
        if "url" in result:
            return result["url"]
        raise XiaoNanError("文生图失败，返回数据中未找到图片链接")

    def video(self, prompt: str, width: int = 1152, height: int = 768,
              num_frames: int = None, frame_rate: int = 24,
              image_url: str = "", negative_prompt: str = "",
              seed: int = None):
        """
        提交文生视频任务
        :param prompt: 提示词
        :param width: 视频宽度，默认 1152
        :param height: 视频高度，默认 768
        :param num_frames: 帧数（81-441），默认 121（约5秒）
        :param frame_rate: 帧率，默认 24
        :param image_url: 参考图 URL（可选）
        :param negative_prompt: 反向提示词（可选）
        :param seed: 随机种子（可选）
        :return: VideoTask 对象，调用 .wait() 自动轮询获取视频 URL
        """
        data = {
            "model": "agnes-video-v2.0",
            "prompt": prompt,
            "width": width,
            "height": height,
            "frame_rate": frame_rate
        }
        if num_frames is not None:
            data["num_frames"] = num_frames
        if image_url:
            data["image_url"] = image_url
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = seed

        result = self._post("/v1/multimodal/completions", data)
        if not result.get("success"):
            raise XiaoNanError("文生视频任务提交失败", original_error=result.get('error', '未知错误'))
        video_id = result["video_id"]
        return VideoTask(self, video_id)


class VideoTask:
    """文生视频任务，封装自动轮询逻辑"""

    def __init__(self, client, video_id: str):
        self.client = client
        self.video_id = video_id

    def wait(self, interval: int = 10, timeout: int = 360) -> str:
        """
        等待视频生成完成，返回视频 URL
        :param interval: 轮询间隔（秒），默认 10
        :param timeout: 超时时间（秒），默认 360（6分钟）
        :return: 视频 URL
        """
        start = time.time()
        url = f"{self.client.base_url}/v1/multimodal/video_query"
        headers = {"Authorization": f"Bearer {self.client.api_key}"}

        while True:
            if time.time() - start > timeout:
                raise TimeoutError(f"视频生成超时（{timeout}秒），video_id={self.video_id}")

            resp = requests.get(url, params={"video_id": self.video_id},
                                headers=headers, timeout=30)
            resp.raise_for_status()
            result = resp.json()

            if result.get("url"):
                return result["url"]
            if result.get("status") in ("failed", "error"):
                raise XiaoNanError("文生视频生成失败", original_error=str(result))

            time.sleep(interval)