"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";
import { useSettings } from "@/lib/hooks/use-settings";

export default function SettingsPageClient() {
  const { settings, updateSettings, form } = useSettings();

  return (
    <Card className="p-4 m-3">
      <CardHeader className="text-lg font-semibold">
        <CardTitle>{settings.app_name} Ajustes</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(updateSettings)}
            className="space-y-4"
          >
            <FormField
              control={form.control}
              name="show_valencian"
              render={({ field }) => (
                <FormItem className="flex items-center space-x-4">
                  <FormControl>
                    <Checkbox
                      checked={field.value || false}
                      onCheckedChange={(checked) => field.onChange(checked)}
                    />
                  </FormControl>
                  <FormLabel>Mostrar Valenciano</FormLabel>
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="show_balearic"
              render={({ field }) => (
                <FormItem className="flex items-center space-x-4">
                  <FormControl>
                    <Checkbox
                      checked={field.value || false}
                      onCheckedChange={(checked) => field.onChange(checked)}
                    />
                  </FormControl>
                  <FormLabel>Mostrar Balearic</FormLabel>
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="show_opt_pre2017"
              render={({ field }) => (
                <FormItem className="flex items-center space-x-4">
                  <FormControl>
                    <Checkbox
                      checked={field.value || false}
                      onCheckedChange={(checked) => field.onChange(checked)}
                    />
                  </FormControl>
                  <FormLabel>Mostrar Opciones Pre-2017</FormLabel>
                </FormItem>
              )}
            />
            <Button type="submit">Guardar Cambios</Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
