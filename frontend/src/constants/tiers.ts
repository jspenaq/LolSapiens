import type { Option } from "../types";
import { parseSelectValues } from "../utils";

const rawTiers = [
  "1trick",
  "master_plus",
  "diamond_plus",
  "emerald_plus",
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
