import { parseSelectValues } from "../utils";

const rawLanes = ["default", "top", "jungle", "middle", "bottom", "support"];

export default rawLanes.map((lane) => {
  return {
    label: parseSelectValues(lane),
    value: lane,
  };
});
