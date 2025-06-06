好的，下面详细介绍如何**本地引入 html2canvas**，让自动分块截图在没有外网的环境下也能用。

---

# 📦 本地引入 html2canvas 步骤

## 1. 下载 html2canvas 库文件

1. 用有网络的电脑访问  
   [https://html2canvas.hertzen.com/dist/html2canvas.min.js](https://html2canvas.hertzen.com/dist/html2canvas.min.js)
2. 右键页面内容，选择“另存为”，保存为 `html2canvas.min.js`
3. 将 `html2canvas.min.js` 拷贝到你的项目目录（建议放在 `destination/` 或 `code/` 目录下）

---

## 2. 修改 HTML 文件，添加本地 JS 引用

以 `destination/hefei_liuan_guide.html` 为例：

1. 用文本编辑器打开 `destination/hefei_liuan_guide.html`
2. 在 `<head>` 标签内添加一行：

   ```html
   <script src="html2canvas.min.js"></script>
   ```

   > 如果你把 `html2canvas.min.js` 放在 `destination/` 目录下，直接如上写法即可。  
   > 如果放在别的目录，比如 `code/`，则写成 `<script src="../code/html2canvas.min.js"></script>`

3. 保存文件

---

## 3. 使用自动分块截图代码（本地版）

1. 打开 `destination/hefei_liuan_guide.html`，按 F12 打开开发者工具，切换到 Console
2. 粘贴以下代码（**注意：已去除自动加载部分**）：

```javascript
// 本地版自动分块截图
(function(){
    if (typeof html2canvas !== 'function') {
        alert('html2canvas 加载失败，请检查 <script src=\"html2canvas.min.js\"> 是否已正确引入！');
        return;
    }
    const sections = document.querySelectorAll('.header, .content-section, footer');
    console.log(`找到 ${sections.length} 个内容块`);
    let index = 0;
    function captureNext() {
        if (index >= sections.length) {
            console.log('🎉 所有截图完成！');
            return;
        }
        const section = sections[index];
        console.log(`正在截取第 ${index + 1} 个内容块...`);
        html2canvas(section, {
            backgroundColor: '#ffffff',
            useCORS: true,
            scale: 1.5
        }).then(canvas => {
            const link = document.createElement('a');
            link.download = `hefei_liuan_guide_${String(index + 1).padStart(2, '0')}.png`;
            link.href = canvas.toDataURL('image/png', 0.9);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            console.log(`✅ 第 ${index + 1} 张下载完成`);
            index++;
            setTimeout(captureNext, 1000);
        }).catch(e => {
            console.error(`❌ 第 ${index + 1} 张失败:`, e);
            index++;
            setTimeout(captureNext, 1000);
        });
    }
    captureNext();
})();
```

---

## 4. 执行截图

- 按回车，等待图片自动下载
- 检查浏览器下载文件夹，将图片移动到 `D:\share\python\trea\eye\0606`

---

## 5. 常见问题

- **图片下载不了？**  
  检查 `<script src="html2canvas.min.js"></script>` 路径是否正确，Console 是否有报错。
- **图片内容不完整？**  
  可适当调整 `scale` 参数（如 2），或手动调整浏览器窗口宽度。
- **部分内容渲染异常？**  
  html2canvas对极个别复杂样式支持有限，建议分块截图。

---

## 总结

- 本地引入 html2canvas 可以完全脱离外网，适合内网、无网环境。
- 只需下载一次 js 文件，后续所有 HTML 都可复用。
- 自动分块截图效率高，图片美观。

如需自动化批量处理多个 HTML 或有特殊需求，也可以继续提问！
