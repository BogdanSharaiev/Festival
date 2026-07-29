<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Функції</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f9;
      color: #333;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px;
    }
    .container {
      width: 100%;
      max-width: 500px;
      text-align: center;
      background-color: white;
      padding: 20px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      border-radius: 8px;
      margin-bottom: 20px;
    }
    h1 {
      margin-bottom: 20px;
    }
    input[type="text"], button {
      width: 100%;
      padding: 12px;
      margin: 8px 0;
      border-radius: 4px;
      border: 1px solid #ccc;
    }
    button {
      background-color: #007bff;
      color: white;
      cursor: pointer;
      font-size: 16px;
    }
    button:hover {
      background-color: #0056b3;
    }
    #result, #tableResult {
      margin-top: 20px;
      font-weight: bold;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    table, th, td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }
    th {
      background-color: #007bff;
      color: white;
    }
  </style>
</head>
<body>

<div class="container">
  <h1>Scalar Function</h1>
  <p>Write Event name:</p>
  <input type="text" id="eventInput" placeholder="Type event name" />
  <button onclick="callScalarFunction()">Start</button>
  <div id="result"></div>
</div>

<div class="container">
  <h1>Table Data</h1>
  <button onclick="fetchTableData()">Load Table</button>
  <table id="data-table">
    <thead>
      <tr></tr>
    </thead>
    <tbody></tbody>
  </table>
</div>

<script>
    async function callScalarFunction() {
        try {
            let event_name = document.getElementById('eventInput').value;
            const url = 'http://localhost:8000/api/func2';
            let response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-type": "application/json"
                },
                body: JSON.stringify({ value: event_name })
            });
            let result = await response.json();
            if (response.ok) {
                document.getElementById("result").textContent = "Чек з найбільшою кількостю продаж для події " + event_name +' :' +result.mostSoldCheckNum;
            } else {
                document.getElementById("result").textContent = "Помилка: " + result.error;
            }
        } catch (error) {
            document.getElementById("result").textContent = "Помилка запита: " + error.message;
        }
    }

    async function fetchTableData() {
        const url = 'http://localhost:8000/api/func1'; 

        try {
            const response = await fetch(url);
            const data = await response.json();
            populateTable(data);
        } catch (error) {
            alert("Помилка завантаження даних.");
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
</script>

</body>
</html>
