import tkinter as tk
from tkinter import messagebox
import subprocess
from tkinter import ttk

# 设置目标网站列表
webdic = {'人民网':'RenMinWang',
          '民政局':'MinZhengJu',
          '长安网':'ChangAnWang',
          '卫健委':'WeiJianWei'}
weblst = list(webdic.keys())

# 定义“开始爬虫”按钮函数
def run_crawler():
    
    # 检查目标网站
    target = combobox.get()
    if  target not in weblst:
        text_output.insert(tk.END, '请选择正确的目标网站！' + '\n')
        text_output.see(tk.END) 
        return False
    
    # 获取用户输入的关键词和迭代次数
    keyword = entry_keyword.get()
    maxpage = entry_iterations.get()

    # 根据用户指定目标网站选择子进程文件
    file_path = '{}.py'.format(webdic[target])
    
    try:
        result = subprocess.run([file_path, 
                                "--keyword",
                                keyword,
                                "--maxpage",
                                maxpage], 
                                check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        text_output.insert(tk.END, output + '\n')
        text_output.see(tk.END) 
    except subprocess.CalledProcessError as e:
        messagebox.showerror('错误', '无法运行爬虫程序')
        text_output.insert(tk.END, e.stderr.strip() + '\n')
        text_output.see(tk.END) 


###########################下为主函数##############################

# 创建主窗口
window = tk.Tk()
window.title("爬虫程序")
window.geometry("300x300")

# 创建关键词输入框
label_keyword = tk.Label(window, text="搜索词：")
label_keyword.pack()
entry_keyword = tk.Entry(window)
entry_keyword.pack()

# 创建迭代次数输入框
label_iterations = tk.Label(window, text="爬取页数：")
label_iterations.pack()
entry_iterations = tk.Entry(window)
entry_iterations.pack()

# 创建下拉选项组件
label = ttk.Label(window, text="选择目标网站")
label.pack(pady=5)
combobox = ttk.Combobox(window, value=weblst, text="选择目标网站")
combobox.pack()

# 创建运行按钮
btn_run = tk.Button(window, text="运行爬虫", command=run_crawler)
btn_run.pack(pady=20)

# 创建输出文本框
text_output = tk.Text(window, height=50)
text_output.pack()

# 运行主循环
window.mainloop()
