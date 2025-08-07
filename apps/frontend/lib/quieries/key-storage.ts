const verbsQueryKeys = {
  getVerbs: () => ["verbs"],
  getVerbByInfinitive: (infinitive: string) => ["verb", infinitive],
  getVerbsByForm: (form: string) => ["verbs", "form", form],
  getTopVerbs: () => ["verbs", "top"],
};

const staffQueryKeys = {
  getSettings: () => ["settings"],
};

export { staffQueryKeys, verbsQueryKeys };
