import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { getSettings, updateSettings, useSettings } from '@/lib/settings'

const FIELDS: { key: keyof ReturnType<typeof getSettings>; label: string }[] = [
  { key: 'show_valencian', label: 'Mostrar Valenciano' },
  { key: 'show_balearic', label: 'Mostrar Balearic' },
  { key: 'show_opt_pre2017', label: 'Mostrar Opciones Pre-2017' },
]

export const Route = createFileRoute('/settings')({
  component: function SettingsPage() {
    const settings = useSettings()
    return (
      <div className="flex-1 overflow-y-auto p-4">
        <Card className="p-4 m-3 max-w-md">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Ajustes</CardTitle>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
              {FIELDS.map(({ key, label }) => (
                <label key={key} className="flex items-center space-x-4">
                  <input
                    type="checkbox"
                    className="size-4 accent-violet-700"
                    checked={settings[key]}
                    onChange={(e) => updateSettings({ [key]: e.target.checked })}
                  />
                  <span className="text-sm">{label}</span>
                </label>
              ))}
            </form>
          </CardContent>
        </Card>
      </div>
    )
  },
})
