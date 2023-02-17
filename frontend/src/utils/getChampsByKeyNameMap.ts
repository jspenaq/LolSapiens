import type { Champion } from "../types";

const getChampsByKeyName = (
  champions_data: Record<string, Champion>
): Record<string, Champion> => {
  return Object.values(champions_data).reduce<Record<string, Champion>>(
    (championsObj, currentChampion) => {
      // current champion isn't duplicated so we just add i

      championsObj[currentChampion.key_name] = currentChampion;

      return championsObj;
    },
    {}
  );
};

export default getChampsByKeyName;
