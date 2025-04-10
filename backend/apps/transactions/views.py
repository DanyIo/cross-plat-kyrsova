from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from .services import TransactionService
from django.http import HttpResponseForbidden
from rest_framework import status

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
      
        transactions_data = TransactionService.get_user_transactions_data(self.request.user)
        
        return Response(
             transactions_data
        )

    def perform_create(self, serializer):
      
        TransactionService.create_transaction(self.request.user, serializer.validated_data)


class TransactionUpdateView(generics.UpdateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self): # type: ignore

        obj = Transaction.objects.get(pk=self.kwargs['pk'])
     
        return obj
    
    def perform_update(self, serializer): # type: ignore
     
        transaction = self.get_object()
        updated_transaction = TransactionService.update_transaction(self.request.user, transaction, serializer.validated_data)
        return Response(TransactionSerializer(updated_transaction).data)  # Return updated transaction
    
    def delete(self, request, pk, *args, **kwargs):
       
        transaction = Transaction.objects.get(pk=self.kwargs['pk'])
        if isinstance(transaction, HttpResponseForbidden):
            return transaction 
        
        TransactionService.destroy_transaction(self.request.user, transaction)
        return Response(status=status.HTTP_204_NO_CONTENT)
  