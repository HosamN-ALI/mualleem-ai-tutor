'use client'

// @ts-ignore - react-katex doesn't have type definitions
import { BlockMath, InlineMath } from 'react-katex'
import 'katex/dist/katex.min.css'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  image?: string
}

interface ChatBubbleProps {
  message: Message
}

export default function ChatBubble({ message }: ChatBubbleProps) {
  const isUser = message.role === 'user'

  // Parse LaTeX in content
  const renderContent = (text: string) => {
    // Split by display math ($...$)
    const displayMathRegex = /\$\$(.*?)\$\$/g
    const inlineMathRegex = /\$(.*?)\$/g
    
    const parts: string[] = []
    let lastIndex = 0
    let match

    // First handle display math
    const textWithDisplayMath = text.replace(displayMathRegex, (match, latex) => {
      return `DISPLAYMATH${parts.length}DISPLAYMATH${parts.push(latex) - 1}`
    })

    // Then handle inline math
    const segments = textWithDisplayMath.split(inlineMathRegex)
    
    return segments.map((segment, index) => {
      // Check if it's a display math placeholder
      const displayMatch = segment.match(/DISPLAYMATH(\d+)DISPLAYMATH(\d+)/)
      if (displayMatch) {
        const latex = parts[parseInt(displayMatch[2])]
        return <BlockMath key={index} math={latex} />
      }
      
      // Odd indices are inline math
      if (index % 2 === 1) {
        return <InlineMath key={index} math={segment} />
      }
      
      // Even indices are regular text
      return <span key={index}>{segment}</span>
    })
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-6 py-4 ${
          isUser
            ? 'bg-primary-600 text-white'
            : 'bg-gray-100 text-gray-800'
        }`}
      >
        {message.image && (
          <img
            src={message.image}
            alt="Uploaded"
            className="mb-3 rounded-lg max-h-48 object-contain"
          />
        )}
        <div className="text-base leading-relaxed whitespace-pre-wrap">
          {renderContent(message.content)}
        </div>
      </div>
    </div>
  )
}
