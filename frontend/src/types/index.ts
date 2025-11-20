export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  imageUrl?: string;
  timestamp: Date;
  model_used?: string;
  context_used?: boolean;
}

export interface ReviewData {
  session_id: string;
  question: string;
  answer: string;
  rating: number;
  feedback?: string;
  model_used?: string;
  context_used?: boolean;
  user_id?: string;
}

export interface ReviewStats {
  total_reviews: number;
  average_rating: number;
  rating_distribution: Record<string, number>;
}
