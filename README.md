# 携程酒店评论爬虫文档

## 概述

该脚本是一个Python爬虫，用于从携程网站上爬取酒店评论。它使用Selenium库与Chrome浏览器进行交互，模拟用户浏览酒店评论页面并提取数据。

## 环境配置

在运行此脚本之前，需要确保您的环境中安装了以下组件：

- Python 3
- Selenium库
- Chrome浏览器
- Chrome WebDriver

您可以使用pip安装Selenium库：

```bash
pip install selenium
```

Chrome WebDriver应与您的Chrome浏览器版本相对应，并放置在可执行路径中。

## 使用方法

1. 确保您已按照上述“环境配置”安装所有必要的软件和库。
2. 将脚本保存到您的计算机上。
3. 修改脚本中的`hotels`列表，包含您想要爬取评论的酒店名称和对应的携程网址。
4. 在脚本所在目录下打开命令行工具或使用IDE直接运行。
5. 运行脚本：

```bash
python <脚本名称>.py
```

## 脚本功能

- **日志配置**：配置日志记录，包括日志级别、格式和输出文件。
- **浏览器选项配置**：设置ChromeOptions，以便在爬虫运行时模拟正常用户的行为。
- **提取评论信息**：从每个评论卡片中提取用户头像、用户名、房间类型、入住信息、家庭信息、评论信息、评分、评论内容、有用计数、评论日期和酒店回复。
- **保存数据为JSON**：将提取的评论信息保存为JSON文件。
- **创建数据文件夹**：在指定的父文件夹中创建一个文件夹，用于存储JSON数据文件。
- **主功能**：遍历提供的酒店列表，访问每个酒店的评论页面，提取评论并保存数据。

## 代码解释

### 初始化浏览器

```python
option = ChromeOptions()
option.add_argument(r"user-data-dir=D:\AppData\AppData\Local\Google\Chrome\User Data")
...
browser = webdriver.Chrome(options=option)
```

这部分代码初始化了一个Chrome浏览器实例，配置了用户数据目录和其他防反爬虫的选项。

### 提取评论信息

```python
def extract(review_cards):
    ...
    for card in review_cards:
        ...
        all_reviews.append({...})
    ...
```

`extract`函数遍历每个评论卡片，提取所需的信息，并将它们保存在字典中，然后将这些字典添加到一个列表中。

### 保存数据

```python
def save2json(data, file_path):
    ...
```

`save2json`函数将提取的评论数据以JSON格式保存到指定的文件路径。

### 创建文件夹

```python
def create_folder(parent_folder_name, folder_name):
    ...
```

`create_folder`函数在指定的父文件夹中创建一个新文件夹，如果文件夹已存在，则不会重复创建。

### 主函数

```python
def main(hotels):
    ...
```

`main`函数是脚本的入口点，它遍历酒店列表，访问每个酒店的评论页面，并调用其他函数来提取评论数据和保存为JSON。

