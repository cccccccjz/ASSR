import numpy as np
from scipy.io import wavfile  # 改用scipy库保存浮点型音频
import os
params = {
        'subject_id': 'S01',
        'mod_frequencies': 20,
        'carrier_freq': 1000,
        'stim_duration': 2.0,
        'sample_rate': 44100,
        'isi_range': [1.5, 2.0],
        'sound_level': 60,
        'n_blocks': 1,
        'trials_per_block': 10,
        'trigger_codes': {
            '40Hz_start': 0x01,
            '40Hz_end': 0x02,
            'start': 0xFF,
            'end': 0xFE
        }
    }
def generate_am_wave(params):

    # 从参数提取关键值
    sr = params['sample_rate']
    duration = params['stim_duration']
    mod_freq = params['mod_frequencies']
    carrier_freq = params['carrier_freq']

    # 生成时间轴（更精确的linspace替代方案）
    num_samples = int(duration * sr)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    # 生成AM信号组件
    carrier = np.sin(2 * np.pi * carrier_freq * t)  # 载波
    modulator = 1 + 0.5 * np.sin(2 * np.pi * mod_freq * t)  # 调制波

    # 合成AM信号
    am_signal = carrier * modulator

    # 消除直流偏移
    am_signal -= np.mean(am_signal)

    # 添加50ms淡入淡出
    fade_duration = 0.05  # 秒
    fade_samples = int(fade_duration * sr)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    am_signal[:fade_samples] *= fade_in
    am_signal[-fade_samples:] *= fade_out

    # 动态范围压缩（防止削波）
    peak = np.max(np.abs(am_signal))
    if peak > 1.0:
        am_signal /= peak * 1.05  # 保留5%余量

    # 应用音量控制
    am_signal *= (params['sound_level'] / 100.0)

    # 保存为32位浮点WAV
    wavfile.write(
       f'{mod_freq}Hz.wav',
        sr,
        am_signal.astype(np.float32)  # 必须明确指定浮点型
    )
if __name__ == "__main__":
    generate_am_wave(params)
