# PPP协议

> 来源：`计算机网络 / 数据链路层/PPP协议.md`

## PPP协议的特点
互联网用户需要连接ISP才能接入互联网，PPP协议就是计算机和ISP通信时所用的数据链路层协议，Point-to-Point Protocol
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20260613165237482.png)
### PPP协议的组成
1. 一个将IP数据报封装到串行链路的方法
2. 一个用来建立、配置和测试数据链路连接的链路控制协议LCP
3. 一套网络控制协议NCP

### PPP 帧格式
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20260613170411180.png)
####  首部
首部=Flag+A+C+Protocol
首部第一个字段是标志字符F，规定为0x7E
第二个地址字段A为FF，第三个控制字段C为0x03，但这两个字段并没有什么信息
第四个字段时2个字节的协议字段，用来区分后面的信息类型
1. 0x0021,IP数据报
2. 0xC021，LCP
3. 0x8021，网络层的控制数据
#### 尾部
尾部第一个字段是FCS
尾部=FCS+FLAG
MTU为1500字节
## 透明传输方式
主要问题是和F冲突，也就是0x7E(0x01111110)
### 字节填充(异步)
异步传输就是逐个比特发送，PPP选择将0x7D作为转义符
填充方法如下
- 0x7E -> (0x7D,0x5E)
- 0x7D ->(0x7D,0x5D)
- 小于0x20的，加上0x20，前面加上0x7D,0x03->(0x7D,0x23)
### 零比特填充(同步)
使用SONET/SDH链路时，是同步传输，一连串的比特连续发送
由于F有连续的6个1，先扫描信息部分，只要发现有5个连续的1，就再后面填入一个0，这样就不会出现连续的6个1，等接收端接收到时，先找到首部的F，然后对后面信息部分扫描，把这个0去掉就行
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20260613172037242.png)

- 差错检测
- PPP 不提供哪些功能

## 相关笔记
- [点对点信道](点对点信道.md)
- [封装成帧](封装成帧.md)
- [透明传输](透明传输.md)
- [差错检测](差错检测.md)
- [数据链路层](数据链路层.md)
