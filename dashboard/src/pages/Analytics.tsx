import { TrendingUp, Clock, Target, Award } from 'lucide-react'

export default function Analytics() {
  const metrics = [
    { label: 'Total Requests', value: '12,345', trend: '+12.5%', icon: TrendingUp },
    { label: 'Avg Response Time', value: '2.3s', trend: '-8.2%', icon: Clock },
    { label: 'Success Rate', value: '98.5%', trend: '+2.1%', icon: Target },
    { label: 'User Satisfaction', value: '4.8/5', trend: '+0.3', icon: Award },
  ]

  return (
    <div className="space-y-6">
      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric) => {
          const Icon = metric.icon
          return (
            <div key={metric.label} className="card">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-gray-600">{metric.label}</p>
                  <p className="text-2xl font-bold mt-2">{metric.value}</p>
                  <p className="text-sm text-green-600 mt-1">{metric.trend}</p>
                </div>
                <Icon className="w-8 h-8 text-primary-600" />
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-bold text-lg mb-4">Translation Volume</h3>
          <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <p className="text-gray-500">Chart visualization would go here</p>
          </div>
        </div>

        <div className="card">
          <h3 className="font-bold text-lg mb-4">Cache Performance</h3>
          <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <p className="text-gray-500">Chart visualization would go here</p>
          </div>
        </div>
      </div>

      {/* Usage Table */}
      <div className="card">
        <h3 className="font-bold text-lg mb-4">Recent Activity</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Date</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Requests</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Cache Hit Rate</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Avg Time</th>
              </tr>
            </thead>
            <tbody>
              {[1, 2, 3, 4, 5].map((i) => (
                <tr key={i} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4">2025-01-{10 - i}</td>
                  <td className="py-3 px-4">{Math.floor(Math.random() * 200) + 50}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-sm">
                      {Math.floor(Math.random() * 20) + 70}%
                    </span>
                  </td>
                  <td className="py-3 px-4">{(Math.random() * 2 + 1).toFixed(2)}s</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
