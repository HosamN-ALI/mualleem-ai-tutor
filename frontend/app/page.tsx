'use client'

import { useState } from 'react'
import ChatInterface from '@/components/ChatInterface'
import { BookOpen } from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <BookOpen className="w-12 h-12 text-primary-600" />
            <h1 className="text-4xl font-bold text-gray-800">معلّم</h1>
          </div>
          <p className="text-gray-600 text-lg">
            منصة التعليم الذكية - اسأل كتابك المدرسي
          </p>
        </header>
        
        <ChatInterface />
      </div>
    </main>
  )
}
