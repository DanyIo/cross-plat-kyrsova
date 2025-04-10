export interface Transaction {
  id: number;
  amount: number;
  category: string;
  transaction_type: 'income' | 'expense';
  date: string;
  description: string;
}
