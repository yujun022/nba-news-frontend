document.addEventListener("DOMContentLoaded", function () {
    // 載入新聞列表
    fetch("http://127.0.0.1:8000/news") // 你的後端 API
        .then(response => response.json())
        .then(data => {
            const newsList = document.getElementById("news-list");
            data.forEach(news => {
                const li = document.createElement("li");
                const a = document.createElement("a");
                a.href = news.link;
                a.textContent = news.title;
                a.target = "_blank";
                li.appendChild(a);
                newsList.appendChild(li);
            });
        })
        .catch(error => console.error("Error fetching news:", error));

    // 處理新增新聞表單提交
    document.getElementById("news-form").addEventListener("submit", function (event) {
        event.preventDefault(); // 防止表單自動提交

        // 獲取表單資料
        const title = document.getElementById("title").value;
        const link = document.getElementById("link").value;

        // 構造新聞資料
        const newsData = { title, link };

        // 發送 POST 請求到後端 API
        fetch("http://127.0.0.1:8000/news", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newsData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("新增成功:", data);
            // 重新載入新聞列表
            loadNews();
        })
        .catch(error => console.error("新增失敗:", error));
    });

    // 函式：載入新聞
    function loadNews() {
        fetch("http://127.0.0.1:8000/news")
            .then(response => response.json())
            .then(data => {
                const newsList = document.getElementById("news-list");
                newsList.innerHTML = ''; // 清空列表
                data.forEach(news => {
                    const li = document.createElement("li");
                    const a = document.createElement("a");
                    a.href = news.link;
                    a.textContent = news.title;
                    a.target = "_blank";
                    li.appendChild(a);
                    newsList.appendChild(li);
                });
            })
            .catch(error => console.error("Error fetching news:", error));
    }

    // 初次載入新聞列表
    loadNews();
});


