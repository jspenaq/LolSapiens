import type { ReactNode } from "react";
import { useState } from "react";

const Tooltip = ({
  children,
  tooltipContent,
  text = "",
}: {
  children: ReactNode;
  tooltipContent?: ReactNode;
  text?: string;
}): JSX.Element => {
  const [show, setShow] = useState<boolean>(false);

  const handleShow = (value: boolean) => () => {
    setShow(value);
  };

  return (
    // Se puede cambiar por las coords y portal... por ahora xD...
    <div>
      <div onMouseOver={handleShow(true)} onMouseOut={handleShow(false)}>
        {children}
      </div>
      {
        show &&
          // <Portal>l{

          (tooltipContent ?? <div className="tooltip">{text}</div>)
        // }</Portal>
      }
    </div>
  );
};

export default Tooltip;
