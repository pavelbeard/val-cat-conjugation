"use client";

import { useEffect } from "react";
import { createPortal } from "react-dom";

interface ModalProps {
  isOpen: boolean;
  handleClose?: () => void;
  children: Readonly<React.ReactNode>;
}

export default function Modal({ isOpen, handleClose, children }: ModalProps) {
  // escape key handling
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key == "Escape" && isOpen) {
        event.preventDefault();

        handleClose?.();
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, handleClose]);

  // prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }
  }, [isOpen]);

  return (
    isOpen &&
    createPortal(
      <div className="fixed inset-0 z-50 flex items-start justify-center bg-blue-300">
        <div
          className="p-4 m-4"
          onClick={(e) => e.stopPropagation()} // Prevent click from closing modal
        >
          {children}
        </div>
      </div>,
      document.body
    )
  );
}
