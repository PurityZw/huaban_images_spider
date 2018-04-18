# -*- coding:utf-8 -*-
import random
import global_varible


class SpiderVariable():
    def get_random_user_agent(self):
        """
        获取User-Agent
        :return: 随机后的User-Agent
        """
        return random.choice(global_varible.USER_AGENT_LIST)

    def get_random_proxy_addr(self):
        """
        获取Proxy代理
        :return: 随机后的Proxy
        """
        return random.choice(global_varible.PROXY_LIST)