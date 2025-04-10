interface Budget {
  id: number;
  user: string;
  rent: number;
  food: number;
  transportation: number;
  entertainment: number;
  created_at: string;
  updated_at: string;
}

interface NetWorth {
  id: number;
  user: string;
  net_worth: number;
  created_at: string;
  updated_at: string;
}
