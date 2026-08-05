"""
潇楠 Web3哨兵 API SDK - 统一客户端入口
一个 Key 调用所有功能：文本对话、文生图、文生视频、TTS、播客、市场分析等
"""

import requests
from typing import Optional, Dict, Any

from multimodal import MultimodalMixin
from tools.generation import GenerationMixin
from tools.market import MarketMixin
from tools.data import DataMixin
from tools.media import MediaMixin
from tools.account import AccountMixin


class Client(
    MultimodalMixin,
    GenerationMixin,
    MarketMixin,
    DataMixin,
    MediaMixin,
    AccountMixin
):
    """统一客户端，所有 API 调用都通过它发起"""

    def __init__(self, api_key: str, base_url: str = "https://www.ming.store"):
        """
        初始化客户端
        :param api_key: API Key，格式 sk-xxxxxxxxxxxxxxxx
        :param base_url: API 基础地址，默认 https://www.ming.store
        """
        if not api_key:
            raise ValueError("API Key 不能为空，请前往 https://www.ming.store/key/buy_api_key.php 购买")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })

    def _post(self, path: str, data: Dict[str, Any]) -> Dict:
        """内部方法：发送 POST 请求"""
        url = f"{self.base_url}{path}"
        resp = self.session.post(url, json=data, timeout=120)
        resp.raise_for_status()
        return resp.json()

    def _get(self, path: str, params: Dict[str, Any] = None) -> Dict:
        """内部方法：发送 GET 请求"""
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    # ========== 聚合API：文本对话 ==========
    def chat(self, message: str, model: str = "deepseek-v4-flash",
             system: str = "", max_tokens: int = 4096,
             temperature: float = 0.7) -> str:
        """
        文本对话
        :param message: 用户消息
        :param model: 模型 ID，默认 deepseek-v4-flash
        :param system: 系统提示词（可选）
        :param max_tokens: 最大输出 Token
        :param temperature: 温度参数 [0, 2]
        :return: AI 回复文本
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})

        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        result = self._post("/v1/chat/completions", data)
        return result["choices"][0]["message"]["content"]

    # ========== 聚合API：查询可用模型列表 ==========
    def list_models(self) -> list:
        """
        查询可用的文本对话模型列表（无需 API Key）
        :return: 模型列表
        """
        resp = requests.get(f"{self.base_url}/v1/models", timeout=10)
        resp.raise_for_status()
        return resp.json()["data"]