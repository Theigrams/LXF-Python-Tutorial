#%%
from subprocess import Popen, PIPE, STDOUT
import re
import os

#%%
os.getcwd()
md_path=r'C:\Users\Theigrams\Desktop\lxf_python\md'
tex_path=r'C:\Users\Theigrams\Desktop\lxf_python\tex'
os.chdir(md_path)
md_list=os.listdir()
md_list.remove('fig')

#%%
import wget

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

#%%
import shutil
shutil.rmtree(tex_path+'\\fig')
shutil.copytree(md_path+'\\fig', tex_path+'\\fig')
#%%
os.chdir(md_path)
for md in md_list:
    in_md=md
    tex=md.replace('.md','.tex')
    out_tex='..\\tex\\'+tex
    p = Popen(['pandoc',in_md,'-o',out_tex, '-f', 'markdown', '-t', 'latex'])

# %%
os.chdir(tex_path)
tex_list=os.listdir()
tex_list=list(filter(lambda x:x[-3:]=='tex',tex_list))
tex_list.remove('gen.tex')
tex_list.remove('hd.tex')
for tex in tex_list:
    contents = []
    with open(tex,'r', encoding='utf-8') as f:
        tex_file=f.read()
        tex_file=re.sub(r'\\tightlist\n', r'', tex_file)
        re_img=re.compile(r'\\includegraphics\{(.{1,}?)\}')
        fig=r" \n \\begin{figure}[htp]\n\t\\centering\n\t\\includegraphics[width=0.6\\linewidth]{\1}\n\\end{figure}\n"
        tex_file2=re_img.sub(fig,tex_file)
        tex_file2=tex_file2.replace(r'/fig','fig')
        tex_file2=tex_file2.replace(r'verbatim','pythoncode')
        # tex_file2=tex_file2.replace(r'pythoncode','pythoncode')
        contents.append(tex_file2 +"\n")
        
    with open(tex, "w",encoding='utf-8') as f:
        f.writelines(contents)


#%%
for t in tex_list:
    if t.split('.')[1]=='0':
        print('\n')
        print(r'\newpage')
        print(r'\section{%s}' % t.split('.')[2][1:])
        print(r'\input{%s}' % t)
    else:
        print(r'\newpage')
        print(r'\input{%s}' % t)

