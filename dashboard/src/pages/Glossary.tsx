import { useState } from 'react'
import { Plus, Edit, Trash2 } from 'lucide-react'

export default function Glossary() {
  const [glossaries, setGlossaries] = useState([
    { id: 1, term: 'Rechtsanwalt', replacement: 'Anwalt', scope: 'global' },
    { id: 2, term: 'Verwaltungsgericht', replacement: 'Gericht', scope: 'sentence' },
    { id: 3, term: 'Krankenversicherung', replacement: 'Versicherung', scope: 'global' },
  ])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Glossary Management</h2>
          <p className="text-gray-600 mt-1">Manage custom term translations</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2 inline" />
          Add Term
        </button>
      </div>

      {/* Glossary Table */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Original Term</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Replacement</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Scope</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody>
              {glossaries.map((item) => (
                <tr key={item.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 px-4">
                    <span className="font-medium text-gray-900">{item.term}</span>
                  </td>
                  <td className="py-4 px-4">
                    <span className="text-gray-700">{item.replacement}</span>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm ${
                      item.scope === 'global' 
                        ? 'bg-blue-100 text-blue-800' 
                        : 'bg-purple-100 text-purple-800'
                    }`}>
                      {item.scope}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-right">
                    <button className="p-2 hover:bg-gray-100 rounded-lg mr-2">
                      <Edit className="w-4 h-4 text-gray-600" />
                    </button>
                    <button className="p-2 hover:bg-red-50 rounded-lg">
                      <Trash2 className="w-4 h-4 text-red-600" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Instructions */}
      <div className="card bg-blue-50 border border-blue-200">
        <h4 className="font-bold text-blue-900 mb-2">How to use Glossary</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Add custom term replacements for consistent translations</li>
          <li>• Choose "global" scope for all occurrences or "sentence" for contextual use</li>
          <li>• Glossary terms are applied automatically during translation</li>
        </ul>
      </div>
    </div>
  )
}
