import { updateClicks } from "@/actions/verbs";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { verbsQueryKeys } from "../quieries/key-storage";
import { useVerbSearch } from "./use-verb-search";

export default function useVerbClick(form: string) {
  const queryClient = useQueryClient();
  const { tab } = useVerbSearch();

  const mutation = useMutation({
    mutationFn: () => updateClicks(form),
    onSuccess: () => {
      if (tab === "top_verbs") {
        queryClient.invalidateQueries({
          queryKey: verbsQueryKeys.getTopVerbs(),
        });
      } else if (tab === "verbs") {
        queryClient.invalidateQueries({
          queryKey: verbsQueryKeys.getVerbs(),
        });
      }
    },
  });

  const handleVerbClick = () => {
    mutation.mutate();
  };

  return {
    handleVerbClick,
    isLoading: mutation.isPending,
    error: mutation.error,
  };
}
