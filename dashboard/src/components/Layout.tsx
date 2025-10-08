import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Home, FileText, Book, BarChart3, Settings, LogOut } from 'lucide-react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Translate', href: '/translate', icon: FileText },
    { name: 'Glossary', href: '/glossary', icon: Book },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
    { name: 'Settings', href: '/settings', icon: Settings },
  ]

  const isActive = (path: string) => location.pathname === path

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 w-64 bg-gradient-to-b from-primary-600 to-secondary-600 text-white">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-6">
            <h1 className="text-2xl font-bold">🇩🇪 German Simplifier</h1>
            <p className="text-sm text-primary-100 mt-1">Make German easy to read</p>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                    isActive(item.href)
                      ? 'bg-white/20 shadow-lg'
                      : 'hover:bg-white/10'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              )
            })}
          </nav>

          {/* User info */}
          <div className="p-4 border-t border-white/20">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                <span className="font-bold">U</span>
              </div>
              <div className="flex-1">
                <p className="font-medium">User</p>
                <p className="text-xs text-primary-100">user@example.com</p>
              </div>
              <button className="p-2 hover:bg-white/10 rounded-lg transition">
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="ml-64 min-h-screen">
        {/* Header */}
        <header className="bg-white shadow-sm">
          <div className="px-8 py-4">
            <h2 className="text-2xl font-bold text-gray-900">
              {navigation.find(item => isActive(item.href))?.name || 'Dashboard'}
            </h2>
          </div>
        </header>

        {/* Content */}
        <main className="p-8">
          {children}
        </main>
      </div>
    </div>
  )
}
