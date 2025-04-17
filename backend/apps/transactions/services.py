from .models import Transaction
from .serializers import TransactionSerializer
from django.http import HttpResponseForbidden


class TransactionService:
    @staticmethod
    def get_user_transactions_data(user):
        """
        Returns a list of transaction data for the specific user (processed for the response).
        """
        transactions = Transaction.objects.filter(user=user)
        return TransactionSerializer(transactions, many=True).data  # Serialize the data

    @staticmethod
    def create_transaction(user, data):
        """
        Creates a new transaction for the specific user.
        """
        data["user"] = user

        return Transaction.objects.create(**data)

    @staticmethod
    def update_transaction(user, transaction, data):
        """
        Updates the specified transaction for the user.
        """
        # Ensure the transaction is owned by the user
        if transaction.user != user:
            return HttpResponseForbidden(
                "You do not have permission to view this resource."
            )

        # Update the transaction with the new data
        for attr, value in data.items():
            setattr(transaction, attr, value)
        transaction.save()

    @staticmethod
    def destroy_transaction(user, transaction):
        """
        Deletes the specified transaction for the user.
        """
        # Ensure the transaction is owned by the user
        if transaction.user != user:
            return HttpResponseForbidden(
                "You do not have permission to delete this resource."
            )

        transaction.delete()
        return None  # Return None to indicate successful deletion
