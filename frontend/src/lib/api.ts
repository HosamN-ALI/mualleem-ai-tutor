import { ReviewData } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function sendChatMessage(question: string, image?: File) {
  const formData = new FormData();
  formData.append('question', question);
  if (image) {
    formData.append('image', image);
  }

  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'فشل في إرسال السؤال');
  }

  return response.json();
}

export async function submitReview(reviewData: ReviewData) {
  const response = await fetch(`${API_URL}/reviews`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(reviewData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'فشل في إرسال التقييم');
  }

  return response.json();
}

export async function getReviewStats() {
  const response = await fetch(`${API_URL}/reviews/stats`);

  if (!response.ok) {
    throw new Error('فشل في جلب إحصائيات التقييمات');
  }

  return response.json();
}
