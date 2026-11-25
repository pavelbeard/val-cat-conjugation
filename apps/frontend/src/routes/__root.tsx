import { createRootRoute, Outlet } from '@tanstack/react-router'
import Header from '@/components/header'
import Footer from '@/components/footer'

export const Route = createRootRoute({
  component: () => (
    <section className="h-dvh flex flex-col">
      <Header />
      <div className="flex-1 overflow-hidden flex flex-col">
        <Outlet />
      </div>
      <Footer />
    </section>
  ),
})
