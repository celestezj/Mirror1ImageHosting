/**
 * Minified by jsDelivr using Terser v5.7.1.
 * Original file: /gh/Tomotoes/js@master/log.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
!function() {
    if (window.console && window.console.log) {
        const e = (...e)=>setTimeout(console.log.bind(console, ...e));
        
        localStorage.getItem("access") || localStorage.setItem("access", (new Date).getTime());
        let o = new Date(Number.parseInt(localStorage.getItem("access")))
          , t = `${o.getFullYear()}年${o.getMonth() + 1}月${o.getDate()}日`
          , n = 0;
        localStorage.getItem("hit") ? n = Number.parseInt(localStorage.getItem("hit")) : localStorage.setItem("hit", 0),
        localStorage.setItem("hit", ++n),
        e(`PS: 这是你自 ${t} 以来第 ${n} 次在本站打开控制台，你想知道什么秘密嘛~`);
    }
}();
//# sourceMappingURL=/sm/33cf0d57569fd00ee3db2f268b264e1b30abc666a376a2d99feb1e97e4241215.map
