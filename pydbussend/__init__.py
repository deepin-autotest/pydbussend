#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
from funnylog2 import logger


class PyDBusSend:

    def __init__(self, dbus_name: str, object_path: str = None, interface: str = None, sudo_pwd: str = None):
        self.cmd = ["dbus-send"]
        if sudo_pwd is not None:
            self.cmd.insert(0, f"echo '{sudo_pwd}' | sudo -S")
        self.cmd.append(f"--dest={dbus_name}")
        self.cmd.append(f"/{dbus_name.replace('.', '/')}" if object_path is None else object_path)
        self.interface = dbus_name if interface is None else interface
        self.cmd.append(self.interface)

    @property
    def session(self):
        self.cmd.insert(1, "--session")
        self.cmd.insert(2, "--print-reply=literal")
        return self

    @property
    def system(self):
        self.cmd.insert(1, "--system")
        self.cmd.insert(2, "--print-reply=literal")
        return self

    def method(self, method: str):
        self.cmd.remove(self.interface)
        self.cmd.append(f"{self.interface}.{method}")
        return self

    def string_args(self, *args):
        for arg in args:
            self.cmd.append(f'string:"{arg}"')

    def bool_args(self, arg: bool):
        self.cmd.append(f'boolean:"{str(arg).lower()}"')

    def send(self):
        str_cmd = " ".join(self.cmd)
        logger.info(str_cmd)
        return os.popen(str_cmd).read()


if __name__ == "__main__":
    a = PyDBusSend(
        dbus_name="org.kde.KWin",
        object_path="/Screenshot",
        interface="screenshotFullscreen",
    ).session.send()
    print(a)
