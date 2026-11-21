# 实验：宝可梦战斗力（CP）回归问题

> 来源：`机器学习 / machine-learning/lab/lab0/lab0.md`

## 实验目标

实现本周课程所讲述的宝可梦战斗力（CP）的回归问题。

## 实验内容

- 给定 10 组宝可梦进化前后的 CP 值（training data）
- 假定回归函数为课堂上所讲述的一元一次函数：


$$
y=b+w x
$$


- Loss function 为：


$$
L(w,b)
=
\sum_{n=1}^{10}
\left(
\hat{y}^{n}
-
\left(
b+w\cdot x_{cp}^{n}
\right)
\right)^2
$$


- 利用梯度下降法，找到最佳的 \(b\) 和 \(w\)


$$
\boxed{b=-188.4,\qquad w=2.67}
$$

求偏导得到

$$
\frac{\partial L}{\partial w} = \sum_{n=1}^{10}(-2x^n_{cp})(\hat{y}^n-b-wx_{cp}^n)
$$


$$
\frac{\partial L}{\partial b} = \sum_{n=1}^{10}(-2)(\hat{y}^n-b-wx_{cp}^n)
$$

这样我们就可以写一个求梯度的函数
```python
def getGrad(b,w):
	# initial b_grad and w_grad
	b_grad = 0.0
	w_grad = 0.0
	# 计算梯度
	for i in range(len(x_data)):
		b_grad += -2 * (y_data[i] - b - w * x_data[i])
		w_grad += -2 * x_data[i] * (y_data[i] - b - w * x_data[i])
	
	return b_grad, w_grad
```

利用梯度下降法
```python
for i in range(iteration):

b_grad, w_grad = getGrad(b,w)

b -= lr * b_grad

w -= lr * w_grad
```
