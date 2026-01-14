#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字转语音 & 语音转文字工具
- 文字转语音：支持离线（pyttsx3）和在线（gTTS）两种方式
- 语音转文字：支持麦克风录音识别和音频文件识别
"""

import os
import sys
import time


def text_to_speech_offline(text, rate=150, volume=1.0, output_file=None):
    """
    使用pyttsx3库实现离线文字转语音
    
    Args:
        text: 要转换的文字
        rate: 语速（默认150）
        volume: 音量（0.0-1.0，默认1.0）
        output_file: 输出文件路径（可选，如果提供则保存为音频文件）
    """
    try:
        import pyttsx3
    except ImportError:
        print("错误：未安装pyttsx3库")
        print("请运行：pip install pyttsx3")
        return False
    
    try:
        engine = pyttsx3.init()
        
        # 设置语速
        engine.setProperty('rate', rate)
        
        # 设置音量
        engine.setProperty('volume', volume)
        
        # 获取可用的语音
        voices = engine.getProperty('voices')
        
        # 尝试设置中文语音（如果有）
        for voice in voices:
            if 'chinese' in voice.name.lower() or 'zh' in voice.languages:
                engine.setProperty('voice', voice.id)
                break
        
        if output_file:
            # 保存到文件
            engine.save_to_file(text, output_file)
            engine.runAndWait()
            print(f"语音已保存到：{output_file}")
        else:
            # 直接播放
            engine.say(text)
            engine.runAndWait()
            print("播放完成")
        
        return True
    except Exception as e:
        print(f"离线转换失败：{e}")
        return False


def text_to_speech_online(text, lang='zh-cn', output_file='output.mp3', slow=False):
    """
    使用gTTS库实现在线文字转语音（需要网络连接）
    
    Args:
        text: 要转换的文字
        lang: 语言代码（默认'zh-cn'为中文）
        output_file: 输出文件路径
        slow: 是否慢速朗读（默认False）
    """
    try:
        from gtts import gTTS
    except ImportError:
        print("错误：未安装gTTS库")
        print("请运行：pip install gtts")
        return False
    
    try:
        # 创建gTTS对象
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # 保存音频文件
        tts.save(output_file)
        print(f"语音已保存到：{output_file}")
        
        # 可选：自动播放（需要安装播放器）
        try:
            if sys.platform == 'darwin':  # macOS
                os.system(f'afplay "{output_file}"')
            elif sys.platform == 'win32':  # Windows
                os.system(f'start {output_file}')
            else:  # Linux
                os.system(f'mpg123 "{output_file}"')
        except Exception as e:
            print(f"播放提示：可以手动打开 {output_file} 进行播放")
        
        return True
    except Exception as e:
        print(f"在线转换失败：{e}")
        return False


def speech_to_text_from_mic(language='zh-CN', duration=5):
    """
    从麦克风录音并转换为文字
    
    Args:
        language: 语言代码（默认'zh-CN'为中文）
        duration: 录音时长（秒），None 表示自动检测语音结束
    
    Returns:
        识别出的文字或 None
    """
    try:
        import speech_recognition as sr
    except ImportError:
        print("错误：未安装 speech_recognition 库")
        print("请运行：pip3 install SpeechRecognition")
        return None
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("\n正在调整环境噪音...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print(f"请开始说话（录音 {duration} 秒）...")
            
            if duration:
                audio = recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            else:
                audio = recognizer.listen(source)
            
            print("录音完成，正在识别...")
            
            # 尝试使用 Google 语音识别（需要网络）
            try:
                text = recognizer.recognize_google(audio, language=language)
                print(f"\n识别结果：{text}")
                return text
            except sr.UnknownValueError:
                print("错误：无法识别语音内容")
                return None
            except sr.RequestError as e:
                print(f"错误：无法连接到识别服务 - {e}")
                return None
                
    except ImportError as e:
        print("\n错误：PyAudio 未正确安装")
        print("\nmacOS 安装方法：")
        print("1. 安装 Homebrew（如果还没有）：")
        print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("2. 安装 portaudio：")
        print("   brew install portaudio")
        print("3. 重新安装 pyaudio：")
        print("   pip3 install pyaudio")
        print("\n或者使用功能 3（音频文件识别）来代替麦克风录音")
        return None
    except Exception as e:
        print(f"录音失败：{e}")
        return None


def speech_to_text_from_file(audio_file, language='zh-CN'):
    """
    从音频文件转换为文字
    
    Args:
        audio_file: 音频文件路径（支持 WAV 格式）
        language: 语言代码（默认'zh-CN'为中文）
    
    Returns:
        识别出的文字或 None
    """
    try:
        import speech_recognition as sr
    except ImportError:
        print("错误：未安装 speech_recognition 库")
        print("请运行：pip install SpeechRecognition")
        return None
    
    if not os.path.exists(audio_file):
        print(f"错误：文件不存在 - {audio_file}")
        return None
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            print(f"正在读取音频文件：{audio_file}")
            audio = recognizer.record(source)
            
            print("正在识别...")
            
            # 尝试使用 Google 语音识别
            try:
                text = recognizer.recognize_google(audio, language=language)
                print(f"\n识别结果：{text}")
                return text
            except sr.UnknownValueError:
                print("错误：无法识别语音内容")
                return None
            except sr.RequestError as e:
                print(f"错误：无法连接到识别服务 - {e}")
                return None
                
    except Exception as e:
        print(f"文件识别失败：{e}")
        return None


def main():
    """主函数"""
    print("=" * 50)
    print("文字转语音 & 语音转文字工具")
    print("=" * 50)
    
    # 选择功能
    print("\n请选择功能：")
    print("1. 文字转语音（Text-to-Speech）")
    print("2. 语音转文字 - 麦克风录音（Speech-to-Text）")
    print("3. 语音转文字 - 音频文件（Speech-to-Text）")
    
    function_choice = input("\n请输入选项（1/2/3）[默认1]：").strip() or "1"
    
    if function_choice == "1":
        # 文字转语音
        print("\n--- 文字转语音 ---")
        print("请选择转换模式：")
        print("1. 离线模式（pyttsx3 - 速度快，无需网络）")
        print("2. 在线模式（gTTS - 需要网络，音质好）")
        
        choice = input("\n请输入选项（1或2）[默认1]：").strip() or "1"
        
        # 输入文字
        print("\n请输入要转换的文字：")
        text = input().strip()
        
        if not text:
            print("错误：未输入任何文字")
            return
        
        # 执行转换
        if choice == "1":
            print("\n使用离线模式转换中...")
            
            # 是否保存文件
            save = input("是否保存为文件？(y/n)[默认n]：").strip().lower()
            
            if save == 'y':
                output_file = input("请输入输出文件名[默认output.wav]：").strip() or "output.wav"
                text_to_speech_offline(text, output_file=output_file)
            else:
                text_to_speech_offline(text)
        
        elif choice == "2":
            print("\n使用在线模式转换中...")
            output_file = input("请输入输出文件名[默认output.mp3]：").strip() or "output.mp3"
            
            # 是否慢速朗读
            slow = input("是否慢速朗读？(y/n)[默认n]：").strip().lower() == 'y'
            
            text_to_speech_online(text, output_file=output_file, slow=slow)
        
        else:
            print("错误：无效的选项")
    
    elif function_choice == "2":
        # 语音转文字 - 麦克风
        print("\n--- 语音转文字（麦克风录音）---")
        
        # 选择语言
        print("请选择语言：")
        print("1. 中文（zh-CN）")
        print("2. 英文（en-US）")
        lang_choice = input("请输入选项[默认1]：").strip() or "1"
        
        language = "zh-CN" if lang_choice == "1" else "en-US"
        
        # 录音时长
        duration_input = input("请输入录音时长（秒）[默认5]：").strip() or "5"
        try:
            duration = int(duration_input)
        except:
            duration = 5
        
        # 执行识别
        text = speech_to_text_from_mic(language=language, duration=duration)
        
        if text:
            # 询问是否保存
            save = input("\n是否保存识别结果到文件？(y/n)[默认n]：").strip().lower()
            if save == 'y':
                filename = input("请输入文件名[默认result.txt]：").strip() or "result.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"已保存到：{filename}")
    
    elif function_choice == "3":
        # 语音转文字 - 音频文件
        print("\n--- 语音转文字（音频文件）---")
        print("支持的格式：WAV")
        
        audio_file = input("请输入音频文件路径：").strip()
        
        if not audio_file:
            print("错误：未输入文件路径")
            return
        
        # 选择语言
        print("\n请选择语言：")
        print("1. 中文（zh-CN）")
        print("2. 英文（en-US）")
        lang_choice = input("请输入选项[默认1]：").strip() or "1"
        
        language = "zh-CN" if lang_choice == "1" else "en-US"
        
        # 执行识别
        text = speech_to_text_from_file(audio_file, language=language)
        
        if text:
            # 询问是否保存
            save = input("\n是否保存识别结果到文件？(y/n)[默认n]：").strip().lower()
            if save == 'y':
                filename = input("请输入文件名[默认result.txt]：").strip() or "result.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"已保存到：{filename}")
    
    else:
        print("错误：无效的选项")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已退出")
    except Exception as e:
        print(f"\n发生错误：{e}")
