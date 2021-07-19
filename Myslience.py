

# -*- coding:utf-8 -*-

'''

@项目名称:VAD_python

@作者:kingback

@文件名称:Myslience.py

@IDE:PyCharm

@文件创建时间:2021-07-19 16:25：36

@月份:7月


'''

import os
import soundfile as sf
import numpy as np
import librosa
from scipy.signal import medfilt
import matplotlib.pyplot as plt


class MySlience(object):

    def __init__(self,src_dir,des_dir):
        # 设置属性
        self.src_dir=src_dir        #待切除静音段的语音所在文件夹
        self.des_dir=des_dir        #去除静音段后语音所在文件夹
        
    # 返回传入文件夹内的所有语音文件路径
    def file_name(self,file_dir):
        L = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.wav':
                    L.append(os.path.join(root, file))
            return L


    def demain(self):
        src_files=self.file_name(self.src_dir)
        for src_filenamae in src_files:
            self.slience(src_filenamae,self.des_dir)
            
    def frame2Time(self,frameNum,framelen,inc,fs):
        frames=np.array(range(0,frameNum,1))
        frames=frames*inc+framelen/2
        frameTime=frames/fs
        return frameTime

    #
    def slience(self,filename, slice_dir):

        print('当前在操作文件：', filename)

        clean_data, _ = sf.read(filename)
        
        '''
        Step 1: 这一步根据动态阈值实现端点检测，并绘图表示
        '''

        # 求取MFCCs参数
        y, sr = librosa.load(filename, sr=16000)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=24, n_fft=1024, hop_length=512)

        # x轴坐标变换
        frames=mfccs.shape[1]
        time=np.array(range(len(y)))/16000                  #采样点转换为时间刻度
        frame2Time=self.frame2Time(frames,1024,512,16000)   #帧转换为时间刻度

        #设置图片大小
        plt.figure(figsize=(10, 7))

        # 画出短时过零率
        plt.subplot(311)
        # 显示中文
        plt.plot(time, y, 'black')
        plt.xlabel("Time/s\n (a) Voice waveform", fontsize=15, fontweight='bold')
        plt.ylabel("amplitude/V", fontsize=15, fontweight='bold')
        # 修改坐标轴字体及大小
        plt.yticks(fontproperties='Times New Roman', size=15,weight='bold')
        plt.xticks(fontproperties='Times New Roman', size=15,weight='bold')
        # 时间刻度显示
        plt.axis([0,max(frame2Time),0.8*min(y),1.1*max(y)])


        # 画图显示MFcc0
        plt.subplot(312)
        # plt.title("The original MFCC0 feature",fontproperties='Times New Roman', size=15,fontweight='bold')
        plt.plot(frame2Time,mfccs[0, :],'black')
        plt.xlabel("Time/s\n (b) MFCC0 feature",fontsize=15,fontweight='bold')
        plt.ylabel("amplitude",fontsize=15,fontweight='bold')
        # 修改坐标轴字体及大小
        plt.yticks(fontproperties='Times New Roman', size=15,weight='bold')
        plt.xticks(fontproperties='Times New Roman', size=15,weight='bold')
        plt.axis([0,max(frame2Time),min(mfccs[0, :])-10,max(mfccs[0, :])+10])

     
        # # 对mfcc进行中值滤波，平滑参数
        Mfcc1=medfilt(mfccs[0,:],9)

        #
        pic = mfccs[0, :]
        pic=Mfcc1
        start = 0
        end = 0
        points = []
        print(min(pic) * 0.9)
        min_data = min(pic) * 0.9
        for i in range((pic.shape[0])):
            if (pic[i] < min_data and start == 0):
                start = i
                # end=i
            if (pic[i] < min_data and start != 0):
                end = i
                # print(end)

            elif (pic[i] > min_data and start != 0):
                # print('当前时间段为：',start,end)
                hh = [start, end]
                points.append(hh)
                start = 0

        # 解决 文件的最后为静音
        if (pic[-1] < min_data and start != 0):
            hh = [start, end]
            points.append(hh)
            start = 0
        distances = []
        
        for i in range(len(points)):

            two_ends = points[i]
            distance = two_ends[1] - two_ends[0]
            if (distance > 5):
                distances.append(points[i])
                

        # 这里说明一下，distance内存的是最终需要的结果
        print(distances, np.array(distances).shape)
        print(points)
 
        plt.subplot(313)
        # 对mfcc进行中值滤波
        Mfcc1 = medfilt(mfccs[0, :], 9)
        plt.plot(frame2Time, Mfcc1,'black')
        plt.axis([0, max(frame2Time), min(Mfcc1) - 10, max(Mfcc1) + 10])
        plt.xlabel("Time/s\n (c) MFCC0 median filtering and Voice Activity Detection ", fontsize=15,fontweight='bold')
        plt.ylabel("amplitude", fontsize=15,fontweight='bold')
        # 修改坐标轴字体及大小
        plt.yticks(fontproperties='Times New Roman', size=15,weight='bold')
        plt.xticks(fontproperties='Times New Roman', size=15,weight='bold')

        # 开始画出剪切掉的部分
        starts = np.array(distances)[:, 0]
        ends = np.array(distances)[:, 1]
        starts2time = (starts * 512 + 512) / 16000
        ends2time = (ends * 512 + 512) / 16000
        print(ends2time)
        plt.vlines(starts2time, min(Mfcc1)-10, max(Mfcc1)+10, colors="black", linestyles="solid",lw=2)
        plt.vlines(ends2time, min(Mfcc1)-10, max(Mfcc1)+10, colors="black", linestyles="dashed",lw=2.5)


        # 设置标题
        plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.tight_layout()  # 解决绘图时上下标题重叠现象

        # 保存到本地文件夹
        name = filename.split('\\')[-1]
        '''
        选择保存为svg格式或者png格式
        '''
        # png_name = os.path.join(slice_dir, name) + ".png"
        # plt.savefig(png_name, dpi=200)

        svg_name = os.path.join(slice_dir, name) + ".svg"
        plt.savefig(svg_name, bbox_inches='tight')


        # 画图展示
        plt.show()
        
        '''
           Step2: 这一步根据端点检测结果，去除语音中静音段。
        '''


        # 取出来端点，按照端点，进行切割,分情况讨论：len(distances)==0 :未检测到静音段  else: 检测到存在静音段

        if (len(distances) == 0):

            print('检测到的静音段的个数为： %s 未对文件进行处理：' % len(distances))
            slience_clean = os.path.join(slice_dir, name)
            sf.write(slience_clean, clean_data, 16000)


        else:
            # print(points)
            slience_data = []
            for i in range(len(distances)):
                if (i == 0):
                    start, end = distances[i]
                    # 将左右端点转换到 采样点
                    if (start == 1):
                        internal_clean = clean_data[0:0]
                    else:
                        # 求取开始帧的开头
                        start = (start - 1) * 512
                        # 求取结束帧的结尾
                        end = (end - 1) * 512 + 1024

                        internal_clean = clean_data[0:start - 1]
                else:
                    _, end = distances[i - 1]
                    start, _ = distances[i]
                    start = (start - 1) * 512
                    end = (end - 1) * 512 + 1024
                    internal_clean = clean_data[end + 1:start]

                hhh = np.array(internal_clean)
                print('纯净的片段的长度为：', hhh.shape)

                # 开始拼接
                slience_data.extend(internal_clean)


            # 开始 添加 最后一部分,需要分情况讨论，1. 文件末尾本来就是静音的  2.文件末尾不是静音的
            ll = len(distances)
            _, end = distances[ll - 1]
            end = (end - 1) * 512 + 1024
            end_part_clean = clean_data[end:len(clean_data)]
            slience_data.extend(end_part_clean)


            # #文件写入
            hh = np.array(slience_data)
            print('去除静音段的片段采样点个数为：', len(hh))
            slience_file_path = os.path.join(slice_dir, name)
            sf.write(slience_file_path, slience_data, 16000)
