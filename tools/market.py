"""
市场与安全分析工具：市场数据、风控检查、代币安全、代币审计、DEX分析
"""

import requests

from errors import XiaoNanError


class MarketMixin:
    """市场分析混入类，将被 Client 继承"""

    # ========== 市场数据 + AI 分析 ==========
    def market(self, pair: str) -> dict:
        """
        获取市场数据 + AI 分析报告
        :param pair: 交易对，如 BTCUSDT
        :return: 字典，包含 raw_data（市场数据）和 ai_analysis（AI 分析报告）
        """
        url = f"{self.base_url}/key/v1/market_analyze.php"
        data = {"api_key": self.api_key, "pair": pair.upper()}
        resp = requests.post(url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=120)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise XiaoNanError("市场数据获取失败", original_error=result.get('error', '未知错误'))
        return result

    # ========== 风控检查 + AI 解读 ==========
    def risk(self, pair: str, side: str, leverage: float = 10,
             position_size: str = "", stop_loss: str = "",
             holding_time: str = "", reason: str = "") -> dict:
        """
        开仓风控检查 + AI 解读
        :param pair: 交易对
        :param side: 方向，long 或 short
        :param leverage: 杠杆倍数
        :param position_size: 仓位大小（选填）
        :param stop_loss: 止损价（选填）
        :param holding_time: 计划持仓时间（选填）
        :param reason: 开仓理由（选填）
        :return: 字典，包含 raw_data、risk_report、ai_analysis
        """
        url = f"{self.base_url}/key/v1/risk_analyze.php"
        data = {
            "api_key": self.api_key,
            "pair": pair.upper(),
            "side": side,
            "leverage": leverage
        }
        if position_size:
            data["position_size"] = position_size
        if stop_loss:
            data["stop_loss"] = stop_loss
        if holding_time:
            data["holding_time"] = holding_time
        if reason:
            data["reason"] = reason

        resp = requests.post(url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=120)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise XiaoNanError("风控检查失败", original_error=result.get('error', '未知错误'))
        return result

    # ========== 代币安全检测 + AI 解读 ==========
    def token_check(self, address: str, chain_id: str = "56") -> dict:
        """
        代币安全检测 + AI 解读（GoPlus）
        :param address: 代币合约地址
        :param chain_id: 链 ID，默认 56（BSC），可选 1、56、137、42161、8453
        :return: 字典，包含 raw_data（安全报告）和 ai_analysis（AI 解读）
        """
        url = f"{self.base_url}/key/v1/token_analyze.php"
        data = {"api_key": self.api_key, "address": address, "chain_id": chain_id}
        resp = requests.post(url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise XiaoNanError("代币安全检测失败", original_error=result.get('error', '未知错误'))
        return result

    # ========== 代币合约审计 + AI 解读 ==========
    def token_audit(self, contract_address: str, chain_id: str = "56") -> dict:
        """
        币安代币安全审计 + AI 解读
        :param contract_address: 代币合约地址
        :param chain_id: 链 ID，默认 56（BSC），可选 1、56、137、42161、8453
        :return: 字典，包含 raw_data（审计数据）和 ai_analysis（AI 解读）
        """
        url = f"{self.base_url}/key/v1/token_audit_analyze.php"
        data = {"api_key": self.api_key, "contract_address": contract_address, "chain_id": chain_id}
        resp = requests.post(url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise XiaoNanError("代币审计失败", original_error=result.get('error', '未知错误'))
        return result

    # ========== DEX 交易对分析 + AI 解读 ==========
    def dex(self, token_address: str, chain: str = "bsc") -> dict:
        """
        DEX 交易对分析 + AI 解读
        :param token_address: 代币合约地址
        :param chain: 链标识：ethereum, bsc, solana, base, arbitrum, polygon
        :return: 字典，包含 raw_data 和 ai_analysis
        """
        url = f"{self.base_url}/key/v1/dexscreener_analyze.php"
        data = {"api_key": self.api_key, "token_address": token_address, "chain": chain}
        resp = requests.post(url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise XiaoNanError("DEX分析失败", original_error=result.get('error', '未知错误'))
        return result