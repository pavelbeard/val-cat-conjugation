import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent, CardHeader, CardTitle } from '@vcc/web-builder'
import { th } from '@vcc/web-builder'

export const Route = createFileRoute('/translator')({
  component: () => (
    <div className={th.scrollPage}>
      <Card className="p-4 m-3 max-w-md">
        <CardHeader>
          <CardTitle className="text-lg font-semibold">Traductor</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Work in Progress</p>
        </CardContent>
      </Card>
    </div>
  ),
})
