import { translateVerb } from "@/actions/verbs";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useEffect } from "react";
import { verbsQueryKeys } from "../quieries/key-storage";
import { Database__VerbOutput } from "../types/verbs";

export default function useVerbTranslate({
  verb,
}: {
  verb: Database__VerbOutput;
}) {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (verb: string) => translateVerb(verb),
    onSuccess: (data) => {
      queryClient.setQueryData(
        verbsQueryKeys.getVerbByInfinitive(verb.infinitive),
        data
      );
    },
  });

  useEffect(() => {
    if ((!verb?.moods || verb?.moods?.length === 0) && verb?.infinitive) {
      mutation.mutate(verb.infinitive);
    }
  }, [verb]);

  return {
    isTranslating: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error,
    mutate: mutation.mutate,
    data: queryClient.getQueryData<Database__VerbOutput>([
      "verb",
      verb.infinitive,
    ]),
  };
}
