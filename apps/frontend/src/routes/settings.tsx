import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { updateSettings, useSettings, type Settings } from '@/lib/settings'
import { L } from '@/lib/literals'

// El valencià es mostra primer; el català (central) és el marc nou
const FIELDS: { key: keyof Settings; label: string }[] = [
  { key: 'show_valencian', label: L.settings.showValencian },
  { key: 'show_catalan', label: L.settings.showCatalan },
  { key: 'show_balearic', label: L.settings.showBalearic },
  { key: 'show_opt_pre2017', label: L.settings.showPre2017 },
]

export const Route = createFileRoute('/settings')({
  component: function SettingsPage() {
    const settings = useSettings()
    return (
      <div className="flex-1 overflow-y-auto p-4">
        <Card className="p-4 m-3 max-w-md">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">{L.settings.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
              {FIELDS.map(({ key, label }) => (
                <Label key={key}>
                  <input
                    type="checkbox"
                    className="size-4 accent-primary"
                    checked={settings[key]}
                    onChange={(e) => updateSettings({ [key]: e.target.checked })}
                  />
                  <span>{label}</span>
                </Label>
              ))}
            </form>
          </CardContent>
        </Card>
      </div>
    )
  },
})
