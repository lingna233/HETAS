// 替换登录按钮
function showUser(username) {
    var navItem = '<li class="nav-item">' +
                  '<a class="nav-link" href="#">' + username + '</a>' +
                  '</li>';
    $('.navbar-nav').children().last().replaceWith(navItem);
}

// 登录按钮的点击事件
$('.navbar-nav').on('click', 'li.nav-item:last-child', function () {
    // 处理登录逻辑
    // ...
    // 成功登录后，调用 showUser(username) 函数
    showUser(username);
});