import { createRootRoute, Outlet } from '@tanstack/react-router'
import Header from '@/components/header'
import { th } from '@vcc/web-builder'

export const Route = createRootRoute({
  component: () => (
    <section className={th.app}>
      <Header />
      <div className={th.pageArea}>
        <Outlet />
      </div>
    </section>
  ),
})
