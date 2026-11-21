# RNN

> 来源：`机器学习 / machine-learning/第七章-RNN/RNN.md`

Recurrent Neural Network
在slot filling当中我们使用DNN会遇到问题
![image.png|467](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20261012113126484.png)
在智能客服、智能订票系统中，往往会需要slot filling技术，它会分析⽤⼾说出的语句，将时间、地址等有效的关键词填到对应的槽上，并过滤掉⽆效的词语

词汇要转化成vector，可以使⽤1-of-N编码，word hashing或者是word vector等⽅式，此外我们可以尝试使⽤Feedforward Neural Network来分析词汇，判断出它是属于时间或是⽬的地的概率

但这样做会有⼀个问题，该神经⽹络会先处理“arrive”和“leave”这两个词汇，然后再处理“Taipei”，这时对NN来说，输⼊是相同的，它没有办法区分出“Taipei”是出发地还是⽬的地

这个时候我们就希望神经⽹络是有记忆的，如果NN在看到“Taipei”的时候，还能记住之前已经看过的“arrive”或是“leave”，就可以根据上下⽂得到正确的答案

LSTM

前⽂提到的RNN只是最简单的版本，并没有对memory的管理多加约束，可以随时进⾏读取，⽽现在常⽤的memory管理⽅式叫做⻓短期记忆(Long Short-term Memory)，简称LSTM

冷知识：可以被理解为⽐较⻓的短期记忆，因此是short-term，⽽⾮是long-short term