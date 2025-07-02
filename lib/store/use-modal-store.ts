import { create } from "zustand";
import { persist } from "zustand/middleware";

interface ModalStore {
  isOpen: boolean;
  openModal: () => void;
  closeModal: () => void;
}

export const useModalStore = create<ModalStore>()(
  persist(
    (set) => ({
      isOpen: false,
      openModal: () => set({ isOpen: true }),
      closeModal: () => set({ isOpen: false }),
    }),
    {
      name: "modal-storage", // unique name for the storage
    }
  )
);
