import { useState } from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import { ReviewForm } from './ReviewForm';
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

interface ChatMessageProps {
  message: ChatMessageType;
  sessionId: string;
  onReviewSubmitted?: () => void;
}

export function ChatMessage({ message, sessionId, onReviewSubmitted }: ChatMessageProps) {
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [reviewSubmitted, setReviewSubmitted] = useState(false);

  const handleReviewSubmitted = () => {
    setReviewSubmitted(true);
    setShowReviewForm(false);
    onReviewSubmitted?.();
  };

  const renderContent = (content: string) => {
    const parts = content.split(/(\$\$[\s\S]+?\$\$|\$[^\$]+?\$)/g);

    return parts.map((part, index) => {
      if (part.startsWith('$$') && part.endsWith('$$')) {
        const latex = part.slice(2, -2);
        return (
          <div key={index} className="my-4">
            <BlockMath math={latex} />
          </div>
        );
      } else if (part.startsWith('$') && part.endsWith('$')) {
        const latex = part.slice(1, -1);
        return <InlineMath key={index} math={latex} />;
      } else {
        return <span key={index}>{part}</span>;
      }
    });
  };

  return (
    <div
      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}
      dir="rtl"
    >
      <div className="max-w-3xl space-y-3">
        <div
          className={`rounded-lg p-4 ${
            message.role === 'user'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {message.imageUrl && (
            <img
              src={message.imageUrl}
              alt="Uploaded"
              className="max-w-full rounded-lg mb-2"
            />
          )}
          <div className="whitespace-pre-wrap">{renderContent(message.content)}</div>
        </div>

        {message.role === 'assistant' && !reviewSubmitted && (
          <div className="flex justify-start">
            {!showReviewForm ? (
              <button
                onClick={() => setShowReviewForm(true)}
                className="text-sm text-blue-600 hover:text-blue-700 hover:underline transition-colors"
              >
                قيّم هذه الإجابة
              </button>
            ) : (
              <div className="w-full">
                <ReviewForm
                  sessionId={sessionId}
                  question={message.content}
                  answer={message.content}
                  modelUsed={message.model_used}
                  contextUsed={message.context_used}
                  onReviewSubmitted={handleReviewSubmitted}
                  onCancel={() => setShowReviewForm(false)}
                />
              </div>
            )}
          </div>
        )}

        {reviewSubmitted && (
          <div className="text-sm text-green-600 flex items-center gap-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            تم إرسال التقييم. شكراً لك!
          </div>
        )}
      </div>
    </div>
  );
}
