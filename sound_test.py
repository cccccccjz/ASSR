from playsound import playsound
import os
from psychopy import visual, event, sound, core, prefs
params = {
    'subject_id': 'S01',
    'mod_frequencies': [40],  # 虽然保留参数但不再使用
    'carrier_freq': 1000,         # 虽然保留参数但不再使用
    'stim_duration': 2.0,         # 必须与output.wav实际时长一致
    'isi_range': [1.5, 2.0],
    'sound_level': 60,            # 音量参数仍有效
    'n_blocks': 3,
    'trials_per_block': 10,
    'trigger_codes': {
        '40Hz': 0x01,
        'start': 0xFF,
        'end': 0xFE
    }
}
def play_wav_files():
    print(sound.getDevices())
    prefs.hardware['audioLib'] = ['ptb']  # 可选值: ['ptb', 'pyo', 'pygame']
    prefs.hardware['audioDevice'] = '耳机 (Realtek(R) Audio)'  # 指定设备名称
    audio_file = "40Hz.wav"
    sound_stim = sound.Sound(
        os.path.abspath(audio_file),
        volume=params['sound_level'] / 100.0,
        secs=params['stim_duration']
    )
    sound_stim.play()
    core.wait(params['stim_duration'])

if __name__ == "__main__":
    play_wav_files()