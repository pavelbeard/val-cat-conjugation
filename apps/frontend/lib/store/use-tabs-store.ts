import { create } from "zustand";

interface TabsStore {
  tab: "top_verbs" | "verbs";
  setTab: (tab: "top_verbs" | "verbs") => void;
}

export const useTabsStore = create<TabsStore>()((set) => ({
  tab: "verbs",
  setTab: (tab) => set({ tab }),
}));
