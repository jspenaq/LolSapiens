import { parseSelectValues } from "../utils";

const rawSpicy = ["0", "1", "2", "3", "4", "10"];

export default rawSpicy.map((spicy) => {
  return {
    label: parseSelectValues(spicy),
    value: spicy,
  };
});
