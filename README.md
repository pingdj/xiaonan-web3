<p align="center">
  <h1 align="center">🛡️ 潇楠 Web3哨兵 · Python SDK</h1>
  <p align="center">
    <img src="https://img.shields.io/pypi/v/xiaonan-web3?color=blue" alt="PyPI version">
    <img src="https://img.shields.io/pypi/pyversions/xiaonan-web3?color=green" alt="Python versions">
    <img src="https://img.shields.io/pypi/dm/xiaonan-web3?color=orange" alt="Downloads">
    <img src="https://img.shields.io/github/license/pingdj/xiaonan-web3?color=lightgrey" alt="License">
  </p>
  <p align="center">
    一个 API Key，调用 20+ AI 功能。覆盖文本对话、文生图、文生视频、TTS、播客、市场分析、安全检测等全部能力。
  </p>
</p>

---

## 📦 安装

    pip install xiaonan-web3

**要求**：Python 3.8 及以上版本。

---

## 🚀 快速开始

1. [购买 API Key](https://www.ming.store/key/buy_api_key.php)
2. 在代码中初始化客户端

    from xiaonan import Client

    client = Client(api_key="sk-你的Key")

---

## 📋 功能列表

| 类别 | 方法 | 说明 |
|------|------|------|
| 💬 文本对话 | `client.chat()` | 调用 DeepSeek、GPT、Qwen、Kimi 等大模型 |
| 📋 模型列表 | `client.list_models()` | 查询可用文本模型列表 |
| 🎨 多模态模型 | `client.list_multimodal_models()` | 查询可用图像/视频模型列表 |
| 🖼️ 文生图 | `client.image()` | 根据提示词生成图片 |
| 🎬 文生视频 | `client.video().wait()` | 提交视频任务，自动轮询 |
| 🔊 TTS | `client.tts()` | 文本转语音，返回音频链接 |
| 🎙️ 播客 | `client.podcast().wait()` | 双人播客，自动轮询 |
| ✍️ AI 创作 | `client.article()` | 根据关键词生成文章 |
| 📈 市场数据 | `client.market()` | 市场数据 + AI 分析报告 |
| 🛡️ 风控检查 | `client.risk()` | 开仓风控 + AI 建议 |
| 🔍 代币安全 | `client.token_check()` | GoPlus 安全检测 |
| 🔐 代币审计 | `client.token_audit()` | 币安 Web3 合约审计 |
| 📊 DEX 分析 | `client.dex()` | DEX 交易对分析 |
| 📄 网页提取 | `client.extract()` | 网页内容提取 + AI 分析 |
| 📰 实时快讯 | `client.newsflash()` | Web3 实时快讯 |
| 🦅 特朗普动态 | `client.trump_feed()` | Truth Social + X 双平台 |
| 📹 视频解析 | `client.video_parse()` | 抖音/TikTok 去水印 |
| 🤖 数字人 V2 | `client.digital_human_v2().wait()` | 单图音频驱动，自动轮询 |
| 📊 配额查询 | `client.quota()` | 查询 Key 剩余配额 |

---

## 💻 代码示例

### 文本对话

    from xiaonan import Client

    client = Client(api_key="sk-你的Key")

    reply = client.chat("你好，请介绍一下你自己")
    print(reply)

    # 指定模型
    reply = client.chat("分析一下今天的行情", model="deepseek-v4-flash")

### 文生图

    image_url = client.image("一只在月亮下奔跑的狼")
    print(image_url)

    # 指定尺寸
    image_url = client.image("赛博朋克城市夜景", size="1024x1024")

### 文生视频

    task = client.video("海浪拍打礁石的慢动作", width=1920, height=1080)
    video_url = task.wait()  # 自动轮询直到完成
    print(video_url)

### TTS 文本转语音

    audio_url = client.tts("你好世界，欢迎使用潇楠Web3哨兵")
    print(audio_url)

### AI 一键创作

    article = client.article("Web3发展趋势", length="short")
    print(article['title'])
    print(article['content'])

### 市场数据 + AI 分析

    data = client.market("BTCUSDT")
    print(data['ai_analysis'])

### 风控检查

    report = client.risk(pair="BTCUSDT", side="long", leverage=10)
    print(f"风险等级: {report['risk_report']['level']}")

### 代币安全检测

    result = client.token_check("0x55d398326f99059fF775485246999027B3197955")
    print(f"风险等级: {result['raw_data']['risk_level']}")
    print(result['ai_analysis'])

### 查询配额

    info = client.quota()
    print(f"总: {info['total_quota']}, 已用: {info['used_quota']}, 剩余: {info['remaining']}")

---

## ❗ 错误处理

SDK 在所有 API 调用失败时抛出 `XiaoNanError` 异常，包含 HTTP 状态码和中文错误提示：

    from xiaonan import Client
    from xiaonan.errors import XiaoNanError

    client = Client(api_key="sk-你的Key")

    try:
        reply = client.chat("你好")
    except XiaoNanError as e:
        print(f"调用失败: {e}")

---

## 🔗 相关资源

| 资源 | 链接 |
|------|------|
| PyPI 包首页 | [pypi.org/project/xiaonan-web3](https://pypi.org/project/xiaonan-web3/) |
| GitHub 仓库 | [github.com/pingdj/xiaonan-web3](https://github.com/pingdj/xiaonan-web3) |
| API 接口文档 | [ming.store/key/docs.php](https://www.ming.store/key/docs.php) |
| 聚合多模型 API | [ming.store/key/llm_api_docs.php](https://www.ming.store/key/llm_api_docs.php) |
| MCP 接入指南 | [ming.store/key/mcp_docs.php](https://www.ming.store/key/mcp_docs.php) |
| 购买 API Key | [ming.store/key/buy_api_key.php](https://www.ming.store/key/buy_api_key.php) |

---

## 📄 License

MIT © 2026 潇楠 Web3实验室