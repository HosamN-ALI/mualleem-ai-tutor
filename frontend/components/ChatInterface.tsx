'use client'

import { useState, useRef } from 'react'
import { Send, Image as ImageIcon, Loader2, BookOpen } from 'lucide-react'
import ChatBubble from './ChatBubble'
import axios from 'axios'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  image?: string
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]

    if (!file) {
      return
    }

    // Explicitly prevent non-image files (e.g. PDF) from being used in /chat
    if (!file.type.startsWith('image/')) {
      setSelectedImage(null)
      setImagePreview(null)
      setErrorMessage('رفع ملفات PDF للمنهج يتم من صفحة إعداد المنهج، أما هنا فيمكن رفع صور فقط.')
      // Reset the input so the same invalid file can trigger onChange again if re-selected
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      return
    }

    // Check file size (limit to 10MB)
    const maxSize = 10 * 1024 * 1024 // 10MB in bytes
    if (file.size > maxSize) {
      setSelectedImage(null)
      setImagePreview(null)
      setErrorMessage('حجم الصورة كبير جداً. يرجى اختيار صورة أصغر من 10 ميجابايت.')
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      return
    }

    // Check if it's a valid image format
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if (!validTypes.includes(file.type.toLowerCase())) {
      setSelectedImage(null)
      setImagePreview(null)
      setErrorMessage('نوع الصورة غير مدعوم. يرجى استخدام صور بصيغة JPG، PNG، GIF، أو WebP.')
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      return
    }

    setErrorMessage(null)
    setSelectedImage(file)

    const reader = new FileReader()
    reader.onloadend = () => {
      setImagePreview(reader.result as string)
    }
    reader.onerror = () => {
      setErrorMessage('حدث خطأ أثناء قراءة الصورة. يرجى المحاولة مرة أخرى.')
      setSelectedImage(null)
      setImagePreview(null)
    }
    reader.readAsDataURL(file)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!input.trim() && !selectedImage) return

    const trimmedQuestion = input.trim()

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: trimmedQuestion,
      image: imagePreview || undefined
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const formData = new FormData()
      formData.append('question', trimmedQuestion)
      if (selectedImage) {
        formData.append('image', selectedImage)
      }

      const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

      const response = await axios.post(`${apiBaseUrl}/chat`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.answer || 'عذراً، لم أتمكن من الحصول على إجابة.'
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      let errorContent = 'عذراً، حدث خطأ. يرجى المحاولة مرة أخرى.'

      if (axios.isAxiosError(error)) {
        if (error.response) {
          // Server responded with error status
          const status = error.response.status
          const serverMessage = error.response.data?.detail

          switch (status) {
            case 400:
              errorContent = serverMessage || 'خطأ في البيانات المرسلة. يرجى التحقق من صحة السؤال والصورة.'
              break
            case 413:
              errorContent = serverMessage || 'حجم الصورة كبير جداً. الحد الأقصى 10 ميجابايت.'
              break
            case 422:
              errorContent = serverMessage || 'تنسيق الصورة غير مدعوم أو البيانات غير صالحة.'
              break
            case 429:
              errorContent = serverMessage || 'تم تجاوز عدد الطلبات المسموح. يرجى الانتظار قليلاً ثم المحاولة مرة أخرى.'
              break
            case 500:
              errorContent = serverMessage || 'خطأ في الخادم. يرجى المحاولة لاحقاً.'
              break
            case 502:
              errorContent = 'خطأ في الاتصال مع الخادم. يرجى المحاولة لاحقاً.'
              break
            case 503:
              errorContent = 'الخدمة غير متاحة حالياً. يرجى المحاولة لاحقاً.'
              break
            case 504:
              errorContent = 'انتهت مهلة الاتصال مع الخادم. يرجى المحاولة مرة أخرى.'
              break
            default:
              errorContent = serverMessage || `خطأ من الخادم (${status}). يرجى المحاولة مرة أخرى.`
          }
        } else if (error.request) {
          // Network error
          errorContent = 'لا يمكن الاتصال بالخادم. تحقق من اتصال الإنترنت وحاول مرة أخرى.'
        } else {
          // Request setup error
          errorContent = 'خطأ في إعداد الطلب. يرجى إعادة تحميل الصفحة والمحاولة مرة أخرى.'
        }
      }

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: errorContent
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      setSelectedImage(null)
      setImagePreview(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto bg-white rounded-none sm:rounded-2xl shadow-none sm:shadow-2xl overflow-hidden min-h-screen sm:min-h-0">
      {/* Chat Messages Area */}
      <div className="h-[calc(100vh-140px)] sm:h-96 md:h-[500px] lg:h-[600px] overflow-y-auto p-3 sm:p-6 space-y-3 sm:space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center px-4">
              <BookOpen className="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-3 sm:mb-4 opacity-50" />
              <p className="text-sm sm:text-base md:text-lg leading-relaxed">ابدأ بطرح سؤالك أو ارفع صورة المسألة</p>
            </div>
          </div>
        ) : (
          messages.map(message => (
            <ChatBubble key={message.id} message={message} />
          ))
        )}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl px-4 sm:px-6 py-3 sm:py-4">
              <Loader2 className="w-5 h-5 sm:w-6 sm:h-6 animate-spin text-primary-600" />
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-3 sm:p-4 bg-gray-50">
        {errorMessage && (
          <div className="mb-2 text-xs sm:text-sm text-red-600 px-1 leading-relaxed">{errorMessage}</div>
        )}

        {imagePreview && (
          <div className="mb-3 relative inline-block">
            <img
              src={imagePreview}
              alt="Preview"
              className="h-16 sm:h-20 rounded-lg border-2 border-primary-300 max-w-full object-contain"
            />
            <button
              onClick={() => {
                setSelectedImage(null)
                setImagePreview(null)
              }}
              className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full min-w-[20px] min-h-[20px] sm:min-w-[24px] sm:min-h-[24px] flex items-center justify-center text-xs sm:text-sm font-bold touch-manipulation"
            >
              ×
            </button>
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex gap-2">
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
            className="min-h-[44px] min-w-[44px] p-2.5 sm:p-3 rounded-xl bg-gray-200 hover:bg-gray-300 transition-colors touch-manipulation"
            disabled={isLoading}
          >
            <ImageIcon className="w-4 h-4 sm:w-5 sm:h-5 text-gray-600" />
          </button>

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="اكتب سؤالك هنا..."
            className="flex-1 px-3 sm:px-4 py-2.5 sm:py-3 min-h-[44px] rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm sm:text-base"
            disabled={isLoading}
          />

          <button
            type="submit"
            disabled={isLoading || (!input.trim() && !selectedImage)}
            className="px-3 sm:px-6 py-2.5 sm:py-3 min-h-[44px] min-w-[44px] bg-primary-600 text-white rounded-xl hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-1 sm:gap-2 touch-manipulation text-sm sm:text-base"
          >
            <Send className="w-4 h-4 sm:w-5 sm:h-5" />
            <span className="hidden sm:inline">إرسال</span>
          </button>
        </form>
      </div>
    </div>
  )
}
