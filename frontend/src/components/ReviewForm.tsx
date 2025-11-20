import { useState } from 'react';
import { RatingStars } from './RatingStars';
import { submitReview } from '../lib/api';
import { ReviewData } from '../types';

interface ReviewFormProps {
  sessionId: string;
  question: string;
  answer: string;
  modelUsed?: string;
  contextUsed?: boolean;
  onReviewSubmitted: () => void;
  onCancel: () => void;
}

export function ReviewForm({
  sessionId,
  question,
  answer,
  modelUsed,
  contextUsed,
  onReviewSubmitted,
  onCancel
}: ReviewFormProps) {
  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (rating === 0) {
      setError('يرجى اختيار تقييم');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const reviewData: ReviewData = {
        session_id: sessionId,
        question,
        answer,
        rating,
        feedback: feedback.trim() || undefined,
        model_used: modelUsed,
        context_used: contextUsed
      };

      await submitReview(reviewData);
      onReviewSubmitted();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل في إرسال التقييم');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200" dir="rtl">
      <h3 className="text-xl font-bold text-gray-800 mb-4">قيّم هذه الإجابة</h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            التقييم <span className="text-red-500">*</span>
          </label>
          <div className="flex justify-center">
            <RatingStars rating={rating} onRatingChange={setRating} size="lg" />
          </div>
        </div>

        <div>
          <label htmlFor="feedback" className="block text-sm font-medium text-gray-700 mb-2">
            ملاحظاتك (اختياري)
          </label>
          <textarea
            id="feedback"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={4}
            placeholder="شاركنا رأيك حول جودة الإجابة..."
          />
        </div>

        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        <div className="flex gap-3 justify-end">
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
          >
            إلغاء
          </button>
          <button
            type="submit"
            disabled={isSubmitting || rating === 0}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'جاري الإرسال...' : 'إرسال التقييم'}
          </button>
        </div>
      </form>
    </div>
  );
}
