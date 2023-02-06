import { ReactNode } from "react";
import Portal from "./Portal";

const Tooltip = ({
  children,
  show = false,
}: {
  children: ReactNode;
  show: boolean;
}) => {
  console.log(children);
  return show ? (
    <Portal>
      <div className="tooltip">{children}</div>
    </Portal>
  ) : null;
};

export default Tooltip;
