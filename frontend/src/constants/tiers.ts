import type { Option } from "../types";
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

export const tiers = rawTiers.map<Option>((tier) => {
  return {
    label: parseSelectValues(tier),
    value: tier,
  };
});
