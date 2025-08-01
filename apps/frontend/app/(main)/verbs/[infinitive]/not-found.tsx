import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-4">
      <h1 className="text-2xl font-bold text-red-600">
        No ha encontrado el verbo
      </h1>
      <Link href="/verbs" className="px-4 py-2 bg-blue-500 text-white rounded">
        Volver a la lista de verbos
      </Link>
    </div>
  );
}
