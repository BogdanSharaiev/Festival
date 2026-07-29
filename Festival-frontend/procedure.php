<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Процедура</title>
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

    
  </style>
</head>
<body>

<div class="container">
  <h1>Procedure</h1>
  <p>Самий дорогий квиток для заданої Події:</p>

  <input type="text" id="procedureInput" placeholder="Введите значение" />
  <button onclick="runProcedure()">Start</button>
  
  <div id="result" style="margin-top: 20px; font-weight: bold;"></div>
</div>

<script>
 async function runProcedure() {
  const inputValue = document.getElementById("procedureInput").value;
  const url = `http://127.0.0.1:8000/api/procedure`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ value: inputValue })
    });

    const text = await response.text();  
    console.log("Response text:", text);  

    try {
      const result = JSON.parse(text);  
      if (response.ok) {
        document.getElementById("result").textContent = "Успішне виконання процедури для event_id: " + inputValue;
      } else {
        document.getElementById("result").textContent = "Помилка: " + result.error;
        console.error(result.details);
      }
    } catch (jsonError) {
      document.getElementById("result").textContent = "Помилка: отримано невалидний JSON. Текст відповіді: " + text;
    }

  } catch (error) {
    document.getElementById("result").textContent = "Помилка виконання запиту: " + error.message;
  }
}

</script>

</body>
</html>
