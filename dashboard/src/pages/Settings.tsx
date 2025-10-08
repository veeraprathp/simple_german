import { Save, Key, Bell, User } from 'lucide-react'

export default function Settings() {
  return (
    <div className="space-y-6">
      {/* API Settings */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Key className="w-6 h-6 text-primary-600" />
          <h3 className="font-bold text-lg">API Configuration</h3>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              API Endpoint
            </label>
            <input
              type="text"
              className="input"
              defaultValue="http://localhost:8000"
              placeholder="https://api.example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              API Key
            </label>
            <input
              type="password"
              className="input"
              defaultValue="••••••••••••••••"
              placeholder="Enter your API key"
            />
          </div>
        </div>
      </div>

      {/* User Settings */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <User className="w-6 h-6 text-primary-600" />
          <h3 className="font-bold text-lg">User Profile</h3>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Display Name
            </label>
            <input
              type="text"
              className="input"
              defaultValue="User"
              placeholder="Your name"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              type="email"
              className="input"
              defaultValue="user@example.com"
              placeholder="your@email.com"
            />
          </div>
        </div>
      </div>

      {/* Notification Settings */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Bell className="w-6 h-6 text-primary-600" />
          <h3 className="font-bold text-lg">Notifications</h3>
        </div>
        <div className="space-y-3">
          <label className="flex items-center space-x-3">
            <input type="checkbox" className="rounded text-primary-600" defaultChecked />
            <span className="text-gray-700">Email notifications for completed translations</span>
          </label>
          <label className="flex items-center space-x-3">
            <input type="checkbox" className="rounded text-primary-600" />
            <span className="text-gray-700">Weekly usage reports</span>
          </label>
          <label className="flex items-center space-x-3">
            <input type="checkbox" className="rounded text-primary-600" defaultChecked />
            <span className="text-gray-700">System alerts and updates</span>
          </label>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button className="btn btn-primary">
          <Save className="w-5 h-5 mr-2 inline" />
          Save Changes
        </button>
      </div>
    </div>
  )
}
