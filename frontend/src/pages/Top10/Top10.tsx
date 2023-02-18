import { BanList, Select } from "../../components";
import useTop10 from "../../hooks/useTop10";
import classes from "./top10.module.scss";
import { lanes, tiers } from "../../constants";
import { useState } from "react";
import type { Option } from "../../types";

const Top10 = (): JSX.Element => {
  const [tier, setTier] = useState<Option | null>(tiers[0]);
  const [lane, setLane] = useState<Option | null>(lanes[0]);

  const { data: bans } = useTop10({
    lane: lane?.value ?? "default",
    tier: tier?.value ?? "gold_plus",
  });

  const handleTier = (newValue: Option | null): void => {
    setTier(newValue);
  };
  const handleLane = (newValue: Option | null): void => {
    setLane(newValue);
  };

  return (
    <section className={classes.top10}>
      <h1>Top 10</h1>
      <div className={classes.controls}>
        <Select options={tiers} onChange={handleTier} defaultValue={tier} />
        <Select options={lanes} onChange={handleLane} defaultValue={lane} />
      </div>

      {bans && Boolean(bans.length) && <BanList bans={bans} />}
    </section>
  );
};

export default Top10;
