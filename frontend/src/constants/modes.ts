import { parseSelectValues } from "../utils";

const rawModes = ["ranked", "aram"];

export default rawModes.map((mode) => {
  return {
    name: parseSelectValues(mode),
    id: mode,
  };
});
