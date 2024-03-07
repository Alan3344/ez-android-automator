"""
@Time: 2023/11/17 12:21
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test_douyin.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.douyin_task1 import DouyinVideoPublishTask

client = PublishClient(uiautomator2.connect_usb())
# print(client.dump_xml())
# exit()
client.set_task(DouyinVideoPublishTask(5, '', '我总在忙忙碌碌寻宝藏', 'http://192.168.3.8:8000/media/videos/test.mp4'))
client.run_current_task()
