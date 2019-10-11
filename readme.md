# python调用word2vec工具包安装和使用指南

## word2vec pythin-toolkit installation and use tutorial

[本文选译自英文版](https://github.com/danielfrg/word2vec)，代码注释均摘自本文，建议先阅读[skip-model相关知识](http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/)再阅读本指南

### 环境准备

1. 安装gcc, 安装gcc坑比较多，这里建议使用codeblocks自带的gcc编译器，下载[地址](http://www.codeblocks.org/downloads/26)，这里注意，一定要点击codeblocks-mingw版本，安装完成后设置环境变量Path, INCLUDE, LIB
2. 尝试安装：`pip install word2vec`, 观察报错情况，这里有几种解决方法，我遇到的报错是`Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": https://visualstudio.microsoft.com/downloads/` 解决方法是下载microsoft vc++[下载指南](https://blog.csdn.net/u012247418/article/details/82314129), 还有其他可能的错误，链接如下：[报错列表](https://blog.csdn.net/BEYONDMA/article/details/88381650)，题外话：安装python工具包时，先查阅[pypi](https://pypi.org/)，可以避免一些错误

### 模型的训练

​       导入模型`import word2vec`

1. 同义词合并，例如michael jacson和 michael-jackson 

   ```python
   word2vec.word2phrase('./txt_file/text8', './txt_file/text8-phrases', verbose=True)
   ```

   

2. 训练skip-gram model， 得到word2vec词向量表示，size为向量的维数

   ```python
   word2vec.word2vec('/Users/drodriguez/Downloads/text8-phrases', '/Users/drodriguez/Downloads/text8.bin', size=100, verbose=True)
   ```

   

3. 输出`text8.bin`文件，包含二进制形式的词向量组

4. 词向量的应用：单词聚类，产生`text8-clusters.txt`包含所有单词的聚类结果, 结果数目小于等于单词表数目

   ```python
   word2vec.word2clusters('/Users/drodriguez/Downloads/text8', '/Users/drodriguez/Downloads/text8-clusters.txt', 100, verbose=True)
   ```

### model模型的使用

1. 导入刚才产生的模型

   ```python
   model = word2vec.load('/Users/drodriguez/Downloads/text8.bin')
   ```

2. model的属性 `model.vocab`, 得到单词表的numpy.array格式，这里的单词不是词向量形式

3. `model.vectors`是模型的矩阵，n为单词数目，m为词向量长度，`vectors`为n*m维

4. 可以通过`model['dog'].shape`或者`model['dog'][:10]`来访问某一个单词的词向量信息

5. 计算几个词向量两两之间的距离：`model.distance("dog", "cat", "fish")`

6. 得到某一个单词的相似词（基于余弦相似度）：`indexes, metrics = model.similar("dog")`,第一个返回值为相似向量的下标，第二个为相似度，都为tuple格式，得到相应的单词可使用`model.vocab[indexes]`

7. 得到相似词的统计信息：（词，相似度）`model.generate_response(indexes, metrics)`，还可以使用`model.generate_response(indexes, metrics).tolist()`来转换得到python数据类型

8. 词向量直接加减运算：`indexes, metrics = model.analogy(pos=['king', 'woman'], neg=['man'])`,返回值和`generate_response method`相同

   

### cluster模型的使用

1. 导入cluster模型

   ```python
   clusters = word2vec.load_clusters('/Users/drodriguez/Downloads/text8-clusters.txt')
   ```

2. 得到某一组结果`clusters.get_words_on_cluster(90)`，结果为这一组的所有单词

### cluster和model的结合使用

1. 将cluster添加到word2vec model中

   ```python
   model.clusters = clusters
   ```

2. 进行类似的加减分析：`indexes, metrics = model.analogy(pos=["paris", "germany"], neg=["france"])`

3. 得到结果后，`model.generate_response(indexes, metrics).tolist()`，得到(单词，相似程度，所属组号)