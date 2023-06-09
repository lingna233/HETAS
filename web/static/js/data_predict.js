window.onload = function () {   // 保证下面代码在网页加载完成后再执行。这样可以避免在网页未加载完成时，无法找到“.btn”等元素无法找到
// 获取预测按钮和输入框的元素
    const predictBtn = document.querySelector('.btn');
    const modelSelect = document.getElementById("model");
    const incomeInput = document.querySelector('input[id="income"]');
    const household_head_sexInput = document.querySelector('input[id="household_head_sex"]');
    const num_family_membersInput = document.querySelector('input[id="num_family_members"]');
    const number_of_workersInput = document.querySelector('input[id="number_of_workers"]');
    const number_of_televisionInput = document.querySelector('input[id="number_of_television"]');
    const number_of_carInput = document.querySelector('input[id="number_of_car"]');
    const number_of_phoneInput = document.querySelector('input[id="number_of_phone"]');
    const number_of_personal_computerInput = document.querySelector('input[id="number_of_personal_computer"]');
    // 获取output元素
    const outputElement = document.getElementById("output_household_expenditure");

    function predict() {
        // 获取用户名和密码
        const selectedModel = modelSelect.options[modelSelect.selectedIndex].value;
        const income = incomeInput.value;
        const household_head_sex = household_head_sexInput.value;
        const num_family_members = num_family_membersInput.value;
        const number_of_workers = number_of_workersInput.value;
        const number_of_television = number_of_televisionInput.value;
        const number_of_car = number_of_carInput.value;
        const number_of_phone = number_of_phoneInput.value;
        const number_of_personal_computer = number_of_personal_computerInput.value;

        // 检查是否任意一项为空
        if (selectedModel === '' || income === '' || household_head_sex === '' ||
            num_family_members === '' || number_of_workers === '' || number_of_television === '' ||
            number_of_car === '' || number_of_phone === '' || number_of_personal_computer === '') {
            alert('请填写完整的数据！');
            return;
        }

        // 创建 XMLHttpRequest 对象
        const xhr = new XMLHttpRequest();

        // 设置请求方式和 URL
        xhr.open('POST', '/do_predict');

        // 设置请求头部信息
        xhr.setRequestHeader('Content-Type', 'application/json');

        // 构建请求体
        const requestBody = JSON.stringify({
            selectedModel: selectedModel,
            income: income,
            household_head_sex: household_head_sex,
            num_family_members: num_family_members,
            number_of_workers: number_of_workers,
            number_of_television: number_of_television,
            number_of_car: number_of_car,
            number_of_phone: number_of_phone,
            number_of_personal_computer: number_of_personal_computer
        });

        // 发送请求
        xhr.send(requestBody);

        // 监听状态变化，获取响应
        xhr.onreadystatechange = function () {
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                const response = JSON.parse(this.responseText);
                outputElement.value = response.output_household_expenditure;
            }
        };
    }

    // 监听登录按钮的点击事件
    predictBtn.addEventListener('click', predict);
};
