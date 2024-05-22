"""
@Time: 2024/5/14 19:00
@Auth: coin
@Email: 918731093@qq.com
@File: bilibili_task.py
@IDE: PyCharm
@Motto：one coin
"""
import time
from ez_android_automator.client import Stage, PublishClient, AndroidClient, PublishTask, DownloadMediaStage, \
    PhoneLoginTask, WaitCallBackStage


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.restart_app("tv.danmaku.bili", self.clear_data)
        if self.clear_data:
            client.wait_to_click({'text': '同意并继续'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({"content-desc": "登录，按钮"})
        client.wait_to_click({"text": "请输入手机号码"})
        client.device.send_keys(self.phone)
        client.wait_to_click({"text": "获取验证码"})


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.device.send_keys(self.code)
        client.wait_to_click({"text": "同意并登录"})

    def code_callback(self, code: str):
        self.code = code


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({"content-desc": "发布内容,5之3,标签"}, gap=3)


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '视频'})
        time.sleep(1)
        client.device.click(160, 650)
        client.wait_to_click({'text': '发布'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, content: str):
        super().__init__(serial)
        self.content = content

    def run(self, client: PublishClient):
        client.wait_to_click({"text": "合适的标题可以吸引更多人观看～"})
        client.device.send_keys(self.content)
        client.wait_to_click({"text": "发布"})


class BilibiliPublishVideoTask(PublishTask):
    """
    Publish a video on Bilibili.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        # self.stages.append(DownloadMediaStage(0, video))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))


class BilibiliPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, self.get_code, auth_stage.code_callback))
        self.stages.append(auth_stage)
