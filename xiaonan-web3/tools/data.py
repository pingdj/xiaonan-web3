"""
数据获取工具：网页内容提取、实时快讯、特朗普动态
"""

import requests


class DataMixin:
    """数据获取混入类，将被 Client 继承"""

    # ========== 网页内容提取 ==========
    def extract(self, url: str, mode: str = "basic") -> dict:
        """
        网页内容提取 + AI 分析
        :param url: 网页链接，最多 3 个用英文逗号分隔
        :param mode: 模式：basic（纯提取，消耗1次）、summary（摘要生成，消耗3次）、social（社交媒体分析，消耗5次）
        :return: 字典，包含 mode 和 results
        """
        api_url = f"{self.base_url}/key/v1/extract.php"
        data = {"api_key": self.api_key, "url": url, "mode": mode}
        resp = requests.post(api_url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=60)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise Exception(f"网页提取失败：{result.get('error', '未知错误')}")
        return result

    # ========== 实时 Web3 快讯 ==========
    def newsflash(self, category: str = "all", keyword: str = "",
                  page: int = 1, size: int = 10, lang: str = "zh-cn") -> dict:
        """
        获取实时 Web3 快讯
        :param category: 分类：all, ai, funding, on-chain-data, macro-policy 等
        :param keyword: 搜索关键词（优先于 category）
        :param page: 页码，默认 1
        :param size: 每页条数，默认 10，最大 50
        :param lang: 语言，默认 zh-cn
        :return: 字典，包含 data（快讯列表）等信息
        """
        api_url = f"{self.base_url}/key/v1/newsflash.php"
        data = {
            "api_key": self.api_key,
            "category": category,
            "page": page,
            "size": size,
            "lang": lang
        }
        if keyword:
            data["keyword"] = keyword

        import time
        time.sleep(0.6)  # 避免连续请求被上游限制
        max_retries = 3
        for attempt in range(max_retries):
            resp = requests.post(api_url, data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"},
                                 timeout=15)
            if resp.status_code == 530 and attempt < max_retries - 1:
                time.sleep(2)
                continue
            break
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise Exception(f"快讯获取失败：{result.get('error', '未知错误')}")
        return result

    # ========== 特朗普动态追踪 ==========
    def trump_feed(self, action: str = "get") -> dict:
        """
        获取特朗普 Truth Social 和 Twitter/X 双平台动态
        :param action: get=获取缓存数据，refresh=强制刷新（消耗3次配额）
        :return: 字典，包含 posts 数组
        """
        api_url = f"{self.base_url}/key/v1/trump_feed.php"
        data = {"api_key": self.api_key, "action": action}
        resp = requests.post(api_url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise Exception(f"特朗普动态获取失败：{result.get('error', '未知错误')}")
        return result