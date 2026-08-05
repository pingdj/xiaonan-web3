"""
账户工具：配额查询
"""

import requests

from errors import XiaoNanError


class AccountMixin:
    """账户混入类，将被 Client 继承"""

    def quota(self) -> dict:
        """
        查询 API Key 配额信息
        :return: 字典，包含 total_quota（总次数）、used_quota（已使用）、remaining（剩余）
        """
        url = f"{self.base_url}/key/v1/quota.php"
        data = {"api_key": self.api_key}
        resp = requests.post(url, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             timeout=10)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise XiaoNanError("配额查询失败", original_error=result.get('error', '未知错误'))
        return {
            "total_quota": result["total_quota"],
            "used_quota": result["used_quota"],
            "remaining": result["remaining"]
        }