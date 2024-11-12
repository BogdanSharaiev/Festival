from django.contrib import admin
from django.urls import path, include
from .views import getTickets,getEvents, startProcedure, func1, func2, event, ticket, transactions
urlpatterns = [
   path('tickets',getTickets),
   path('events',getEvents),
   path('procedure',startProcedure),
   path('func1', func1),
   path('func2',func2),
   path('ticket',ticket),
   path('ticket/<int:ticket_id>/',ticket),
   path('event',event),
   path('event/<int:event_id>/', event),
   path('transaction',transactions),
]