# 文字转语音 & 语音转文字工具

这是一个功能完整的语音处理工具，支持：
- 📝 **文字转语音**（Text-to-Speech, TTS）
- 🎤 **语音转文字**（Speech-to-Text, STT）

## 功能特点

### 文字转语音（TTS）
- ✅ **离线模式**：使用 `pyttsx3` 库，无需网络，速度快
- ✅ **在线模式**：使用 `gTTS` 库，音质更好，支持多种语言
- ✅ **灵活配置**：支持语速、音量等参数调整
- ✅ **文件保存**：可保存为音频文件
- ✅ **自动播放**：转换后自动播放（可选）

### 语音转文字（STT）
- ✅ **麦克风录音识别**：实时录音并转换为文字
- ✅ **音频文件识别**：从 WAV 文件识别语音内容
- ✅ **多语言支持**：支持中文、英文等多种语言
- ✅ **结果保存**：可将识别结果保存为文本文件

## 安装依赖

### 文字转语音（TTS）依赖
```bash
pip3 install pyttsx3 gtts pyobjc
```

### 语音转文字（STT）依赖
```bash
# 基础库
pip3 install SpeechRecognition

# 麦克风录音支持（需要 PyAudio）
# macOS:
brew install portaudio
pip3 install pyaudio

# Linux:
sudo apt-get install portaudio19-dev python3-pyaudio
pip3 install pyaudio

# Windows:
pip3 install pyaudio
```

### 一次性安装全部依赖
```bash
# macOS
brew install portaudio
pip3 install pyttsx3 gtts pyobjc SpeechRecognition pyaudio

# Linux
sudo apt-get install portaudio19-dev
pip3 install pyttsx3 gtts SpeechRecognition pyaudio

# Windows
pip3 install pyttsx3 gtts pyobjc SpeechRecognition pyaudio
```

## 使用方法

### 运行程序
```bash
cd /Users/slg/text_to_viece
python3 script/main.py
```

### 功能说明

#### 1. 文字转语音（TTS）

**离线模式**：
1. 运行程序，选择功能 `1`（文字转语音）
2. 选择选项 `1`（离线模式）
3. 输入要转换的文字
4. 选择是否保存为文件

**在线模式**：
1. 运行程序，选择功能 `1`（文字转语音）
2. 选择选项 `2`（在线模式）
3. 输入要转换的文字
4. 输入输出文件名
5. 选择是否慢速朗读

#### 2. 语音转文字 - 麦克风录音（STT）

1. 运行程序，选择功能 `2`（语音转文字 - 麦克风）
2. 选择语言（中文或英文）
3. 输入录音时长（秒）
4. 对着麦克风说话
5. 查看识别结果
6. 可选：保存结果到文本文件

**注意**：需要确保麦克风权限已开启

#### 3. 语音转文字 - 音频文件（STT）

1. 运行程序，选择功能 `3`（语音转文字 - 音频文件）
2. 输入音频文件路径（支持 WAV 格式）
3. 选择语言（中文或英文）
4. 查看识别结果
5. 可选：保存结果到文本文件

## 代码示例

### 文字转语音

```python
from script.main import text_to_speech_offline, text_to_speech_online

# 离线模式 - 直接播放
text_to_speech_offline("你好，这是一个测试")

# 离线模式 - 保存为文件
text_to_speech_offline("你好，这是一个测试", output_file="hello.wav")

# 在线模式 - 保存为MP3
text_to_speech_online("你好，这是一个测试", output_file="hello.mp3")

# 在线模式 - 慢速朗读
text_to_speech_online("你好，这是一个测试", output_file="hello_slow.mp3", slow=True)
```

### 语音转文字

```python
from script.main import speech_to_text_from_mic, speech_to_text_from_file

# 从麦克风录音识别（中文，5秒）
text = speech_to_text_from_mic(language='zh-CN', duration=5)
print(f"识别结果：{text}")

# 从麦克风录音识别（英文，10秒）
text = speech_to_text_from_mic(language='en-US', duration=10)

# 从音频文件识别
text = speech_to_text_from_file("audio.wav", language='zh-CN')
print(f"识别结果：{text}")
```

## 支持的语言

### TTS - gTTS（在线模式）支持的语言示例：
- 中文（简体）：`zh-cn`
- 中文（繁体）：`zh-tw`
- 英语：`en`
- 日语：`ja`
- 韩语：`ko`
- 法语：`fr`
- 德语：`de`

更多语言请参考：https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang

### STT - 语音识别支持的语言示例：
- 中文：`zh-CN`（普通话）、`zh-TW`（台湾）、`zh-HK`（香港）
- 英语：`en-US`（美国）、`en-GB`（英国）、`en-AU`（澳大利亚）
- 日语：`ja-JP`
- 韩语：`ko-KR`
- 法语：`fr-FR`
- 德语：`de-DE`

更多语言请参考：https://cloud.google.com/speech-to-text/docs/languages

## 常见问题

### 文字转语音（TTS）

**Q: macOS 系统上 pyttsx3 报错？**  
A: 安装 pyobjc：
```bash
pip3 install pyobjc
```

**Q: 在线模式无法连接？**  
A: 确保网络连接正常，gTTS 需要访问 Google 翻译服务。

**Q: 音频无法播放？**  
A: 
- macOS：自动使用 `afplay`
- Windows：自动使用 `start`
- Linux：需要安装 `mpg123`（`sudo apt install mpg123`）

### 语音转文字（STT）

**Q: 提示找不到麦克风或 PyAudio 错误？**  
A: 需要安装 PyAudio：
```bash
# macOS
brew install portaudio
pip3 install pyaudio

# Linux
sudo apt-get install portaudio19-dev
pip3 install pyaudio

# Windows
pip3 install pyaudio
```

**Q: macOS 提示没有麦克风权限？**  
A: 前往 系统偏好设置 > 安全性与隐私 > 隐私 > 麦克风，允许终端访问麦克风。

**Q: 识别不准确或无法识别？**  
A: 
- 确保环境安静，减少背景噪音
- 说话清晰，语速适中
- 调整录音时长
- 检查麦克风是否正常工作
- 确保网络连接正常（使用 Google 语音识别服务）

**Q: 音频文件无法识别？**  
A: 
- 目前仅支持 WAV 格式
- 可以使用 ffmpeg 转换其他格式：
  ```bash
  ffmpeg -i input.mp3 output.wav
  ```

**Q: 语音识别需要网络吗？**  
A: 是的，默认使用 Google Speech Recognition API，需要网络连接。如需离线识别，可以考虑使用 Vosk 或 Whisper 等库。

## 许可证

MIT License
