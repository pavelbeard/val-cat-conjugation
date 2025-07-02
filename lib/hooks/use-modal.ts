"use client";

import { useState } from "react";

export default function useModal() {
  const [isOpen, setIsOpen] = useState(false);

  const modal = {
    isOpen,
    openModal: () => {
      setIsOpen(true);
    },
    closeModal: () => {
      setIsOpen(false);
    },
  };

  return modal;
}
