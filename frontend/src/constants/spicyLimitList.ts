import { parseSelectValues } from "../utils";

const rawSpicyLimit = ["10","15","20"];

export default rawSpicyLimit.map((limit) => {
  return {
    label: parseSelectValues(limit),
    value: limit,
  };
});
