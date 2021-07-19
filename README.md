# VAD_Python

实现对语音进行端点检测，并去除语音中静音段，可以作为语音信号处理的一个预处理。

# Step 1. 安装必备库
~~~python
  soundfile==0.10.3
  numpy==1.19.3
  librosa==0.8.0
  scipy==1.2.1
  matplotlib==3.3.3
~~~

# Step 2. 进入文件run.py 修改

~~~python

  ## 修改自己的文件夹路径
  src_dir = r"./切割源文件"
  des_dir = r"./切割后文件"

~~~
# Step 3. 运行run.py 得到输出结果
![image](https://user-images.githubusercontent.com/39001883/126146075-b9cce2f1-b3ea-4ada-ac83-a530b5394a69.png)



