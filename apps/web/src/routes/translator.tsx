import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export const Route = createFileRoute('/translator')({
  component: () => (
    <div className="flex-1 overflow-y-auto p-4">
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
