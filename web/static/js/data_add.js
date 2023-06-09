window.onload = function () {   // 保证下面代码在网页加载完成后再执行。这样可以避免在网页未加载完成时，无法找到“.btn”等元素无法找到
// 获取登录按钮和输入框的元素
    const addBtn = document.querySelector('.btn');
    const household_head_sexSelect = document.getElementById("household_head_sex");
    const household_incomeInput = document.querySelector('input[id="household_income"]');
    const num_family_membersInput = document.querySelector('input[id="num_family_members"]');
    const number_of_workersInput = document.querySelector('input[id="number_of_workers"]');
    const number_of_televisionInput = document.querySelector('input[id="number_of_television"]');
    const number_of_carInput = document.querySelector('input[id="number_of_car"]');
    const number_of_phoneInput = document.querySelector('input[id="number_of_phone"]');
    const number_of_personal_computerInput = document.querySelector('input[id="number_of_personal_computer"]');
    const total_household_expenditureInput = document.querySelector('input[id="total_household_expenditure"]');

    function add() {
        // 获取用户名和密码
        const household_head_sex = household_head_sexSelect.options[household_head_sexSelect.selectedIndex].value;
        const household_income = household_incomeInput.value;
        const num_family_members = num_family_membersInput.value;
        const number_of_workers = number_of_workersInput.value;
        const number_of_television = number_of_televisionInput.value;
        const number_of_car = number_of_carInput.value;
        const number_of_phone = number_of_phoneInput.value;
        const number_of_personal_computer = number_of_personal_computerInput.value;
        const total_household_expenditure = total_household_expenditureInput.value;

        if (true) {
            // 创建 XMLHttpRequest 对象
            const xhr = new XMLHttpRequest();

            // 设置请求方式和 URL
            xhr.open('POST', '/do_dataadd');

            // 设置请求头部信息
            xhr.setRequestHeader('Content-Type', 'application/json');

            // 构建请求体
            const requestBody = JSON.stringify({
                household_head_sex: household_head_sex,
                household_income: household_income,
                num_family_members: num_family_members,
                number_of_workers: number_of_workers,
                number_of_television: number_of_television,
                number_of_car: number_of_car,
                number_of_phone: number_of_phone,
                number_of_personal_computer: number_of_personal_computer,
                total_household_expenditure: total_household_expenditure 
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
                            // 登录成功，跳转到首页
                            window.location.href = '/data_management';
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
        } else {
            alert('确认密码与密码不一致，请重新输入');
            return alert;
        }

    }

    // 监听登录按钮的点击事件
    addBtn.addEventListener('click', add);
};