# CNN

> 来源：`机器学习 / machine-learning/第五章-卷积神经网络/CNN.md`

![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012102859739.png)
CNN的步骤就是先重复多次Convolution+Max Pooling
最后flatten之后丢掉Fully Connected Feedforward network里面

#### CNN对比DNN
Fully Connected Feedforward network的问题在于都是完全图，两两相连，这就导致需要学习的参数特别多
但是实际上有很多参数我们是用不到的
就是说我们可以逐个识别，你不用一下子识别图里是一个鸟，而是去识别里面的pattern
#### Some patterns are much smaller than the whole image
比如说我们要识别图片里的鸟嘴，他只有很小一部分
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012103504339.png)
所以我们每次输入其实只需要这个图片的一部分，不需要整个image
#### The same patterns appear in different regions
鸟嘴可能出现在图片的边缘，也有可能在中心，但是我们完全可以共用neutron
#### Subsampling the pixels will not change the object
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012103946895.png)
我们可以对⼀张image做subsampling(⼆次抽样)，假如你把它奇数⾏、偶数列的pixel拿掉，image就可以变成原来的⼗分之⼀⼤⼩，⽽且并不会影响⼈对这张image的理解，其实就是缩小一下分辨率，但是对整体没什么影响
### Convolution
就是我们学习一个filter，他就相当于DNN里的neutron，比如3x3大小，然后我们把它放在image的左上角，让他一步一步移动，这样他就扫描过了所经过的所有3x3的区域，识别这个区域内有没有我们想要的pattern
每次移动我们就把filter和image那块做内积，就是同一个地方乘起来然后再相加
这样的好处在于每次输入只有一小部分(局部连接），而且出现在不同位置的pattern都被扫过，并且参数共享了
![image.png|435](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012105031817.png)
对每个filter都会产生一个matrix，然后我们给他合起来就得到了Feature Map
这每个matrix就叫做一个channel
#### CNN的局限性
CNN对**不同**scale**的相同**pattern**的处理**上存在⼀定的困难，由于现在每⼀个filter size都是⼀样的，这意味着，如果你今天有同⼀个pattern，它有不同的size，有⼤的⻦嘴，也有⼩的⻦嘴，CNN并不能够⾃动处理这个问题；DeepMind曾经发过⼀篇paper，上⾯提到了当你input⼀张image的时候，它在CNN前⾯，再接另外⼀个network，这个network做的事情是，它会output⼀些scalar，告诉你说，它要把这个image的⾥⾯的哪些位置做旋转、缩放，然后，再丢到CNN⾥⾯，这样你其实会得到⽐较好的performance

### Max Pooling
![image.png|439](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012112158441.png)
max pooling就是把每个filter的输出做一个subsampling，分组取最大值

#### Flatten
![image.png](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012112411698.png)
Flatten就是把feature map拉直，然后再放到DNN里面