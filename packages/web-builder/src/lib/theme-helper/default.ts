import { cn } from '../utils'
import type { ThemeHelper } from './types'

/**
 * Tema per defecte: tokens semàntics en un sol lloc.
 * Per evitar className llargs repetits als tags, els components de la app
 * usen aquests tokens: th.surface, th.panel, th.menuLink(...), etc.
 */

const surface = 'bg-white dark:bg-black'
const border = 'border-gray-200 dark:border-gray-800'
const text = 'text-gray-800 dark:text-gray-100'
const muted = 'text-gray-500 dark:text-gray-400'
const faint = 'text-gray-400 dark:text-gray-500'
const hover = 'hover:bg-gray-100 dark:hover:bg-gray-900'

export const defaultTheme: ThemeHelper = {
  // tokens base
  surface,
  border,
  text,
  muted,
  faint,
  hover,
  link: 'text-blue-500 font-bold',
  divider: cn('my-2 border-t', border),

  // estructura de pàgina
  app: 'h-screen flex flex-col',
  pageArea: 'flex-1 overflow-hidden flex flex-col',
  page: 'flex flex-col flex-1 overflow-hidden',
  scrollPage: 'flex-1 overflow-y-auto p-4',
  panel: cn('rounded-lg border shadow-lg p-2', surface, border),

  // header + menú hamburguesa
  header: cn('relative flex-none px-4 py-2 shadow z-10', surface),
  pageTitle: 'text-lg font-semibold',
  iconButton: cn('p-1.5 -mr-1 text-gray-700 dark:text-gray-200 hover:text-black dark:hover:text-white'),
  menuLink: (active: boolean) =>
    cn('rounded-md px-3 py-2 text-sm', text, hover, active && 'font-bold bg-gray-100 dark:bg-gray-900'),
  menuLabel: cn('px-3 pb-1 text-xs', faint),
  themeOption: (active: boolean) =>
    cn(
      'flex-1 flex flex-col items-center gap-0.5 rounded-md px-2 py-1.5 text-xs',
      muted,
      hover,
      active && 'bg-gray-100 dark:bg-gray-900 text-black dark:text-white font-semibold',
    ),

  // cerca de verbs
  searchBar: 'flex-none p-4 mx-3 flex items-center gap-2',
  tabs: 'flex w-full px-7',
  tab: (side: 'left' | 'right', active: boolean) =>
    cn(
      'rounded-none! border-b! border-b-gray-400! dark:border-b-gray-600!',
      side === 'left' ? 'rounded-tl-md!' : 'rounded-tr-md!',
      active && 'bg-violet-700 font-bold',
    ),
  listArea: 'flex flex-1 overflow-hidden',
  listCol: cn('flex-1 flex flex-col overflow-hidden w-full h-full', surface),
  listScroll: 'flex-1 overflow-y-auto px-5',
  listDivider: 'divide-y divide-gray-200 dark:divide-gray-800',
  listItem: 'flex items-baseline gap-3 py-1.5 sm:py-2 hover:bg-muted/50 px-1',
  translation: 'text-sm italic text-gray-500',
  notice: 'p-4 text-sm text-gray-500',

  // paginació (dalt del llistat)
  pagination: cn(
    'order-first flex-none flex items-center justify-center gap-1 sm:gap-1.5 px-3 py-2 sm:py-2.5 border-b flex-wrap',
    surface,
    border,
  ),
  pageBtn: 'h-7 min-w-7 px-0 text-xs sm:h-8 sm:min-w-8 sm:text-sm tabular-nums',
  pageBtnNav: 'h-7 px-1.5 sm:h-8 sm:px-4',
  ellipsis: 'px-0.5 text-gray-400 select-none text-xs sm:text-sm',
  perPageLabel: 'flex items-center gap-1 sm:gap-1.5 text-xs sm:text-sm text-gray-500 ml-1 sm:ml-2',
  perPageSelect: 'h-7 sm:h-8 rounded-md border bg-background px-1.5 sm:px-2 text-xs sm:text-sm',
  totalCount: 'hidden sm:inline text-xs text-gray-400 ml-2',

  // índex alfabètic
  letters: cn(
    'flex-none self-stretch flex flex-col items-center justify-start gap-0 px-1.5 py-1.5 text-[10px] leading-none sm:text-xs',
    muted,
  ),
  letter: (active: boolean) => cn('hover:text-blue-600', active && 'font-bold text-blue-600'),

  // detalls / peu
  footerNote: cn('p-2 text-xs w-full', muted),
}
