import getVerbs from "@/actions/get-verbs";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import VerbsList from "@/components/verbs/verbs-list";
import { Suspense } from "react";

export default async function Search() {
  const verbs = getVerbs();

  return (
    <ScrollArea className="flex-1 bg-amber-400 w-full h-full p-4">
      {/* <h1>¡Bienvenidos y bienvenidas al Conjugador de verbos de valencià!</h1>
      <p>
        Esta aplicación te ayuda a conjugar verbos en valenciano de forma rápida
        y sencilla.
      </p>
      <p>
        Para usar el conjugador, simplemente introduce el verbo en infinitivo en
        el campo de búsqueda, presiona <b>Enter</b> y obtendrás la conjugación
        al instante.
      </p> */}
      <Suspense fallback={<div>Loading verbs...</div>}>
        <VerbsList verbsPromise={verbs} />
      </Suspense>
      <ScrollBar />
    </ScrollArea>
  );
}
