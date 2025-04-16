import numpy as np
import wave
import struct

params = {
    'subject_id': 'S01',
    'mod_frequencies': 40,  # 调制频率（Hz）
    'carrier_freq': 1000,  # 载波频率（Hz）
    'stim_duration': 2.0,  # 持续时间（秒）
    'sample_rate' : 44100,  # 音频采样频率
    'isi_range': [1.5, 2.0],
    'sound_level': 60,  # 音量百分比（0~100%）
    'n_blocks': 3,
    'trials_per_block': 10,
    'trigger_codes': {
        '40Hz': 0x01,
        'start': 0xFF,
        'end': 0xFE
    }
}


def generate_am_wave(params):
    """
    从params字典读取参数生成AM调幅波音频文件

    参数：
    params : dict  包含以下键的参数字典：
        - subject_id       : 被试ID（用于输出文件名）
        - mod_frequencies  : 调制频率（Hz）
        - carrier_freq     : 载波频率（Hz）
        - stim_duration    : 刺激时长（秒）
        - sound_level      : 音量百分比（0~100%）
    """
    # 从params提取参数并设置默认值
    output_file = f"{params['subject_id']}_output.wav"


    # 参数校验
    if not output_file.endswith('.wav'):
        raise ValueError("输出文件名必须以.wav结尾")

    # 计算样本总数
    num_samples = int(params['stim_duration'] * params['sample_rate'])
    t = np.arange(num_samples) / params['sample_rate']

    # 生成调制信号（0.5*(1 + sin(2πfmt))）
    modulation = 0.5 * (1 + np.sin(2 * np.pi * params['mod_frequencies'] * t))

    # 生成载波信号（sin(2πfct)）
    carrier = np.sin(2 * np.pi * params['carrier_freq'] * t)

    # 合成AM信号并应用音量
    am_signal = (1 + modulation) * carrier
    am_signal /= np.max(np.abs(am_signal))  # 归一化
    am_signal *= (params['sound_level'] / 100.0)  # 音量控制

    # 转换为16位整型
    scaled_samples = (am_signal * 32767).astype(np.int16)

    # 打包并写入WAV文件
    with wave.open(output_file, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(params['sample_rate'])
        wav_file.writeframes(struct.pack("<" + "h" * len(scaled_samples), *scaled_samples))


if __name__ == "__main__":
    generate_am_wave(params)