"""
内容生成工具：文本转语音、双人播客、AI 一键创作
"""

import time
import requests
import json


class GenerationMixin:
    """内容生成混入类，将被 Client 继承"""

    # ========== TTS 文本转语音 ==========
    def tts(self, text: str, voice: str = "BV007_streaming") -> str:
        """
        文本转语音（TTS），返回可播放的音频链接（有效期24小时）
        :param text: 要转换成语音的文本，最长 1024 字节
        :param voice: 音色 ID，默认亲切女声 BV007_streaming
        :return: 音频 URL
        """
        url = f"{self.base_url}/key/v1/tts.php"
        data = {
            "api_key": self.api_key,
            "text": text,
            "voice": voice
        }
        resp = requests.post(url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise Exception(f"TTS 失败：{result.get('error', '未知错误')}")
        return result["audio_url"]

    # ========== 双人语音播客 ==========
    def podcast(self,
                text: str = "",
                action: int = 0,
                input_url: str = "",
                prompt_text: str = "",
                speaker1: str = "zh_male_dayixiansheng_v2_saturn_bigtts",
                speaker2: str = "zh_female_mizaitongxue_v2_saturn_bigtts",
                audio_format: str = "mp3",
                use_head_music: bool = False,
                use_tail_music: bool = False) -> "PodcastTask":
        """
        提交双人播客生成任务，返回 PodcastTask 对象
        :param text: 输入文本（action=0或3时使用）
        :param action: 生成模式：0=文本总结，3=对话文本，4=联网总结
        :param input_url: 网页链接（action=0时使用，与text二选一）
        :param prompt_text: 搜索关键词（action=4时使用）
        :param speaker1: 发音人1
        :param speaker2: 发音人2
        :param audio_format: 音频格式，默认 mp3
        :param use_head_music: 是否使用片头音效
        :param use_tail_music: 是否使用片尾音效
        :return: PodcastTask 对象，调用 .wait() 自动轮询获取音频链接
        """
        url = f"{self.base_url}/key/v1/podcast.php"
        data = {
            "api_key": self.api_key,
            "action": action,
            "speaker1": speaker1,
            "speaker2": speaker2,
            "audio_format": audio_format,
            "use_head_music": 1 if use_head_music else 0,
            "use_tail_music": 1 if use_tail_music else 0
        }
        if text:
            data["text"] = text
        if input_url:
            data["input_url"] = input_url
        if prompt_text:
            data["prompt_text"] = prompt_text

        resp = requests.post(url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise Exception(f"播客任务提交失败：{result.get('error', '未知错误')}")
        return PodcastTask(self, result["task_id"])

    # ========== AI 一键创作 ==========
    def article(self, keywords: str,
                model_index: int = 0,
                style: str = "professional",
                length: str = "standard",
                web_search_serpapi: bool = False,
                web_search_serper: bool = False) -> dict:
        """
        AI 一键创作，生成原创文章
        :param keywords: 文章主题或关键词
        :param model_index: 模型索引，0表示使用第一个可用模型
        :param style: 写作风格：professional, easy, tutorial, news, product
        :param length: 文章长度：mini, short, medium, standard
        :param web_search_serpapi: 是否启用 SerpApi 联网搜索
        :param web_search_serper: 是否启用 Serper 联网搜索
        :return: 字典，包含 title、content、excerpt、tags
        """
        url = f"{self.base_url}/key/v1/article.php"
        data = {
            "api_key": self.api_key,
            "keywords": keywords,
            "model_index": model_index,
            "style": style,
            "length": length,
            "web_search_serpapi": 1 if web_search_serpapi else 0,
            "web_search_serper": 1 if web_search_serper else 0
        }
        resp = requests.post(url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=120)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise Exception(f"AI 创作失败：{result.get('error', '未知错误')}")
        return {
            "title": result.get("title", ""),
            "content": result.get("content", ""),
            "excerpt": result.get("excerpt", ""),
            "tags": result.get("tags", "")
        }


class PodcastTask:
    """播客任务，封装自动轮询"""

    def __init__(self, client, task_id: str):
        self.client = client
        self.task_id = task_id

    def wait(self, interval: int = 10, timeout: int = 120) -> str:
        """
        等待播客生成完成，返回音频 URL
        :param interval: 轮询间隔（秒），默认 10
        :param timeout: 超时时间（秒），默认 120
        :return: 音频 URL
        """
        start = time.time()
        url = f"{self.client.base_url}/key/v1/podcast_check.php"
        params = {"api_key": self.client.api_key, "task_id": self.task_id}

        while True:
            if time.time() - start > timeout:
                raise TimeoutError(f"播客生成超时（{timeout}秒），task_id={self.task_id}")
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            if result.get("status") == "done":
                return result["audio_url"]
            if result.get("status") == "error":
                raise Exception(f"播客生成失败：{result.get('error_msg', '未知错误')}")
            time.sleep(interval)