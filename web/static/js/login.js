window.onload = function () {   // 保证下面代码在网页加载完成后再执行。这样可以避免在网页未加载完成时，无法找到“.btn”等元素无法找到
// 获取登录按钮和输入框的元素
    const loginBtn = document.querySelector('.btn');
    const usernameInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');

    function login() {
        // 获取用户名和密码
        const username = usernameInput.value;
        const password = passwordInput.value;

        // 创建 XMLHttpRequest 对象
        const xhr = new XMLHttpRequest();

        // 设置请求方式和 URL
        xhr.open('POST', '/check_login');

        // 设置请求头部信息
        xhr.setRequestHeader('Content-Type', 'application/json');

        // 构建请求体
        const requestBody = JSON.stringify({
            username: username,
            password: password
        });

        // 发送请求
        xhr.send(requestBody);

        // 监听请求状态的变化
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // 解析响应体
                    const response = JSON.parse(xhr.responseText);
                    if (response.code === 200) {
                        // 普通用户登录成功，跳转到首页
                        window.location.href = '/index';
                    } else if (response.code === 300) {
                        // 管理员登录成功，跳转到管理员界面
                        window.location.href = '/user_management';
                    } else {
                        // 登录失败，显示错误提示
                        alert(response.message);
                    }
                } else {
                    // 请求出错，显示错误提示
                    alert('请求出错');
                }
            }
        };
    }

    // 监听登录按钮的点击事件
    loginBtn.addEventListener('click', login);
};
