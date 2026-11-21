# Self-Attention

> 来源：`机器学习 / machine-learning/第八章-自注意力机制/Self-Attention.md`

RNN/LSTM的局限：
- 无法并行化处理序列信息
- 本质都是顺序处理，对全局信息的理解依然不理想(捕捉全局依赖的能力较差)
- 能否设计可以并行处理，且序列中的每一个元素都可以直接与序列中的所有其他元素进行交互的模型？
#### one-hot
没有语义信息
### embedding
可以看出一些语义的关联

#### Self-Attention

![image.png|378](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019143519879.png)

就是考虑用内积来得到向量之间的相关关系
![image.png|493](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019145220302.png)

对于任意两个向量，分别进行线性变换，一个乘一个\(W^q\),另一个乘以\(W^k\)
分别得到\(q,k\)
最后做内积得到注意力分数
### QKV模式
![image.png|553](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019150303379.png)
我们先查询\(a^1\)和其他的关系，
就先把\(a^1\)得到查询向量

$$
q^1 = W^q a^1
$$

然后对于其他的向量就求value-vector
也就是

$$
k^i = W^k a^i
$$

那么我们就能得到一些score

$$
\alpha_{1,i} = q^1 \cdot k^i
$$

当然自相关性也可以做一下，然后得到这些score之后，我们就做一个softmax
![image.png|502](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019150605416.png)
然后我们加权求和就能得到\(b^1\)

### Multi-head self-attention
我们可以多弄几个q
得到多个b
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019152457700.png)

得到多个b之后，我们把它拼接起来，然后再乘以一个矩阵\(W^O\)
![image.png|518](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019152636999.png)
就得到了最后的\(b^i\)
