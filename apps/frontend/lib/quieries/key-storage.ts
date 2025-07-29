const verbsQueryKeys = {
  getVerbs: () => ["verbs"],
  getVerbByInfinitive: (infinitive: string) => ["verb", infinitive],
  getVerbsByForm: (form: string) => ["verbs", "form", form],
};

export { verbsQueryKeys };
