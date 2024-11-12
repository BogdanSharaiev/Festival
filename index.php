<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Вивід даних з таблиць</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f9;
      color: #333;
      display: flex;
    }

    /* Стили для бокового меню */
    .sidebar {
      width: 200px;
      background-color: #007bff;
      color: white;
      height: 100vh;
      padding: 20px;
      position: fixed;
      top: 0;
      left: 0;
    }

    .sidebar h2 {
      text-align: center;
      margin-bottom: 20px;
    }

    .sidebar a {
      display: block;
      color: white;
      padding: 12px;
      text-decoration: none;
      margin: 8px 0;
      border-radius: 4px;
    }

    .sidebar a:hover {
      background-color: #0056b3;
    }

    /* Основной контейнер для контента */
    .main-content {
      margin-left: 220px;
      width: 80%;
      max-width: 1200px;
      padding: 20px;
    }

    h1 {
      text-align: center;
      margin-bottom: 20px;
    }

    .table-selector {
      margin: 20px 0;
      display: flex;
      justify-content: center;
    }

    .table-selector select {
      padding: 8px 12px;
      font-size: 16px;
      border-radius: 4px;
      border: 1px solid #ccc;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }

    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }

    th {
      background-color: #007bff;
      color: white;
      cursor: pointer;
    }

    tr:hover {
      background-color: #f1f1f1;
    }
  </style>
</head>
<body>

<!-- меню -->
<div class="sidebar">
  <h2>Меню</h2>
  <a href="/function.php">Функції</a>
  <a href="/procedure.php">Процедури</a>
</div>

<!-- контент -->
<div class="main-content">
  <h1>Data Table</h1>

  <div class="table-selector">
    <label for="table-select">Вибір таблиці:</label>
    <select id="table-select" onchange="fetchTableData()">
      <option value="tickets">Продажі квитків</option>
      <option value="events">Стан подій</option>
      <option value="event">Всі події</option>
      <option value="ticket">Квитки</option>
      <option value="transaction">Всі транзакції</option>
    </select>
  </div>

  <table id="data-table">
    <thead>
      <tr>
      </tr>
    </thead>
    <tbody>

    </tbody>
  </table>
</div>

<script>
   async function fetchTableData() {
    const tableSelect = document.getElementById("table-select").value;
    let url = `http://127.0.0.1:8000/api/${tableSelect}`; 
    try {
      const response = await fetch(url);
      const data = await response.json();
      
      populateTable(data);
    } catch (error) {
      alert("Помилка завантаження даних для: " + tableSelect);
    }
  }

  function populateTable(data) {
    const tableHead = document.getElementById("data-table").querySelector("thead tr");
    const tableBody = document.getElementById("data-table").querySelector("tbody");
    
    tableHead.innerHTML = "";
    tableBody.innerHTML = "";

    if (data.length > 0) {
      Object.keys(data[0]).forEach(key => {
        const th = document.createElement("th");
        th.textContent = key;
        tableHead.appendChild(th);
      });
      data.forEach(row => {
        const tr = document.createElement("tr");
        
        Object.values(row).forEach(value => {
          const td = document.createElement("td");
          td.textContent = value;
          tr.appendChild(td);
        });

        tableBody.appendChild(tr);
      });
    } else {
      const noDataMessage = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = Object.keys(data[0] || { col1: "" }).length;
      td.textContent = "Данных нет";
      td.style.textAlign = "center";
      noDataMessage.appendChild(td);
      tableBody.appendChild(noDataMessage);
    }
  }

  document.addEventListener("DOMContentLoaded", fetchTableData);
</script>

</body>
</html>
