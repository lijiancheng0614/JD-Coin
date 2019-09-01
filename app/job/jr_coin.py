import traceback
import time
import json

from .daka import Daka


class JrCoin(Daka):
    job_name = '京东金融钢镚打卡'

    index_url = 'https://m.jr.jd.com/spe/qyy/main/index.html?userType=41'
    sign_url = 'https://ms.jr.jd.com/gw/generic/gry/h5/m/signIn?_=' + \
        str((int)(time.time()))
    test_url = 'https://ms.jr.jd.com/gw/generic/gry/h5/m/queryTodaySignResult?_=' + \
        str((int)(time.time()))

    def __init__(self, session):
        super().__init__(session)
        self.sign_data = {}

    def get_sign_data(self):
        payload = {
            # COL-AL10 荣耀10
            'reqData': '{"channelSource":"JRAPP","riskDeviceParam":"{\\"deviceType\\":\\"COL-AL10\\"}"}'
        }

        try:
            # 参见 daka_app_min.js -> h.getSign, 第 1825 行开始
            as_json = self.session.post(self.test_url, data=payload).json()
            if 'resultData' in as_json:
                self.sign_data = as_json['resultData']
            else:
                error_msg = as_json.get(
                    'resultMsg') or as_json.get('resultMessage')
                self.logger.error('获取打卡数据失败: {}'.format(error_msg))
        except Exception as e:
            self.logger.error('打卡异常: {}'.format(e))
        return self.sign_data

    def is_signed(self):
        signData = self.get_sign_data()
        if signData:
            self.logger.info('今日已打卡 获取钢镚: {}'.format(
                str(signData['resBusiData']['actualTotalRewardsValue']/100)))
            return True
        return False

    def sign(self):
        payload = {
            # COL-AL10 荣耀10
            'reqData': '{"channelSource":"JRAPP","riskDeviceParam":"{\\"deviceType\\":\\"COL-AL10\\"}"}'
        }
        r = self.session.post(self.sign_url, data=payload)
        as_json = r.json()
        if 'resultCode' in as_json and as_json['resultCode'] == 0 and as_json['resultData']['resBusiCode'] == 0:
            resBusiData = as_json['resultData']['resBusiData']
            # statusCode 14 似乎是表示延期到帐的意思, 如: 签到成功，钢镚将于15个工作日内发放到账
            message = '本次领取钢镚 '+str(resBusiData['actualTotalRewardsValue']/100)

            continuity_days = resBusiData['continuityDays']

            if continuity_days > 1:
                message += '; 签到天数: {}'.format(continuity_days)
        # 已打卡
        elif as_json['resultData']['resBusiCode'] == 15:
            sign_success = True
            message = as_json['resultData']['resBusiMsg']
        else:
            sign_success = False
            message = as_json['resultData']['resBusiMsg']

        self.logger.info('打卡状态: {}; Message: {}'.format(sign_success, message))

        return sign_success
