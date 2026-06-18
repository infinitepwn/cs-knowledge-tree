# TCP连接管理

> 来源：`计算机网络 / 运输层/TCP连接管理.md`

## TCP连接管理

TCP连接有三个阶段：建立连接、数据传送和连接释放
###  建立TCP连接

![image.png|377](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20260614174220467.png)
### 三次握手建立TCP连接
- 第一次：客户端发送 `SYN=1,seq=x`，请求建立连接。
SYN报文不发送数据，但是消耗一个序号
- 第二次：服务器回复 `SYN =1,ACK=1,seq=y,ack=x+1`，表示同意连接并确认客户端请求。
(ack=x+1,是因为确定seq=x已收到)
- 第三次：客户端回复 `ACK=1，seq=x+1,ack=y+1`，确认服务器响应。
(ack=y+1,确认seq=y已收到)
#### ==为什么需要第三次握手
因为第一次握手有可能延误到达，如果只有两次握手，服务器可能误以为要建立新的TCP连接，从而浪费服务器的资源，但是在三次握手的情况下，A不会理睬B
防止旧的、失效的连接请求报文突然到达服务器，导致服务器误以为客户端要建立连接，从而浪费资源。==
### 四次挥手释放TCP连接
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20260616000430576.png)
#### 第一次
客户端发送FIN=1，seq=u，u就是前面最后一个字节的序号加1，和SYN一样，不携带数据，消耗一个序号，**客户机进入FIN-WAIT-1状态**
#### 第二次
服务器发送ACK=1，seq=v，ack=u+1
此时客户机到客户端方向就关闭了，TCP协议属于半关闭状态，但是服务器还可以发信息
**服务器进入CLOSE-WAIT状态**
#### 第三次
服务器如果没有要在发送的信息，就发送FIN=1，ACK=1，seq=w，ack=u+1,**服务器进入LAST-ACK状态**

#### 第四次
客户机发送ACK=1，seq=u+1，ack=w+1，服务器收到之后就进入CLOSED状态
客户机进入TIME-WAIT状态，再等待2MSL后，进入CLOSED状态


![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20260616000908569.png)

## 相关笔记
- [TCP协议](TCP协议.md)
- [TCP报文段](TCP报文段.md)
- [运输层习题](运输层习题.md)
- [最后一节课复习](../最后一节课复习.md)
