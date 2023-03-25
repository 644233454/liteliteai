export function copyToClipboard(textToCopy: string) {
  // navigator clipboard 需要https等安全上下文
  if (navigator.clipboard && window.isSecureContext) {
      return new Promise((res, rej) => {
        // 执行复制命令并移除文本框
        navigator.clipboard.writeText(textToCopy).then(()=>{
          res('成功了')
        }).catch(error=>{
          rej('失败了')
        })
    });
  } else {
      // 创建text area
      let textArea = document.createElement("textarea");
      textArea.value = textToCopy;
      // 使text area不在viewport，同时设置不可见
      textArea.style.position = "absolute";
      textArea.style.opacity = 0;
      textArea.style.left = "-999999px";
      textArea.style.top = "-999999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      return new Promise((res, rej) => {
          // 执行复制命令并移除文本框
          document.execCommand('copy') ? res('成功了') : rej('失败了');
          textArea.remove();
      });
  }
}
