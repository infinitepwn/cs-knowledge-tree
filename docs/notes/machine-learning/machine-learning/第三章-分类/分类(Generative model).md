# 分类(Generative model)

> 来源：`机器学习 / machine-learning/第三章-分类/分类(Generative model).md`

我们希望把分类问题变成一个连续的，可微分的问题来处理
那我们就考虑从概率的角度
对于每个class，我们认为他们的点是从一个高斯分布取样出来的
![image.png|482](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012143118203.png)
决定这个高斯分布的就是两个参数u和\(\Sigma\)
然后我们可以用最大似然估计法，来估计这两个参数
![image.png|487](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012143303358.png)
求解得到u的最优解就是数学期望，\(\Sigma\)就是协方差
当两个class share同一个covariance的时候，boundary就会是linear的
但注意这里我们做了一些假设，假设我们的数据是从高斯分布中采样出来的，也就是由这种分布生成的，因此称为Generative的方法
## Logistic Regression
我们也可以直接求w和b，这种方法就是discriminative的
Cross Entropy就是这里的Loss function
这个最优解是
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012143834942.png)

$$
w_{i+1} = w_i - \eta\sum_{n}{-(\hat y^n - f_{w,b}(x^n))}x_i^n
$$

#### Naive Bayes Classifier(**朴素⻉叶斯分类法**)
认为每个特征是独立的

#### Cross Entropy
Logistic Regression 通常使用 Cross Entropy 而不是 Square Error，主要原因是Square Error 与 Sigmoid 结合时，在输出严重偏离目标的饱和区域可能出现梯度过小的问题
![image.png|427](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019154012024.png)
我们考虑一下Square Error时的梯度
![image.png|426](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261019154253630.png)
他多了两个乘积

$$
f_{w,b}(x)(1-f_{w,b}(x))
$$

这个就会导致不上不下的，无论目标是0还是1，你远离还是靠近，总有一项式接近0的
，这就会导致微分很小，移动速度是⾮常慢的，而当gradient接近于0的时候，很有可能会停下来，因此使⽤square error很有可能在⼀开始的时候就卡住不动了，⽽且这⾥也不能随意地增⼤learning rate，因为在做gradient descent的时候，你的gradient接近于0，有可能离target很近也有可能很远，因此不知道learning rate应该设⼤还是设⼩

综上，尽管square error可以使⽤，但是会出现update⼗分缓慢的现象，⽽使⽤cross entropy可以让你的Training更顺利
## Softmax
Softmax 是主要用于**多分类（Multi-class Classification）**,可以理解成Logistic Regression的推广
先回顾 Logistic Regression。
对于二元分类，我们使用：\(z=w^Tx+b\)

然后通过 Sigmoid：\(\sigma(z)=\frac{1}{1+e^{-z}}\)

将结果转换为一个介于 0 和 1 之间的数

我们只需要计算一个\(P(C_1\mid x)=0.8\)，那么：\(P(C_2\mid x)=0.2\)

因为只有两个类别，\(P(C_1|x)+P(C_2|x) = 1\),我们只需要计算其中一个就行了

**但是，如果现在有三个类别呢？**

假设我们要判断一张图片属于\(C_1,C_2,C_3\)

模型会分别为三个类别计算一个分数：

$$
z_1=w_1^Tx+b_1 \\ z_2=w_2^Tx+b_2 \\ z_3=w_3^Tx+b_3
$$


例如：


$$
z= \begin{pmatrix} 3\\ -3\\ 1 \end{pmatrix}
$$


这些 \(z_i\)称为 **Logits（原始分类分数）**

但它们存在两个问题：

- 可以是任意实数，包括负数。
- 三个数加起来不一定等于 1。

因此不能直接将它们作为概率分布,这时候就需要 Softmax。

#### Softmax 的数学定义


$$
{\phantom{a}}\kern-1em P(C_i\mid x)= \frac{e^{z_i}}{\displaystyle\sum_{j=1}^{K}e^{z_j}}
$$


也可以写成：


$$
y_i=\operatorname{Softmax}(z)_i
$$


#### 为什么 Softmax 要使用指数函数？

Softmax 会进一步强化原始分数较大的类别
