const users = JSON.parse('{{ users | tojson | safe }}');
let currentPage = 1;
const rowsPerPage = 5;

function renderTable(users) {
    const tableBody = document.querySelector("#userTable tbody");
    tableBody.innerHTML = "";

    for (let i = 0; i < users.length; i++) {
        const user = users[i];
        const row = "<tr><td>" + user.id + "</td><td>" + user.username + "</td><td>" + user.password + "</td><td>" + (user.permissions ? "普通用户" : "管理员") + "</td></tr>";
        tableBody.innerHTML += row;
    }
}

function renderPagination() {
    const totalPages = Math.ceil(users.length / rowsPerPage);
    const paginationDiv = document.querySelector("#pagination");
    paginationDiv.innerHTML = "";

    if (currentPage > 1) {
        const prevButton = "<button onclick='prevPage()'>上一页</button>";
        paginationDiv.innerHTML += prevButton;
    }

    for (let i = 1; i <= totalPages; i++) {
        let pageButtonClass = "pageButton";
        if (i === currentPage) {
            pageButtonClass += " currentPage";
        }
        const pageButton = "<button class='" + pageButtonClass + "' onclick='goToPage(" + i + ")'>" + i + "</button>";
        paginationDiv.innerHTML += pageButton;
    }

    if (currentPage < totalPages) {
        const nextButton = "<button onclick='nextPage()'>下一页</button>";
        paginationDiv.innerHTML += nextButton;
    }
}

function goToPage(page) {
    currentPage = page;
    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const usersToShow = users.slice(startIndex, endIndex);
    renderTable(usersToShow);
    renderPagination();
}

function nextPage() {
    if (currentPage < Math.ceil(users.length / rowsPerPage)) {
        currentPage++;
        goToPage(currentPage);
    }
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        goToPage(currentPage);
    }
}

goToPage(1);


