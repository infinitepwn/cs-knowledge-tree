# UDP用户数据报

> 来源：`计算机网络 / 运输层/UDP用户数据报.md`

## UDP 用户数据报格式
- 源端口
- 目的端口
- 长度
- 检验和
校验和不是必须的，如果不需要，就全部设为0，如果校验和算出来刚好为0，那就全置为1
- 伪首部 12B
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20260615232516944.png)

伪首部中包含了IP协议的信息
## 相关笔记
- [UDP协议](UDP协议.md)
- [端口号](端口号.md)
- [运输层](运输层.md)
