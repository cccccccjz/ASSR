from psychopy import visual, event, sound, core, prefs, monitors
import random
import numpy as np
import time
import os
from generate_am_wave import generate_am_wave
from playsound import playsound
from neuracle_lib.triggerBox import TriggerBox,PackageSensorPara,TriggerIn

# 主实验
def run_assr_experiment(params):
    # 初始化窗口
    win = visual.Window(
        size=(1280, 720),
        fullscr=False,
        allowGUI=True,
        monitor='testMonitor',
        units='pix'
    )
    log_file = open(f"{params['subject_id']}.csv", "w")
    log_file.write("Block,Trial,Timestamp\n")

    try:
        # 加载音频文件
        audio_file = "40Hz.wav"  # 确保此文件存在
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"音频文件 {audio_file} 不存在")

        sound_stim = sound.Sound(
            os.path.abspath(audio_file),
            volume=params['sound_level'] / 100.0,
            secs=params['stim_duration']
        )
        print(sound.getDevices())

        """
        设置同步盒的串口
        triggerbox = TriggerBox("COM3")
        """

        # 显示指导语
        instruction = visual.TextStim(win, text="请保持放松，注意听声音\n准备好后按空格键开始实验", height=40)
        instruction.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

        """
        triggerbox.output_event_data('0xFF')
        """


        # 倒计时
        for i in range(5, 0, -1):
            countdown = visual.TextStim(win, text=str(i), height=60)
            countdown.draw()
            win.flip()
            core.wait(1)

        # 发送实验开始触发

        # 区块循环
        for block in range(params['n_blocks']):
            # 试次循环
            for trial_idx in range(params['trials_per_block']):

                # 发送触发并播放声音

                try:
                    """
                    triggerbox.output_event_data('0x01')
                    """
                    fixation = visual.TextStim(win, text="+", height=60)
                    fixation.draw()
                    win.flip()
                    sound_stim.play()
                    core.wait(params['stim_duration'])
                    """
                    triggerbox.output_event_data('0x02')
                    """
                except Exception as e:
                    print(f"播放失败 {audio_file}: {str(e)}")
                    continue  # 继续下一个试次


                win.flip()
                core.wait(params['wait_duration'])

                # 记录数据
                log_file.write(f"{block + 1},{trial_idx + 1},{time.strftime('%H:%M:%S')}\n")

                # 退出检查
                if 'escape' in event.getKeys():
                    raise KeyboardInterrupt

    except Exception as e:
        print(f"实验异常终止: {str(e)}")
    finally:
        """
        triggerbox.output_event_data('0xFE')
        """
        log_file.close()
        if 'win' in locals() and not win._closed:
            win.close()


if __name__ == "__main__":
    prefs.hardware['audioLib'] = ['ptb']  # 可选值: ['ptb', 'pyo', 'pygame']
    prefs.hardware['audioDevice'] = '耳机 (Realtek(R) Audio)'  # 指定设备名称
    params = {
        'subject_id': 'S01',
        'mod_frequencies': 40,
        'carrier_freq': 1000,
        'stim_duration': 2.0,
        'wait_duration': 5.0,
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

    # 生成音频文件（如果不存在）
    if not os.path.exists("40Hz.wav"):
        generate_am_wave(params)

    run_assr_experiment(params)