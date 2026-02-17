
# Windows 11 系统安装简明教程

本文简明扼要地介绍如何从头安装 Windows 11，包括制作系统 U 盘、引导设置、磁盘格式转换及安装过程等关键步骤，主要适用于有操作经验者用于快速复现。

---

## 一、制作系统安装盘

建议使用容量在 **16GB** 以上的 U 盘用于制作系统安装盘。在操作前请确保该 U 盘数据已备份，因为制作过程将**清空其内容**。

1. 访问 [微软 Windows 11 官方下载页面](https://www.microsoft.com/zh-cn/software-download/windows11)。
2. 选择 **“创建 Windows 11 安装媒体”** 下载，文件名通常为 `mediacreationtool.exe`。
3. 运行该工具，按照提示依次选择 **U 盘作为目标设备**。
4. 系统将自动下载并写入 Windows 11 安装文件，整个过程通常需十几分钟。

---

## 二、设置启动顺序与进入安装程序

系统盘制作完成后，将其插入目标电脑的 USB 接口。

- 启动电脑时，需要按下启动快捷键（视品牌和主板而定，可参考主板说明书或品牌文档）进入 **引导选择菜单**。
- 选择系统安装盘启动（通常根据 U 盘品牌名识别）。
- 成功引导后，会看到熟悉的 Windows 安装界面。

---

## 三、Windows 安装界面

1. **选择网络环节**  
   此时因未安装网卡驱动，通常无法联网，应选择 **“我没有互联网”**。  
   若无此选项，可先按 `Shift + F10` 打开命令行，输入以下指令跳过网络设置：

   ```cmd
   oobe\bypassnro
   ```

2. **输入产品密钥**  
   若尚未购买产品密钥，可选择 **“我没有产品密钥”**，后续可在系统内激活。

3. **选择操作系统版本**  
   通常建议选择 **“专业版”**，功能完整且适用范围广。

---

## 四、网卡驱动安装

Windows 安装程序会自动将系统文件复制到目标磁盘并开始部署安装。期间电脑会重启几次，随后进入熟悉的 Windows 11 图形界面。

此时电脑中仍未安装网卡驱动：

- 建议在另一台电脑上搜索本机所用网卡的驱动程序。
- 使用 U 盘将驱动程序拷贝至本机进行安装。
- 由于网卡型号众多，具体操作请读者自行搜索对应解决方案。



---
## 五、安装完成后配置建议

### 1. 系统激活与 Office 激活

可使用 [massgrave.dev](https://massgrave.dev/) 提供的激活脚本，在命令行输入以下命令：

```cmd
irm https://massgrave.dev/get | iex
```

- 回车后选择 `1` 即可激活 Windows。
- 安装 Office 后选择 `2` 即可激活 Office。



### 2. 恢复经典右键菜单（Win10 风格）

输入以下注册表命令后重启系统：

```cmd
reg.exe add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve
```

### 3. 显示桌面常用图标

右键桌面 → 个性化 → 主题 → 桌面图标设置


## 参考链接

1. [超级详细的 Windows 11 安装图解教程（2023年版），附优化建议](https://www.zhihu.com/tardis/zm/art/423873028?source_id=1003)  

2. [无法完成 Windows 11 安装时如何跳过“连接网络”页面](https://www.intel.cn/content/www/cn/zh/support/articles/000092599/intel-nuc.html)  

3. [Microsoft Activation Scripts (MAS)](https://massgrave.dev/)  
