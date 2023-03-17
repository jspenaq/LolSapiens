import { ChampionList, Select } from "../../components";
import useSpicyPicks from "../../hooks/useSpicyPicks";
import classes from "./spicypicks.module.scss";
import { lanes, tiers, spicyLimitList } from "../../constants";
import { useState } from "react";
import type { Option } from "../../types";

const SpicyPicks = (): JSX.Element => {
  const [tier, setTier] = useState<Option | null>(tiers[0]);
  const [lane, setLane] = useState<Option | null>(lanes[0]);
  const [limit, setLimit] = useState<Option | null>(spicyLimitList[0]);

  const { data: picks } = useSpicyPicks({
    lane: lane?.value ?? "default",
    tier: tier?.value ?? "gold_plus",
    limit: limit?.value ?? "10",
  });

  const handleTier = (newValue: Option | null): void => {
    setTier(newValue);
  };
  const handleLane = (newValue: Option | null): void => {
    setLane(newValue);
  };
  const handleLimit = (newValue: Option | null): void => {
    setLimit(newValue);
  };

  return (
    <section className={classes["spicy-picks"]}>
      <h1>Top 10</h1>
      <div className={classes.controls}>
        <Select options={tiers} onChange={handleTier} value={tier} />
        <Select options={lanes} onChange={handleLane} value={lane} />
        <Select options={spicyLimitList} onChange={handleLimit} value={limit} />
      </div>

      {picks && Boolean(picks.length) && <ChampionList champions={picks} />}
    </section>
  );
};

export default SpicyPicks;
