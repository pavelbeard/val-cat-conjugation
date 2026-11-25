import { createRootRoute, Outlet } from '@tanstack/react-router'
import Header from '@/components/header'

export const Route = createRootRoute({
  component: () => (
    <section className="h-screen flex flex-col">
      <Header />
      <div className="flex-1 overflow-hidden flex flex-col">
        <Outlet />
      </div>
    </section>
  ),
})
