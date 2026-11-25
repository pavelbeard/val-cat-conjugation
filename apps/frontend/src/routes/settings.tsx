import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent, CardHeader, CardTitle } from '@vcc/web-builder'
import { Label } from '@vcc/web-builder'
import { getSettings, updateSettings, useSettings } from '@/lib/settings'
import { th } from '@vcc/web-builder'

const FIELDS: { key: keyof ReturnType<typeof getSettings>; label: string }[] = [
  { key: 'show_valencian', label: 'Mostrar Valenciano' },
  { key: 'show_balearic', label: 'Mostrar Balearic' },
  { key: 'show_opt_pre2017', label: 'Mostrar Opciones Pre-2017' },
]

export const Route = createFileRoute('/settings')({
  component: function SettingsPage() {
    const settings = useSettings()
    return (
      <div className={th.scrollPage}>
        <Card className="p-4 m-3 max-w-md">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Ajustes</CardTitle>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
              {FIELDS.map(({ key, label }) => (
                <Label key={key}>
                  <input
                    type="checkbox"
                    className="size-4 accent-violet-700"
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
