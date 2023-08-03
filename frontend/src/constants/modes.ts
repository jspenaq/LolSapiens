import { parseSelectValues } from "../utils";

const rawModes = ["ranked", "aram", "arena"];

export default rawModes.map((mode) => {
  return {
    label: parseSelectValues(mode),
    value: mode,
  };
});
