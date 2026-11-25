/**
 * Definició d'un tema reutilitzable de la UI.
 * Cada tema aporta els tokens base i les classes de component amb estat.
 * Per afegir un tema nou: crea un objecte ThemeHelper i registra'l amb
 * registerTheme('nom', meuTema) (vegeu index.ts).
 */
export interface ThemeHelper {
  // tokens base
  surface: string
  border: string
  text: string
  muted: string
  faint: string
  hover: string
  link: string
  divider: string

  // estructura de pàgina
  app: string
  pageArea: string
  page: string
  scrollPage: string
  panel: string

  // header + menú hamburguesa
  header: string
  pageTitle: string
  iconButton: string
  menuLink: (active: boolean) => string
  menuLabel: string
  themeOption: (active: boolean) => string

  // cerca de verbs
  searchBar: string
  tabs: string
  tab: (side: 'left' | 'right', active: boolean) => string
  listArea: string
  listCol: string
  listScroll: string
  listDivider: string
  listItem: string
  translation: string
  notice: string

  // paginació
  pagination: string
  pageBtn: string
  pageBtnNav: string
  ellipsis: string
  perPageLabel: string
  perPageSelect: string
  totalCount: string

  // índex alfabètic
  letters: string
  letter: (active: boolean) => string

  // detalls / peu
  footerNote: string
}
