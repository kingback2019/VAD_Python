# -*- coding:utf-8 -*-

'''

@项目名称:VAD_python

@作者:kingback

@文件名称:run.py

@IDE:PyCharm

@文件创建时间:2021-07-19 16:25：36

@月份:7月


'''

from Myslience import MySlience


if __name__ == '__main__':
    # 绘画材料
    src_dir = r"./切割源文件"
    des_dir = r"./切割后文件"

    mySlience = MySlience(src_dir, des_dir)
    mySlience.demain()

