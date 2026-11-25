/**
 * Literales de la UI centralizados (un solo sitio para cambiar/traducir textos).
 */
export const L = {
  header: {
    backToList: "Tornar a la llista",
    openMenu: "Obrir menú",
    closeMenu: "Tancar menú",
    menu: "Menú",
  },
  theme: {
    label: "Tema",
    system: "Sistema",
    light: "Clar",
    dark: "Fosc",
  },
  pages: {
    verbs: "Verbs",
    translator: "Traductor",
    ajusts: "Ajusts",
  },
  search: {
    inputLabel: "Cerca de verbs",
    placeholder: "Buscar verbs…",
    placeholderByForm: 'Buscar per forma (ex. "vaig")…',
    placeholderByTranslation: "Buscar per traducció…",
    byForm: "Per forma",
    byTranslation: "Per traducció",
    tabTop: "Verbs principals",
    tabAll: "Verbs",
    searching: "Buscant…",
    notFound: "Cap verb trobat.",
    notFoundFor: (q: string) => `Cap verb trobat per «${q}».`,
    letters: "Índex alfabètic",
  },
  pagination: {
    label: "Paginació",
    prev: "Pàgina anterior",
    next: "Pàgina següent",
    perPage: "Per pàgina",
    perPageShort: "Pàg.",
    perPageLabel: "Resultats per pàgina",
    total: (n: number) => `${n} verbs`,
  },
  footer: {
    iaWarning:
      "Advertencia: traducciones están creadas por un modelo de IA y pueden no ser precisas.",
    materials: "Materiales de referencia:",
    fontNormativa: "Font normativa: AVL",
  },
  verbDetail: {
    loading: "Carregant…",
    notFound: "Verb no trobat",
  },
  translator: {
    title: "Traductor",
    wip: "Work in Progress",
  },
  settings: {
    title: "Ajustes",
    showValencian: "Mostrar Valencià",
    showCatalan: "Mostrar Català",
    showBalearic: "Mostrar Balearic",
    showPre2017: "Mostrar Opciones Pre-2017",
  },
} as const;
