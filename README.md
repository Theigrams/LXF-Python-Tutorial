# LXF Python Tutorial
##  简介

本项目通过爬虫下载 [廖雪峰Python教程](https://www.liaoxuefeng.com/wiki/1016959663602400) ，并将下载的markdown文件转化为LaTeX，最终编译成PDF。



## 前言

最近在看廖雪峰老师的[Python教程](https://www.liaoxuefeng.com/wiki/1016959663602400)，个人感觉写得非常简炼，并且还有在线编程练习，于是产生了将其整理成PDF方便离线查看的想法。

> 下载链接为：https://github.com/Theigrams/LXF-Python-Tutorial/releases/tag/1.0

整个过程一共分为两步：

1. 将网页内容下载成markdown文件
2. 将markdown文件转化成LaTeX，然后编译成PDF



## 爬虫下载

### 获取网址

首先，我们要找到全部的网址，先进入首页https://www.liaoxuefeng.com/wiki/1016959663602400，然后F12进入开发者模式。

![image-20210216214024925](http://pic.theigrams.cn/20210216214032.png?imagslim)

然后查看侧边栏的目录，其 `class="uk-nav uk-nav-side"`，于是用爬虫获取对应信息，因为该网站开启了反爬机制，所以要加上一个headers信息。

```python
from bs4 import BeautifulSoup as bs
import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

response = requests.get("https://www.liaoxuefeng.com/wiki/1016959663602400",headers = headers)  
soup = bs(response.content, "html.parser")  
menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]  
```

`menu_tag` 中储存的内容如下：

```html
>>> print(menu_tag)

<ul class="uk-nav uk-nav-side" id="x-wiki-index" style="margin-right:-15px;">

<div depth="0" id="1016959663602400" style="position:relative;margin-left:15px;">
<i class="uk-icon-plus-square-o" onclick="toggleWikiNode(this)" style="position:absolute;margin-left:-1em;padding-top:8px;"></i>
<a class="x-wiki-index-item" href="/wiki/1016959663602400">Python教程</a>

    <div depth="1" id="1016959735620448" style="display:none;position:relative;margin-left:15px;">
    <a class="x-wiki-index-item" href="/wiki/1016959663602400/1016959735620448">Python简介</a>
    </div>

    <div depth="1" id="1016959856222624" style="display:none;position:relative;margin-left:15px;">
    <i class="uk-icon-plus-square-o" onclick="toggleWikiNode(this)" style="position:absolute;margin-left:-1em;padding-top:8px;"></i>
    <a class="x-wiki-index-item" href="/wiki/1016959663602400/1016959856222624">安装Python</a>

        <div depth="2" id="1016966024263840" style="display:none;position:relative;margin-left:15px;">
        <a class="x-wiki-index-item" href="/wiki/1016959663602400/1016966024263840">Python解释器</a>
        </div>
...
```

我们查找全部 `div` 节点的信息，进入下一级的 `a` 节点，然后从中获取 `href` 和文本信息：

```python
urls=[]
dep=[0,0,0,0]
titles=[]
for li in menu_tag.find_all("div"):  
    url = "http://www.liaoxuefeng.com" + li.a.get('href')  
    urls.append(url)
    i=int(li['depth'])
    dep[i]+=1
    for a in range(i+1,4):
        dep[a]=0
    titles.append('{:0=2d}.{}.{}{}'.format(dep[1],dep[2],dep[3],li.a.string))
```

这里用 `urls` 储存网址，`titles` 储存标题，`dep` 储存层级，输出结果如下：

```python
>>> urls

['http://www.liaoxuefeng.com/wiki/1016959663602400',
 'http://www.liaoxuefeng.com/wiki/1016959663602400/1016959735620448',
 'http://www.liaoxuefeng.com/wiki/1016959663602400/1016959856222624',
 'http://www.liaoxuefeng.com/wiki/1016959663602400/1016966024263840',
 ...
 'http://www.liaoxuefeng.com/wiki/1016959663602400/1019418790329088',
 'http://www.liaoxuefeng.com/wiki/1016959663602400/1018492034821792']
```

```python
>>> titles

['00.0.0Python教程',
 '01.0.0Python简介',
 '02.0.0安装Python',
 '02.1.0Python解释器',
 ...
 '26.0.0FAQ',
 '27.0.0期末总结']
```

### md下载

要将网页下载成markdown格式，Python有很多库都能做到，但我们要精准获取网页正文内容，这就比较麻烦，最简单的方法就是使用浏览器的一些剪辑插件。

这里，我选择了`简悦`，在进入阅读模式之后，就能导出md文件，整个动作流程分图中4步：

![image-20210216221309560](http://pic.theigrams.cn/20210216221309.png?imagslim)

这里我们使用 `selenium` 库来模仿鼠标操作即可。

但第一个难题是 **如何点击插件按钮**，因为`selenium` 库只能处理网页内容，对于浏览器中的按钮就无能为力了，这里有两个解决方案：

1. 自己先设置进入阅读模式的快捷键，然后使用 `pyautogui` 库模拟输入快捷键。
2. `pyautogui` 有个很强大的功能：可以在当前屏幕搜索指定图片的位置，然后点击即可。

两个方案的代码分别如下：

```python
# 方案一
pyautogui.click(800, 800)	# 先点一下其他地方
pyautogui.hotkey('ctrl', 'q')	# 然后输入快捷键

# 方案二
image_path=r'C:\Users\Theigrams\Desktop\aa.png'	# 截图存好的图标
img_location = pyautogui.locateOnScreen(image_path, confidence=0.6)
image_location_point = pyautogui.center(img_location)
x, y = image_location_point	# 获得位置
pyautogui.click(x, y)	# 点击一下
```

方案一最简单，但如果没有快捷键就GG了，所以方案二通用性更好。



然后按步骤来就好：

```python
option = webdriver.ChromeOptions()
option.add_argument("--user-data-dir="+r"C:/Users/Theigrams/AppData/Local/Google/Chrome/User Data/")
browser = webdriver.Chrome(chrome_options=option)

# 步骤2，将光标移动到三个点处
anchor_button=browser.find_element_by_xpath('//*[@id="anchor"]')
ActionChains(browser).move_to_element(anchor_button).perform()

# 步骤3，将光标移动到“动作”处
act_button=browser.find_element_by_xpath('/html/div/sr-read/sr-rd-crlbar/fap/panel-bg/panel/panel-tabs/panel-tab[2]/span')
ActionChains(browser).move_to_element(act_button).perform()

# 步骤4，点击按钮下载
md_button=browser.find_element_by_xpath("/html/div/sr-read/sr-rd-crlbar/fap/panel-bg/panel/panel-groups/panel-group[2]/action-bar/sr-opt-gp[3]/actions/a[5]/button-mask/button-span")
md_button.click()
```

### 整理md文件

接下来是按 `titles` 格式批量重命名下载文件，然后看如果有些小问题就手动修改了。

然后是将md中的网络图片链接转化为本地链接：

1. 根据正则表达式匹配网络图片链接
2. 先将图片下载到fig文件夹中并重命名
3. 将网络图片链接转化为本地链接

```python
import wget
import os

os.getcwd()
md_path=r'C:\Users\Theigrams\Desktop\lxf_python\md'
os.chdir(md_path)
md_list=os.listdir()
md_list.remove('fig')

for md in md_list:
    contents = []
    with open(md,'r', encoding='utf-8') as f:
        md_file=f.read()
        re_img=re.compile(r'\!\[\]\((.{1,}?)\)')
        imgs=re_img.findall(md_file)
        for img in imgs:
            img_name=img.split('attachments')[1].replace(r'/','')+'.png'
            path=r'fig\\'+img_name
            if not os.path.isfile(path):
                wget.download(img, path)
            md_file=re.sub(img, r'\\fig\\'+img_name,md_file)
        contents.append(md_file)
    with open(md, "w",encoding='utf-8') as f:
        f.writelines(contents)
```





## MD转LaTeX

Markdown转LaTeX，最好用的方法是使用 `pandoc`，但默认的转化样式很简陋，这里安利一个模板 [Eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template)，转化出来的效果非常好。

```cmd
pandoc "document.md" -o "document.tex" --from markdown --template "eisvogel.tex" --highlight-style kate --pdf-engine "xelatex" -V CJKmainfont="SimSun"
```

但这个大佬写的模板代码我看不懂，不好自己修改，于是只能自己折腾。



### 朴素转化

pandoc默认转化出来是自带样式的，也就是导言区定义了一堆东西，能直接编译成PDF。

但我只需要最朴素的转化，因为样式可以由自己定义。

```cmd
pandoc "document.md" -o "document2.tex" --from markdown -t latex
```

例如对于下面这样一个md文件，

![image-20210216225252563](http://pic.theigrams.cn/20210216225252.png?imagslim)

前者转化出来足足有300多行，但后者只有26行，非常简洁，这正是我们想要的。

![image-20210216225537972](http://pic.theigrams.cn/20210216225538.png?imagslim)

### 自定义样式

首先是代码框，使用 `minted` 宏包高亮，这本来没什么，但廖老师喜欢搞一些骚操作，比如经常用`代码字符`来展示一些东西。。。

![image-20210216230811449](http://pic.theigrams.cn/20210216230811.png?imagslim)

这就把我坑惨了，因为这些特殊字符 LaTeX 没法显示出来。。。

minted 还用红框标注了这些错误字符。。。

![image-20210216232303736](http://pic.theigrams.cn/20210216232303.png?imagslim)

最后还是在万能的 stackexchange 中找到了解决办法：[minted : changing fontfamily to support UTF8 chars](https://tex.stackexchange.com/questions/159363/minted-changing-fontfamily-to-support-utf8-chars)

方法是使用 `CMU Typewriter Text` 字体。

然后按这个方法 [Minted red box around greek characters](https://tex.stackexchange.com/questions/343494/minted-red-box-around-greek-characters) 消除红框：

```latex
\AtBeginEnvironment{minted}{%
  \renewcommand{\fcolorbox}[4][]{#4}}
```

最后终于正常了.......了个鬼，还是有些特殊字符不能显示，例如下图中 “终端最大化” 那个符号就没能正常显示。。。

![image-20210216233112935](http://pic.theigrams.cn/20210216233113.png?imagslim)

其实使用 `Source Code Pro` 字体倒是能正常显示的，但这个字体太大了，会导致`行内代码` 看起来比正文大，显示不协调。。。算了，不折腾了，就这样吧。



然后修改了一下`行内代码` 的样式，看起来还不错

```latex
\usepackage{xcolor}
\usepackage{soul}
\definecolor{Light}{RGB}{251,234,236}
\sethlcolor{Light}
% 设置 \texttt 红色样式
\let\oldtexttt\texttt 
\renewcommand{\texttt}[1]{\colorbox{Light}{\ttfamily \textcolor{red}{#1}}}
```



## 最终效果

最终效果如下：

![image-20210217000756869](http://pic.theigrams.cn/20210217000756.png?imagslim)

## Github地址

整个代码和PDF都放在了Github上：https://github.com/Theigrams/LXF-Python-Tutorial