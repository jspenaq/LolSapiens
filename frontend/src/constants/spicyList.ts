import { parseSelectValues } from "../utils";

const rawSpicy = ["0", "1", "2"];

export default rawSpicy.map((spicy) => {
  return {
    name: parseSelectValues(spicy),
    id: spicy,
  };
});
