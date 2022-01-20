# -*- coding:utf8 -*-
from django.core.mail import EmailMessage
from typing import List


class Email:
    def __init__(self, subject: str, body: str, to_mails: List[str], files=(), html=True):
        self.message = EmailMessage(subject, body, from_email="", to=to_mails)
        for f in files:
            self.message.attach_file(f)
        if html:
            self.message.content_subtype = "html"

    def send(self):
        return self.message.send()


if __name__ == "__main__":
    import os
    import django
    from pathlib import Path

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tty.settings")
    django.setup()
    import sys

    project_path = Path(__file__).resolve().parent.parent.parent
    sys.path.append(project_path)
    e = Email("易趣互动", '<a href="https://baidu.com">您的新配音音频justcon已发送</a>', ["lin.yu.chen@foxmail.com"], [str(project_path / "db.sqlite3")], html=True)
    print(e.send())
