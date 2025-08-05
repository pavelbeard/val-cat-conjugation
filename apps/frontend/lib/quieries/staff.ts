import { getSettings } from "@/actions/staff";
import { queryOptions } from "@tanstack/react-query";
import { staffQueryKeys } from "./key-storage";

export function queryOptionsGetSettings() {
  return queryOptions({
    queryKey: staffQueryKeys.getSettings(),
    queryFn: async () => getSettings(),
  });
}
