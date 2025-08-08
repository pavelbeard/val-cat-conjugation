import {
  getTopVerbs,
  getVerb,
  getVerbs,
  getVerbsByForm,
  getVerbsWithFirstLetter,
} from "@/actions/verbs";
import { queryOptions } from "@tanstack/react-query";
import { verbsQueryKeys } from "./key-storage";

export function queryOptionsGetVerbs() {
  return queryOptions({
    queryKey: verbsQueryKeys.getVerbs(),
    queryFn: () => getVerbs(),
  });
}

export function queryOptionsGetVerbsWithFirstLetter() {
  return queryOptions({
    queryKey: verbsQueryKeys.getVerbs(),
    queryFn: () => getVerbsWithFirstLetter(),
  });
}

export function queryOptionsGetVerbByInfinitive(infinitive: string) {
  return queryOptions({
    queryKey: verbsQueryKeys.getVerbByInfinitive(infinitive),
    queryFn: () => getVerb({ infinitive }),
  });
}

export function queryOptionsGetVerbsByForm(form: string) {
  return queryOptions({
    queryKey: verbsQueryKeys.getVerbsByForm(form),
    queryFn: () => getVerbsByForm(form),
  });
}

export function queryOptionsGetTopVerbs() {
  return queryOptions({
    queryKey: verbsQueryKeys.getTopVerbs(),
    queryFn: () => getTopVerbs(),
    staleTime: 0,
  });
}
