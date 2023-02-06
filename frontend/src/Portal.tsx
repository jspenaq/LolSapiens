import { ReactNode } from "react";
import { createPortal } from "react-dom";

const Portal = ({ children }: { children: ReactNode }) => {
  const overlay = document.getElementById("overlay") as HTMLElement;
  return createPortal(<div className="portal">{children}</div>, overlay);
};

export default Portal;
