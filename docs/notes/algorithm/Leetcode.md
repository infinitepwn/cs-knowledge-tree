# Leetcode

> 来源：`算法设计与分析 / Leetcode.md`

诚然在AI时代，刷Leetcode似乎没什么意义了，但是作为一个保持大脑活跃的工具还是不错的
## Two sums
You are given an array of integers `nums` and an integer `target`, return _indices of the two numbers such that they add up to `target`_.

You may assume that each input would have **_exactly_ one solution**, and you may not use the _same_ element twice.

You can return the answer in any order.

**Example 1:**

**Input:** nums = [2,7,11,15], target = 9
**Output:** [0,1]
**Explanation:** Because nums[0] + nums[1] == 9, we return [0, 1].

**Example 2:**

**Input:** nums = [3,2,4], target = 6
**Output:** [1,2]

**Example 3:**

**Input:** nums = [3,3], target = 6
**Output:** [0,1]

**Constraints:**

- `2 <= nums.length <= 104`
- `-109 <= nums[i] <= 109`
- `-109 <= target <= 109`
- **Only one valid answer exists.**

**Follow-up:** Can you come up with an algorithm that is less than `O(n2)` time complexity?

我的思路就是，固定其中一个元素，然后只需要搜索target扣除掉这个元素之后的数是否在数组中就行了，只需要一个search函数
``` C
class Solution {
public:
int search(vector<int> nums,int num,int pos)
{

	for(int i = 0;i < nums.size();i++)
	{
		if(num == nums[i] and i != pos)
		{
		return i;
		}
	}
	return -1;
}
vector<int> twoSum(vector<int>& nums, int target) {
	vector<int> indice;
	for(int i = 0;i < nums.size();i++)
	{
		int res = search(nums,target-nums[i],i);
		if(res != -1)
		{
			indice.push_back(i);
			indice.push_back(res);
			break;
		}
	}
	return indice;
	}
};
```
当然这个肯定是非常慢的
![image.png|343](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20260904134013982.png)
### AI评价
整体来说：思路正确，能通过 LeetCode「两数之和」，而且你考虑到了不能重复使用同一个元素 `i != pos`。作为入门写法是合格的。

不过有一个明显的性能问题：`search()` 每次都会遍历数组，而 `twoSum()` 也在遍历数组，所以：

- 时间复杂度：O(n^2)
    
- 额外空间复杂度：O(1)O(1)，不计算返回结果
    
- `nums` 在 `search()` 中按值传递，每次调用都会复制整个数组，产生额外开销
    

你这里：

```cpp
int search(vector<int> nums, int num, int pos)
```

至少应该改成常量引用：

```cpp
int search(const vector<int>& nums, int num, int pos)
```

这样不会复制数组，也能保证函数不会修改 `nums`。

你的代码可以小改为：

```cpp
class Solution {
public:
    int search(const vector<int>& nums, int num, int pos) {
        for (int i = 0; i < nums.size(); i++) {
            if (num == nums[i] && i != pos) {
                return i;
            }
        }
        return -1;
    }

    vector<int> twoSum(vector<int>& nums, int target) {
        for (int i = 0; i < nums.size(); i++) {
            int res = search(nums, target - nums[i], i);

            if (res != -1) {
                return {i, res};
            }
        }

        return {};
    }
};
```

这里还有几个小优化：

1. C++ 中更常用 `&&`，虽然 `and` 完全合法，但较少见。
2. 没必要先创建 `indice` 再 `push_back`，找到答案后可以直接 `return {i, res}`。
3. `indices` 才是“索引”的复数，`indice` 不是常见英文写法。
4. `nums.size()` 返回的是无符号类型，严谨写法可以使用 `size_t`。
    
![image.png|433](https://raw.githubusercontent.com/infinitepwn/note_picbed/main/20260904134119391.png)
这样的空间复杂度就下降了很多

我们分析主要的时间开销在于查找都是\(O(n)\),可以用哈希表来把查找时间降为常数级
更推荐使用哈希表，把时间复杂度降到 O(n)：

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;

        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];

            if (seen.count(complement)) {
                return {seen[complement], i};
            }

            seen[nums[i]] = i;
        }

        return {};
    }
};
```

它的逻辑是：遍历到 `nums[i]` 时，检查之前是否出现过 `target - nums[i]`。

例如：

```text
nums = [2, 7, 11, 15]
target = 9
```

- 看到 `2`：需要 `7`，但此前没有；记录 `2 → 0`
- 看到 `7`：需要 `2`，此前已经记录；返回 `{0, 1}`

## 3Sums
Given an integer array nums, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

**Example 1:**

**Input:** nums = [-1,0,1,2,-1,-4]
**Output:** [[-1,-1,2],[-1,0,1]]
**Explanation:** 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

**Example 2:**

**Input:** nums = [0,1,1]
**Output:** []
**Explanation:** The only possible triplet does not sum up to 0.

**Example 3:**

**Input:** nums = [0,0,0]
**Output:** 0,0,0
**Explanation:** The only possible triplet sums up to 0.

**Constraints:**

- `3 <= nums.length <= 3000`
- `-105 <= nums[i] <= 105`
``` Cpp
class Solution {

public:

void sort(vector<int>& nums)

{

for(int i = 0;i < nums.size(); i++)

{

for(int j = i + 1 ;j < nums.size();j++)

{

if(nums[j]<nums[i])

{

int temp = nums[i];

nums[i] = nums[j];

nums[j] = temp;

}

}

}

}

vector<vector<int>> threeSum(vector<int>& nums) {

sort(nums);

  

vector<vector<int>> ans;

int n = static_cast<int>(nums.size());

  

for (int i = 0; i < n - 2; i++) {

// 最小的数已经大于 0，后面不可能凑出 0

if (nums[i] > 0) {

break;

}

  

// 跳过重复的第一个数

if (i > 0 && nums[i] == nums[i - 1]) {

continue;

}

  

int left = i + 1;

int right = n - 1;

  

while (left < right) {

long long sum =

static_cast<long long>(nums[i]) +

nums[left] +

nums[right];

  

if (sum < 0) {

left++;

} else if (sum > 0) {

right--;

} else {

ans.push_back({

nums[i],

nums[left],

nums[right]

});

  

// 跳过与当前 left 相同的数字

while (left < right &&

nums[left] == nums[left + 1]) {

left++;

}

  

// 跳过与当前 right 相同的数字

while (left < right &&

nums[right] == nums[right - 1]) {

right--;

}

  

left++;

right--;

}

}

}

  

return ans;

}

};
```
### 双指针法

双指针可以把\(O(n^2)\)的复杂度变成\(O(n)\)

|类型|移动方式|常见用途|
|---|---|---|
|相向双指针|两端向中间移动|两数之和、三数之和、回文判断|
|快慢指针|同方向、速度不同|链表环、寻找链表中点|
|读写指针|一个读取，一个写入|删除元素、数组去重、移动零|
|滑动窗口|左右指针维护区间|最长子串、最短子数组|

判断一道题能否使用双指针，可以想三个问题：

1. 数据是否有序，或者能否先排序？
2. 移动某个指针后，能否确定排除一批不可能的答案？
3. 是否需要维护一个连续区间或压缩数组？

双指针最重要的并不是“定义两个变量”，而是：**每移动一次指针，都必须有充分理由排除一部分不可能的情况。**