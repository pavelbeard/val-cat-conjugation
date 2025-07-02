import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";

interface IVerbOpenHandler {
  verbId: string;
  isOpen: boolean;
  handleOpen: () => void;
  handleClose: () => void;
}

export default function useVerbModalHandler({
  verbId,
  isOpen,
  handleOpen,
  handleClose,
}: IVerbOpenHandler) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const handleOpenModalForVerb = useCallback(() => {
    handleOpen();
    const params = new URLSearchParams(searchParams.toString());
    params.set("modal", "true");
    params.set("verb", verbId);
    router.push(`${pathname}?${params.toString()}`);
  }, [searchParams, verbId, router]);

  const handleCloseModalForVerb = useCallback(() => {
    console.log("Closing modal for verb:", verbId);
    handleClose(); // This should be handleClose, but we keep it for consistency with the original code
    router.push(pathname);
  }, [verbId, router, pathname]);

  return { handleOpenModalForVerb, handleCloseModalForVerb };
}
