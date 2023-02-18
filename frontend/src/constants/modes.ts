import { parseSelectValues } from "../utils";

const rawModes = ["ranked", "aram"];

export default rawModes.map((mode) => {
  return {
    label: parseSelectValues(mode),
    value: mode,
  };
});
