import json
from django.http import JsonResponse
from .utils import getdata, stproc, execute_query
from django.views.decorators.csrf import csrf_exempt


def event(request, event_id=None):
    try:
        if request.method == 'GET':
            if event_id:
                data = getdata('SELECT * FROM Events WHERE event_id = ?', [event_id])
                if data:
                    return JsonResponse(data[0], safe=False)
                return JsonResponse({"error": "Event not found"}, status=404)
            else:
                # Якщо event_id не задано, отримуємо всі події
                data = getdata('SELECT * FROM Events')
                return JsonResponse(data, safe=False)

        elif request.method == 'POST':
            if not request.body:
                return JsonResponse({"error": "Empty request body"}, status=400)
            data = json.loads(request.body)
            event_name = data.get("event_name")
            date = data.get("date")
            place_id = data.get("place_id")
            info = data.get("Info")
            execute_query("INSERT INTO Events (event_name, date, place_id, Info) VALUES (?, ?, ?, ?)",
                          [event_name, date, place_id, info])
            return JsonResponse({"message": "Event created"}, status=201)

        elif request.method == 'PUT' and event_id:
            data = json.loads(request.body)
            event_name = data.get("event_name")
            date = data.get("date")
            place_id = data.get("place_id")
            info = data.get("Info")
            execute_query("UPDATE Events SET event_name=?, date=?, place_id=?, Info=? WHERE event_id=?",
                          [event_name, date, place_id, info, event_id])
            return JsonResponse({"message": "Event updated"}, status=200)

        elif request.method == 'DELETE' and event_id:
            execute_query("DELETE FROM Events WHERE event_id = ?", [event_id])
            return JsonResponse({"message": "Event deleted"}, status=204)

        else:
            return JsonResponse({"error": "Method not allowed or missing ID for the operation"}, status=405)

    except Exception as e:
        return JsonResponse({'error': f'Error handling event: {str(e)}'}, status=500)


@csrf_exempt
def ticket(request, ticket_id=None):
    try:
        if request.method == 'GET':
            if ticket_id:
                data = getdata('SELECT * FROM Tickets WHERE ticket_id = ?', [ticket_id])
                if data:
                    return JsonResponse(data[0], safe=False)
                return JsonResponse({"error": "Ticket not found"}, status=404)
            else:
                data = getdata('SELECT * FROM Tickets')
                return JsonResponse(data, safe=False)

        elif request.method == 'POST':
            if not request.body:
                return JsonResponse({"error": "Empty request body"}, status=400)
            data = json.loads(request.body)
            event_id = data.get("event_id")
            ticket_type = data.get("type")
            price = data.get("price")
            quantity = data.get("quantity")
            execute_query("INSERT INTO Tickets (event_id, ticket_type, price, quantity) VALUES (?, ?, ?, ?)", [event_id, ticket_type, price, quantity])
            return JsonResponse({"message": "Ticket created"}, status=201)

        elif request.method == 'PUT' and ticket_id:
            data = json.loads(request.body)
            event_id = data.get("event_id")
            ticket_type = data.get("type")
            price = data.get("price")
            quantity = data.get("quantity")
            execute_query("UPDATE Tickets SET event_id=?, ticket_type=?, price=?, quantity=? WHERE ticket_id=?", [event_id, ticket_type, price,quantity, ticket_id])
            return JsonResponse({"message": "Ticket updated"}, status=200)

        elif request.method == 'DELETE' and ticket_id:
            execute_query("DELETE FROM Tickets WHERE ticket_id = ?", [ticket_id])
            return JsonResponse({"message": "Ticket deleted"}, status=204)

        else:
            return JsonResponse({"error": "Method not allowed or missing ID for the operation"}, status=405)

    except Exception as e:
        return JsonResponse({'error': f'Error handling ticket: {str(e)}'}, status=500)

def transactions(request):
    try:
        data = getdata('SELECT * FROM Transactions')
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Error fetching transactions: {str(e)}'}, status=500)


def func1(request):
    try:
        data = getdata("""Select * FROM mostTicketTransTable()""")
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Error fetching data from mostTicketTransTable: {str(e)}'}, status=500)


@csrf_exempt
def func2(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_name = data['value']
            query = """SELECT dbo.mostTicketTrans(?) as mostSoldCheckNum;"""
            scalar = getdata(query, (event_name,))

            if scalar:
                most_sold_check_num = scalar
                if most_sold_check_num is not None:
                    return JsonResponse({'mostSoldCheckNum': most_sold_check_num}, status=200)
                else:
                    return JsonResponse({'error': 'No result from procedure'}, status=404)
            else:
                return JsonResponse({'error': 'No data returned from database'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Wrong method'}, status=405)


def getTickets(request):
    try:
        data = getdata("""
            SELECT  
                t.ticket_type, 
                SUM(CASE WHEN tr.quantity IS NULL THEN 0 ELSE t.price * tr.quantity END) AS total_price,
                SUM(CASE WHEN tr.quantity IS NULL THEN 0 ELSE tr.quantity END) AS total_sold
            FROM Tickets t
            LEFT JOIN Transactions tr ON t.ticket_id = tr.ticket_id
            GROUP BY t.ticket_type
            ORDER BY total_price DESC
        """)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Error fetching ticket data: {str(e)}'}, status=500)


def getEvents(request):
    try:
        data = getdata("""
     
 SELECT 
    e.event_name, 
    e.date, 
    CASE 
        WHEN e.date > GETDATE() THEN 'Активна'
        ELSE 'Завершена'
    END event_status,
    COALESCE(SUM(t.quantity), 0) AS 'Квитків лишилося'
FROM 
    Events e
LEFT JOIN Tickets t ON e.event_id = t.event_id
GROUP BY 
    e.event_name, 
    e.date, 
    CASE 
        WHEN e.date > GETDATE() THEN 'Активна'
        ELSE 'Завершена'
    END
ORDER BY 
    e.event_name, 
    e.date, 
    event_status;

        """)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Error fetching event data: {str(e)}'}, status=500)


from django.http import JsonResponse
import json
import pyodbc  # або ваша бібліотека для роботи з базою даних


@csrf_exempt
def startProcedure(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            val = data['value']


            query = "EXECUTE dbo.mostExpensiveTicket ?;"
            stproc(query, (val,))

            return JsonResponse({'message': 'Ok'}, status=200)

        except pyodbc.DatabaseError as e:
            print(f"Error encountered: {e}")
            db_error = e.args[0]

            db_error_code = str(db_error[0]) if isinstance(db_error, tuple) else None
            db_error_message = str(db_error[1]) if isinstance(db_error, tuple) else str(db_error)

            print(f"Error code: {db_error_code}, Error message: {db_error_message}")


            if db_error_message == '42000':
                return JsonResponse({
                    'error': 'Помилка бази даних: Невірний тип даних. Введене значення не можна перетворити в ціле число',
                    'details': f'Помилка SQL: {e}'
                }, status=500, content_type='application/json')

            return JsonResponse({
                'error': f'Помилка при виконанні запиту: {db_error_message}',
                'code': db_error_code
            }, status=500, content_type='application/json')

    else:
        return JsonResponse({'error': 'Wrong method'}, status=405, content_type='application/json')




