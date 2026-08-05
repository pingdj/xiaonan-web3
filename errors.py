"""
潇楠 Web3哨兵 SDK 异常类
统一处理所有 API 错误，提供清晰的中文错误提示
"""


class XiaoNanError(Exception):
    """SDK 统一的异常类，封装 HTTP 状态码和错误信息"""

    # HTTP 状态码 → 中文错误提示映射
    MESSAGES = {
        400: "请求参数有误，请检查您的输入是否正确。",
        401: "认证失败，请检查您的 API Key 是否正确，或前往 https://www.ming.store/key/buy_api_key.php 购买。",
        403: "访问被拒绝，请确认您的 API Key 是否有权限调用此接口。",
        404: "请求的接口不存在，请检查 URL 地址是否正确。",
        429: "请求频率过高，请稍后再试（每次调用间隔至少 500 毫秒）。",
        500: "服务器内部错误，请稍后重试。如果多次出现，请联系管理员。",
        502: "上游服务暂时不可用，请稍后重试。",
        503: "服务暂时繁忙，请稍后重试。",
        530: "上游服务暂时不可用，请稍后重试。",
    }

    def __init__(self, message: str, status_code: int = None, original_error: str = None):
        """
        初始化异常
        :param message: 简要错误描述（如"文本对话失败"）
        :param status_code: HTTP 状态码，用于自动匹配中文提示
        :param original_error: API 返回的原始错误信息（可选）
        """
        self.status_code = status_code
        self.original_error = original_error

        # 拼接最终的错误消息
        parts = [message]
        if status_code and status_code in self.MESSAGES:
            parts.append(f"[{status_code}] {self.MESSAGES[status_code]}")
        elif status_code:
            parts.append(f"[{status_code}]")
        if original_error:
            parts.append(f"（原始错误: {original_error}）")

        full_message = " ".join(parts)
        super().__init__(full_message)