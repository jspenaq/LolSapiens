import type { ActionMeta } from "react-select";
import Select from "react-select";
import type { Option } from "../../types";

interface CustomSelectProps {
  options: Option[];
  onChange: (newValue: Option | null, action: ActionMeta<Option>) => void;
  defaultValue?: Option | null;
  name?: string;
  placeholder?: string;
}

const CustomSelect = ({
  onChange,
  options,
  defaultValue = null,
  name,
  placeholder,
}: CustomSelectProps): JSX.Element => {
  return (
    <Select
      onChange={onChange}
      options={options}
      defaultValue={defaultValue}
      className="react-select-container"
      classNamePrefix="react-select"
      name={name}
      placeholder={placeholder}
    />
  );
};

export default CustomSelect;
