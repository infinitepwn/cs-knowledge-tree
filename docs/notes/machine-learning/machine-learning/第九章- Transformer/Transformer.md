# Transformer

> 来源：`机器学习 / machine-learning/第九章- Transformer/Transformer.md`

Transformer就是基于self-attention的seq-seq model
它是可以并行计算的
![image.png|333](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019142548781.png)
### Encoder
![image.png|324](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019142446196.png)

#### residual connection
![image.png|298](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019142943817.png)
我们把向量b经过self-attention之后得到a，然后a+b称为残差连接
然后在做layer normalization

### Decoder
Auto regressive

Encoder的结果就是一些vector
![image.png|407](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019142427253.png)

Decoder也会得到一个向量，然后进行softmax，取最大的
他先用一个拿到第一个token，然后再把这个token作为输入继续
最后还要预测一个结束符\<EOS>
### Masked Self-attention
![image.png|446](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019142804118.png)

不看右边的，产生b1的时候只能看a1，产生b2的时候只看a1,a2

### Encoder-Decoder cross attention


#### 误差传播
#### Supervision learning

掷骰子机制
