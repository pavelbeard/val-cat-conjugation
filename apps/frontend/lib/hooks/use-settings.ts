import { updateSettings as updateSettings__action } from "@/actions/staff";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  useMutation,
  useQueryClient,
  useSuspenseQuery,
} from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z, ZodObject, ZodType } from "zod";
import { staffQueryKeys } from "../quieries/key-storage";
import { queryOptionsGetSettings } from "../quieries/staff";
import { Database__AppSettingsUpdate } from "../types/staff";

export type InterfaceToSchema<T> = ZodObject<{
  [K in keyof Partial<T>]: K extends keyof T ? ZodType<T[K]> : never;
}>;

export const updateSchema = z.object({
  app_name: z.string().optional(),
  version: z.string().optional(),
  description: z.string().optional(),
  show_valencian: z.boolean().optional(),
  show_balearic: z.boolean().optional(),
  show_opt_pre2017: z.boolean().optional(),
}) satisfies InterfaceToSchema<Database__AppSettingsUpdate>;

export function useSettings() {
  const queryClient = useQueryClient();
  const { data } = useSuspenseQuery(queryOptionsGetSettings());

  const form = useForm<z.infer<typeof updateSchema>>({
    defaultValues: data,
    resolver: zodResolver(updateSchema),
  });

  const mutation = useMutation({
    mutationFn: (settings: z.infer<typeof updateSchema>) =>
      updateSettings__action(settings),
    onSuccess: (data) => {
      queryClient.setQueryData(staffQueryKeys.getSettings(), data);
      toast.success("Ajustes actualizados correctamente");
    },
  });

  const updateSettings = (settings: z.infer<typeof updateSchema>) => {
    mutation.mutate(settings);
  };

  return {
    settings: data,
    updateSettings,
    form,
  };
}
