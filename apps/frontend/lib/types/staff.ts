export interface Database__AppSettingsOutput {
  app_name: string;
  version: string;
  description: string;
  show_valencian: boolean;
  show_balearic: boolean;
  show_opt_pre2017: boolean;
}

export interface Database__AppSettingsUpdate {
  app_name?: string;
  version?: string;
  description?: string;
  show_valencian?: boolean;
  show_balearic?: boolean;
  show_opt_pre2017?: boolean;
}
