import { useState } from 'react'
import { Upload, FileText, Download } from 'lucide-react'

export default function Translate() {
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [mode, setMode] = useState<'easy' | 'light'>('easy')
  const [isLoading, setIsLoading] = useState(false)

  const handleTranslate = async () => {
    setIsLoading(true)
    // Mock API call - replace with actual API
    setTimeout(() => {
      setOutputText('Dies ist der vereinfachte Text. Die Übersetzung wurde erfolgreich abgeschlossen.')
      setIsLoading(false)
    }, 2000)
  }

  return (
    <div className="space-y-6">
      {/* Mode Selector */}
      <div className="card">
        <h3 className="font-bold text-lg mb-4">Translation Mode</h3>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2 cursor-pointer">
            <input
              type="radio"
              name="mode"
              value="easy"
              checked={mode === 'easy'}
              onChange={(e) => setMode(e.target.value as 'easy' | 'light')}
              className="text-primary-600 focus:ring-primary-500"
            />
            <span>Einfache Sprache (Easy German)</span>
          </label>
          <label className="flex items-center space-x-2 cursor-pointer">
            <input
              type="radio"
              name="mode"
              value="light"
              checked={mode === 'light'}
              onChange={(e) => setMode(e.target.value as 'easy' | 'light')}
              className="text-primary-600 focus:ring-primary-500"
            />
            <span>Leichte Sprache (Simple German)</span>
          </label>
        </div>
      </div>

      {/* Translation Interface */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-lg">Original Text</h3>
            <button className="btn btn-secondary text-sm">
              <Upload className="w-4 h-4 mr-2 inline" />
              Upload File
            </button>
          </div>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter German text to simplify..."
            className="input min-h-[400px] resize-none"
          />
          <div className="mt-4 flex justify-between items-center">
            <span className="text-sm text-gray-600">{inputText.length} characters</span>
            <button 
              onClick={handleTranslate}
              disabled={!inputText || isLoading}
              className="btn btn-primary"
            >
              {isLoading ? 'Translating...' : 'Translate'}
            </button>
          </div>
        </div>

        {/* Output */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-lg">Simplified Text</h3>
            {outputText && (
              <button className="btn btn-secondary text-sm">
                <Download className="w-4 h-4 mr-2 inline" />
                Export
              </button>
            )}
          </div>
          <textarea
            value={outputText}
            readOnly
            placeholder="Simplified text will appear here..."
            className="input min-h-[400px] resize-none bg-gray-50"
          />
          {outputText && (
            <div className="mt-4 p-3 bg-green-50 rounded-lg">
              <p className="text-sm text-green-800">
                <FileText className="w-4 h-4 inline mr-2" />
                Translation completed successfully!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
