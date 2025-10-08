import { FileText, TrendingUp, Clock, CheckCircle } from 'lucide-react'

export default function Dashboard() {
  const stats = [
    { name: 'Total Translations', value: '1,234', icon: FileText, change: '+12%', color: 'bg-blue-500' },
    { name: 'This Month', value: '156', icon: TrendingUp, change: '+23%', color: 'bg-green-500' },
    { name: 'Avg. Processing Time', value: '2.3s', icon: Clock, change: '-8%', color: 'bg-yellow-500' },
    { name: 'Cache Hit Rate', value: '78%', icon: CheckCircle, change: '+5%', color: 'bg-purple-500' },
  ]

  const recentTranslations = [
    { id: 1, text: 'Der komplizierte Text...', status: 'completed', date: '2 minutes ago' },
    { id: 2, text: 'Ein langer Dokument...', status: 'completed', date: '15 minutes ago' },
    { id: 3, text: 'Rechtliche Informationen...', status: 'processing', date: '30 minutes ago' },
  ]

  return (
    <div className="space-y-8">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.name}</p>
                  <p className="text-3xl font-bold mt-2">{stat.value}</p>
                  <p className="text-sm text-green-600 mt-1">{stat.change} from last month</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Recent Translations */}
      <div className="card">
        <h3 className="text-xl font-bold mb-4">Recent Translations</h3>
        <div className="space-y-4">
          {recentTranslations.map((translation) => (
            <div key={translation.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex-1">
                <p className="font-medium text-gray-900">{translation.text}</p>
                <p className="text-sm text-gray-500">{translation.date}</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                translation.status === 'completed' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {translation.status}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card hover:shadow-lg transition cursor-pointer">
          <FileText className="w-8 h-8 text-primary-600 mb-3" />
          <h4 className="font-bold text-lg mb-2">New Translation</h4>
          <p className="text-gray-600 text-sm">Upload and translate a new document</p>
        </div>
        
        <div className="card hover:shadow-lg transition cursor-pointer">
          <TrendingUp className="w-8 h-8 text-green-600 mb-3" />
          <h4 className="font-bold text-lg mb-2">View Analytics</h4>
          <p className="text-gray-600 text-sm">Check your usage statistics</p>
        </div>
        
        <div className="card hover:shadow-lg transition cursor-pointer">
          <CheckCircle className="w-8 h-8 text-blue-600 mb-3" />
          <h4 className="font-bold text-lg mb-2">Manage Glossary</h4>
          <p className="text-gray-600 text-sm">Update custom translations</p>
        </div>
      </div>
    </div>
  )
}
