# 在（移动）硬盘上安装 Ubuntu 简要教程

本文简要介绍如何将 Ubuntu 系统安装在一块外接硬盘或内置硬盘上，适用于有过操作经验者用于快速复现。

---

## 一、硬件 & 软件准备

- 一台运行 Windows 系统的电脑（本文使用 Windows 11）  
- 一块用于安装 Ubuntu 的硬盘（移动硬盘或内置硬盘均可）  
- 8GB 以上的 U 盘（用于制作启动盘）  
- [Ubuntu 官方](https://ubuntu.com/download/desktop)或[清华源下载](https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/)的系统镜像
- [Rufus 工具](https://rufus.ie/zh/)（用于制作启动盘）

---

## 二、制作启动盘

1. 将 U 盘插入电脑，打开 Rufus 软件  
2. 选择对应的设备（U 盘）  
3. 加载 Ubuntu 的 ISO 镜像文件  
4. 其余设置保持默认，点击“开始”写入  
5. 等待写入完成，即可得到一个可引导的 Ubuntu 启动盘  

---

## 三、安装系统

### 1. BIOS 设置  
进入 BIOS 设置界面，**关闭 Secure Boot（安全启动）**，保存并退出。

### 2. 引导安装程序  
重启电脑并通过快捷键进入启动项选择界面，选择 Ubuntu 启动盘启动。系统将引导进入安装界面。

### 3. 安装分区设置  
在安装类型界面中选择 **“其他选项”**，以便手动分区。建议设置如下（对Linux系统不区分主分区和逻辑分区）：

- **EFI 分区 `/boot`**：1GB，Ext4 格式  
- **Swap 交换分区**：一般为内存大小的1-2倍（**不挂载**）  
- **根目录 `/` 分区**：30GB 以上，Ext4 格式  
- **`/home` 分区**：剩余所有可用空间，Ext4 格式  

⚠️ 注意：**将引导加载器安装到 EFI 分区 `/boot`所在分区。**

---

## 四、重启系统

安装完成后，系统会提示你重启：

- **此时可以拔出 U 盘**
- **不要拔除 Ubuntu 所在的硬盘**

完成后即可通过该硬盘启动 Ubuntu 系统。

---

## 参考链接

- [Create a bootable USB stick with Rufus on Windows](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)  
- [Ubuntu 系统安装在移动固态硬盘，实现在不同电脑即插即用](https://blog.csdn.net/hypc9709/article/details/127941834?spm=1001.2014.3001.5506)  
- [移动硬盘安装 Ubuntu](https://www.cnblogs.com/consistency/p/17838414.html)  


