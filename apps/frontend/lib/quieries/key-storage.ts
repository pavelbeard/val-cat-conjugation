const verbsQueryKeys = {
  getVerbs: () => ["verbs"],
  getVerbByInfinitive: (infinitive: string) => ["verb", infinitive],
  getVerbsByForm: (form: string) => ["verbs", "form", form],
};

const staffQueryKeys = {
  getSettings: () => ["settings"],
};

export { staffQueryKeys, verbsQueryKeys };
