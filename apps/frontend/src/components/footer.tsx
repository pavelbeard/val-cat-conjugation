import { useParams } from '@tanstack/react-router'
import { L } from '@/lib/literals'

export const footerClass = 'flex-none p-2 text-xs w-full text-muted-foreground text-center'
const link = 'text-primary font-bold hover:underline'

/** Footer global: aviso de traducciones IA, materiales de referencia y font normativa.
 * Si la ruta actual és /verbs/$verb, els enllaços apunten al verb concret. */
export default function Footer() {
  const { verb } = useParams({ strict: false }) as { verb?: string }
  const softcatala = verb
    ? `https://www.softcatala.org/conjugador-de-verbs/verb/${verb.replace('-se', '').replace("-se'n", '')}`
    : 'https://www.softcatala.org/conjugador-de-verbs/'
  const diccionari = verb
    ? `https://www.diccionari.cat/catala-castella/${verb}`
    : 'https://www.diccionari.cat/'

  return (
    <footer className={footerClass}>
      {L.footer.iaWarning}
      <br />
      {L.footer.materials}{' '}
      <a className={link} target="_blank" rel="noreferrer" href={softcatala}>
        Softcatala
      </a>
      ,{' '}
      <a className={link} target="_blank" rel="noreferrer" href={diccionari}>
        Diccionari.cat
      </a>
      {' · '}
      {L.footer.fontNormativa}
    </footer>
  )
}
