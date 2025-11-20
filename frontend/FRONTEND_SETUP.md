# Frontend Setup - Mualleem Platform

## ✅ Implementation Complete

The Next.js frontend has been successfully set up with all required features for the AI-powered tutoring platform.

## 🏗️ Architecture

### Tech Stack
- **Framework**: Next.js 14.1.0 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Math Rendering**: react-katex + KaTeX
- **HTTP Client**: Axios
- **Font**: Cairo (Arabic + Latin support)

## 📁 Project Structure

```
frontend/
├── app/
│   ├── globals.css          # Global styles + KaTeX styling
│   ├── layout.tsx            # Root layout with RTL support
│   └── page.tsx              # Home page with ChatInterface
├── components/
│   ├── ChatBubble.tsx        # Message bubble with LaTeX rendering
│   └── ChatInterface.tsx     # Main chat component
├── package.json
├── next.config.js
├── tailwind.config.ts
└── tsconfig.json
```

## 🎯 Key Features Implemented

### 1. **RTL (Right-to-Left) Support**
- HTML `dir="rtl"` attribute set in layout
- Arabic language (`lang="ar"`)
- Cairo font with Arabic subset

### 2. **Chat Interface** (`components/ChatInterface.tsx`)
- ✅ Text input with Arabic placeholder
- ✅ Image upload with preview
- ✅ File selection button
- ✅ Message history display
- ✅ Loading states with spinner
- ✅ Error handling
- ✅ Connects to backend `/chat` endpoint at `http://localhost:8000`

### 3. **Chat Bubble** (`components/ChatBubble.tsx`)
- ✅ Renders user and assistant messages
- ✅ **LaTeX Support**: Parses and renders math equations
  - Inline math: `$x^2$` → $x^2$
  - Display math: `$$\frac{a}{b}$$` → $$\frac{a}{b}$$
- ✅ Image display for uploaded images
- ✅ Proper styling for user vs assistant messages

### 4. **API Integration**
- Uses `axios` to send `multipart/form-data` to backend
- Sends both text (`question`) and image (`image` file)
- Handles responses and errors gracefully

### 5. **UI/UX**
- Modern gradient background
- Responsive design
- Smooth transitions
- Loading indicators
- Image preview before sending
- Remove image button (×)

## 🚀 Running the Application

### Install Dependencies
```bash
cd frontend
npm install
```

### Start Development Server
```bash
npm run dev
```

The app will be available at: **http://localhost:3000**

### Build for Production
```bash
npm run build
npm start
```

## 🔗 Backend Connection

The frontend connects to the backend at:
- **Endpoint**: `POST http://localhost:8000/chat`
- **Content-Type**: `multipart/form-data`
- **Payload**:
  - `question` (string): User's text question
  - `image` (file, optional): Uploaded image

**Important**: Ensure the backend server is running on port 8000 before testing.

## 📝 LaTeX Rendering

The `ChatBubble` component automatically detects and renders LaTeX:

### Inline Math
```
السرعة تساوي $v = \frac{d}{t}$
```
Renders as: السرعة تساوي $v = \frac{d}{t}$

### Display Math
```
$$
E = mc^2
$$
```
Renders as a centered block equation.

## 🎨 Styling

### Tailwind Configuration
- Custom primary color palette (blue shades)
- Responsive utilities
- RTL-aware spacing

### Global CSS
- KaTeX styles imported
- Custom `.katex-display` for centered equations
- Font size adjustments for readability

## 🧪 Testing Checklist

- [x] Next.js server starts without errors
- [x] Page loads with Arabic text and RTL layout
- [x] Text input accepts Arabic characters
- [x] Image upload button opens file picker
- [x] Image preview displays correctly
- [x] Remove image button works
- [x] Send button is disabled when input is empty
- [x] Loading spinner shows during API call
- [ ] Backend connection works (requires backend running)
- [ ] LaTeX equations render correctly
- [ ] Messages display in chat history

## 🔧 Configuration Files

### `next.config.js`
- React strict mode enabled
- Standard Next.js configuration

### `tailwind.config.ts`
- Content paths configured for app directory
- Custom primary color theme

### `tsconfig.json`
- TypeScript strict mode
- Path alias `@/*` for imports
- Next.js plugin enabled

## 📦 Dependencies

### Production
- `next`: 14.1.0
- `react`: ^18.2.0
- `react-dom`: ^18.2.0
- `react-katex`: ^3.0.1 (LaTeX rendering)
- `katex`: ^0.16.9 (LaTeX library)
- `lucide-react`: ^0.316.0 (Icons)
- `axios`: ^1.6.5 (HTTP client)

### Development
- `typescript`: ^5
- `tailwindcss`: ^3.3.0
- `autoprefixer`: ^10.0.1
- `postcss`: ^8
- Type definitions for Node, React, and React DOM

## 🌐 Browser Support

The application supports modern browsers with:
- ES6+ JavaScript
- CSS Grid and Flexbox
- RTL layout
- File API for image uploads

## 🔐 Security Notes

- File uploads are restricted to images (`accept="image/*"`)
- CORS should be configured on backend for `http://localhost:3000`
- No sensitive data is stored in frontend state

## 📱 Responsive Design

The chat interface is responsive:
- Max width: 4xl (56rem)
- Chat bubbles: Max 80% width
- Mobile-friendly touch targets
- Scrollable message area (600px height)

## 🎓 Next Steps

1. **Start Backend**: Ensure FastAPI server is running on port 8000
2. **Test Integration**: Upload an image and ask a question
3. **Verify LaTeX**: Check that math equations render correctly
4. **Add Features**: Consider adding:
   - Message timestamps
   - Copy to clipboard
   - Voice input
   - Dark mode toggle
   - Chat history persistence

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Backend Connection Error
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS settings in backend `main.py`

### LaTeX Not Rendering
- Ensure `katex/dist/katex.min.css` is imported in `ChatBubble.tsx`
- Check browser console for errors

---

**Status**: ✅ Ready for testing
**Last Updated**: 2025-11-19
