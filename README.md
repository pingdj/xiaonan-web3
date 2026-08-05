# 潇楠 Web3哨兵 API SDK

一个 API Key，调用所有功能：文本对话、文生图、文生视频、TTS、播客、市场分析、代币安全检测、DEX分析、网页提取、快讯、特朗普动态等 20+ 功能。

## 安装

pip install xiaonan-web3

## 快速开始

1. 购买 API Key
2. 在代码中初始化客户端

from xiaonan import Client

client = Client(api_key="sk-你的Key")

## 功能列表

### 文本对话
reply = client.chat("你好，请介绍一下你自己")
print(reply)

### 查询可用模型列表
models = client.list_models()
for m in models:
    print(m['id'], m['name'])

### 多模态模型列表
multimodal_models = client.list_multimodal_models()
for m in multimodal_models:
    print(m['model_id'], m['name'], m['type'])

### 文生图
image_url = client.image("一只在月亮下奔跑的狼")
print(image_url)

### 文生视频
task = client.video("海浪拍打礁石的慢动作")
video_url = task.wait()
print(video_url)

### TTS 文本转语音
audio_url = client.tts("你好世界")
print(audio_url)

### 双人语音播客
task = client.podcast(text="人工智能的未来发展趋势")
audio_url = task.wait()
print(audio_url)

### AI 一键创作
article = client.article("Web3发展趋势")
print(article['title'])
print(article['content'])

### 市场数据 + AI分析
data = client.market("BTCUSDT")
print(data['ai_analysis'])

### 风控检查 + AI解读
report = client.risk(pair="BTCUSDT", side="long", leverage=10)
print(report['ai_analysis'])

### 代币安全检测
result = client.token_check("0x55d398326f99059fF775485246999027B3197955")
print(result['ai_analysis'])

### 代币合约审计
result = client.token_audit("0x55d398326f99059fF775485246999027B3197955")
print(result['ai_analysis'])

### DEX交易对分析
result = client.dex("0x55d398326f99059fF775485246999027B3197955", chain="bsc")
print(result['ai_analysis'])

### 网页内容提取
result = client.extract("https://example.com/article")
print(result['results'])

### 实时Web3快讯
news = client.newsflash(category="ai", page=1, size=10)
for item in news['data']['list']:
    print(item['title'])

### 特朗普动态追踪
feed = client.trump_feed()
for post in feed['posts']:
    print(post['content'], post['platform'])

### 视频解析
info = client.video_parse("https://v.douyin.com/xxx/")
print(info['direct_url'])

### AI数字人视频生成
# V1 (OmniHuman1.5, 消耗50次配额)
task = client.digital_human(text="你好，欢迎使用AI数字人", image_url="https://example.com/photo.jpg")
video_url = task.wait()

# V2 (单图音频驱动, 消耗20次配额)
task = client.digital_human_v2(text="你好，欢迎使用AI数字人", image_url="https://example.com/photo.jpg")
video_url = task.wait()

### 配额查询
info = client.quota()
print(f"剩余: {info['remaining']}, 已用: {info['used_quota']}, 总: {info['total_quota']}")

## 错误处理
SDK 在 API 调用失败时会抛出异常，异常信息包含具体的错误原因。例如：

try:
    reply = client.chat("你好")
except Exception as e:
    print(f"调用失败: {e}")

## 更多信息
- [API 接口文档](https://www.ming.store/key/docs.php)
- [聚合多模型 API 文档](https://www.ming.store/key/llm_api_docs.php)
- [MCP 接入指南](https://www.ming.store/key/mcp_docs.php)
- [购买 API Key](https://www.ming.store/key/buy_api_key.php)