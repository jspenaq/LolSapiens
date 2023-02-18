import Select from "react-select";
import type { Option } from "../../types";

interface CustomSelectProps {
  options: Option[];
  onChange: (newValue: Option | null) => void;
  defaultValue?: Option | null;
}

const CustomSelect = ({
  onChange,
  options,
  defaultValue = null,
}: CustomSelectProps): JSX.Element => {
  return (
    <Select
      onChange={onChange}
      options={options}
      defaultValue={defaultValue}
      className="react-select-container"
      classNamePrefix="react-select"
    />
  );
};

export default CustomSelect;
