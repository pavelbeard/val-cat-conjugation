import { getVerb, getVerbs, getVerbsWithFirstLetter } from "@/actions/verbs";
import { queryOptions } from "@tanstack/react-query";
import { verbsQueryKeys } from "./key-storage";

export function queryOptionsGetVerbs() {
  return queryOptions({
    queryKey: verbsQueryKeys.getVerbs(),
    queryFn: async () => getVerbs(),
  });
}

export function queryOptionsGetVerbsWithFirstLetter() {
  return queryOptions({
    queryKey: verbsQueryKeys.getVerbs(),
    queryFn: async () => getVerbsWithFirstLetter(),
  });
}

export function queryOptionsGetVerbByInfinitive(infinitive: string) {
  return queryOptions({
    queryKey: verbsQueryKeys.getVerbByInfinitive(infinitive),
    queryFn: async () => getVerb({ infinitive }),
  });
}
