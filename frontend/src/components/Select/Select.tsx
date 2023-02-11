import { useState } from "react";
import { ReactComponent as CaretIcon } from "../../assets/caret.svg";
import "./select.scss";

interface itemList {
  id?: string;
  name?: string;
}

interface ISelectProps {
  itemList: itemList & Record<string, any>;
  onChangeCallback: Function;
  // Rest props
  [x: string]: any;
}

// TODO: Add overflow scrolling, unit testing, overlay for outside clicks, correct some styling issues.
// TODO: 2. Accessibility
export default function Select({
  itemList,
  onChangeCallback,
  ...props
}: ISelectProps): JSX.Element {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const onSelectionClicked = (id: string): void => {
    console.log(id);
    onChangeCallback(id);
    setIsOpen(false);
  };

  return (
    <div className="select">
      <button
        className="select__toggle"
        onClick={() => {
          setIsOpen((prevState) => !prevState);
        }}
      >
        {
          // eslint-disable-next-line react/prop-types
          props.defaultValue
        }
        <CaretIcon
          className={`select__toggle-caret ${
            isOpen ? "select__toggle-caret--open" : ""
          }`}
        />
      </button>
      {isOpen && (
        <ul className="select__item-container">
          {itemList.map(({ id, name }: itemList) => {
            return (
              <li
                className="select__item"
                value={id || name}
                key={id || name}
                onClick={() => {
                  onSelectionClicked(id || "");
                }}
              >
                {name}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
