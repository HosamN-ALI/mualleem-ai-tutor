import { useState, useRef, useEffect } from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import { ChatMessage } from './ChatMessage';
import { sendChatMessage } from '../lib/api';

export function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [input, setInput] = useState('');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() && !selectedImage) return;

    const userMessage: ChatMessageType = {
      id: crypto.randomUUID(),
      role: 'user',
      content: input,
      imageUrl: imagePreview || undefined,
      timestamp: new Date()
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage(input, selectedImage || undefined);

      const assistantMessage: ChatMessageType = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: response.answer,
        timestamp: new Date(),
        model_used: response.model_used,
        context_used: response.context_used
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: ChatMessageType = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `خطأ: ${error instanceof Error ? error.message : 'حدث خطأ غير متوقع'}`,
        timestamp: new Date()
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      clearImage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      <header className="bg-white shadow-sm border-b border-gray-200 p-4" dir="rtl">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-800">معلّم - المساعد التعليمي الذكي</h1>
          <p className="text-sm text-gray-600">اسأل سؤالك الرياضي وسأساعدك بالحل خطوة بخطوة</p>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-5xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12" dir="rtl">
              <div className="text-6xl mb-4">📚</div>
              <h2 className="text-2xl font-bold text-gray-700 mb-2">مرحباً بك!</h2>
              <p className="text-gray-600">
                اطرح سؤالك الرياضي أو ارفع صورة للمسألة وسأساعدك في حلها
              </p>
            </div>
          )}

          {messages.map((message) => (
            <ChatMessage
              key={message.id}
              message={message}
              sessionId={sessionId}
              onReviewSubmitted={() => console.log('Review submitted')}
            />
          ))}

          {isLoading && (
            <div className="flex justify-start mb-4" dir="rtl">
              <div className="bg-gray-100 rounded-lg p-4">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm text-gray-600">جاري التفكير...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="bg-white border-t border-gray-200 p-4">
        <div className="max-w-5xl mx-auto">
          <form onSubmit={handleSubmit} className="space-y-3" dir="rtl">
            {imagePreview && (
              <div className="relative inline-block">
                <img src={imagePreview} alt="Preview" className="max-h-32 rounded-lg border border-gray-300" />
                <button
                  type="button"
                  onClick={clearImage}
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600"
                >
                  ×
                </button>
              </div>
            )}

            <div className="flex gap-2">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleImageSelect}
                accept="image/*"
                className="hidden"
              />
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                disabled={isLoading}
              >
                <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </button>

              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="اكتب سؤالك هنا..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              />

              <button
                type="submit"
                disabled={isLoading || (!input.trim() && !selectedImage)}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                إرسال
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
