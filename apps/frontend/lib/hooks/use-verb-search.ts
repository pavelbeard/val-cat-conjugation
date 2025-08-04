import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect } from "react";
import { useSearchStore } from "../store/use-search-store";
import { useTabsStore } from "../store/use-tabs-store";
import { useDebounce } from "./use-debounce";

export const useVerbSearch = () => {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const form = useSearchStore((state) => state.query);
  const setForm = useSearchStore((state) => state.setQuery);

  const tab = useTabsStore((state) => state.tab);
  const setTab = useTabsStore((state) => state.setTab);

  const debouncedForm = useDebounce(form, 500);

  const setSearchParams = (value: string) => {
    const newSearchParams = new URLSearchParams(searchParams.toString());

    let url;

    if (value === "") {
      url = pathname;
      newSearchParams.delete("form");
      setForm("");
    } else {
      url = `${pathname}?form=${value}`;
      newSearchParams.set("form", value);
    }

    router.push(url);
  };

  useEffect(() => {
    setSearchParams(debouncedForm);
  }, [debouncedForm]);

  useEffect(() => {
    if (tab === "verbs") {
      setSearchParams("");
    } else {
      setSearchParams(form);
    }
  }, [tab]);

  return { form, setForm, tab, setTab };
};
