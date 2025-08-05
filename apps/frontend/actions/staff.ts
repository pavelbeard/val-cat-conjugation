import {
  Database__AppSettingsOutput,
  Database__AppSettingsUpdate,
} from "@/lib/types/staff";
import { ApiClient } from "@/lib/utils/api-client";
import { createUrl } from "@/lib/utils/create-url";

export const getSettings = async () => {
  const response = await ApiClient.get<Database__AppSettingsOutput>(
    createUrl("settings")
  );
  return response;
};

export const updateSettings = async (settings: Database__AppSettingsUpdate) => {
  const response = await ApiClient.put<Database__AppSettingsOutput>(
    createUrl("settings"),
    settings
  );
  return response;
};
