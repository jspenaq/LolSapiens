/* eslint-disable @typescript-eslint/consistent-type-imports */
import { ReactNode } from "react";
import { createPortal } from "react-dom";

const Portal = ({ children }: { children: ReactNode }): JSX.Element => {
  const overlay = document.getElementById("overlay") as HTMLElement;
  return createPortal(children, overlay);
};

export default Portal;
