import { parseSelectValues } from "../utils";

const rawTiers = [
  "1trick",
  "diamond_plus",
  "platinum_plus",
  "gold_plus",
  "platinum",
  "gold",
  "silver",
];

export default rawTiers.map((tier) => {
  return {
    label: parseSelectValues(tier),
    value: tier,
  };
});
